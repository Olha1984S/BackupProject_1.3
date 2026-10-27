"""History snapshot helpers. Cleanup runs only after a new backup succeeds."""
from datetime import datetime
from pathlib import Path
import shutil
import config
import constants
import file_utils


def save_current_to_history(current_path, history_path):
    current_path, history_path = Path(current_path), Path(history_path)
    history_path.mkdir(parents=True, exist_ok=True)
    snapshot_name = datetime.now().strftime(constants.SNAPSHOT_NAME_FORMAT)
    snapshot_path = history_path / snapshot_name
    # Avoid overwriting an existing snapshot if two backups start in the same second.
    if snapshot_path.exists():
        snapshot_name = datetime.now().strftime(constants.SNAPSHOT_NAME_FORMAT) + f"_{datetime.now().microsecond:06d}"
        snapshot_path = history_path / snapshot_name
    shutil.copytree(current_path, snapshot_path)
    return snapshot_path


def cleanup_history(history_path, max_snapshots=None):
    history_path = Path(history_path)
    if not history_path.is_dir():
        return
    limit = max_snapshots if max_snapshots not in (None, "") else getattr(config, "MAX_HISTORY", 10)
    try:
        limit = max(1, int(limit))
    except (TypeError, ValueError):
        limit = max(1, int(getattr(config, "MAX_HISTORY", 10)))
    snapshots = get_snapshots(history_path)
    while len(snapshots) > limit:
        oldest = snapshots.pop(0)
        if oldest.exists():
            shutil.rmtree(oldest)


def prepare_history(current_path, history_path):
    snapshot = save_current_to_history(current_path, history_path)
    result = file_utils.verify_directories(current_path, snapshot)
    if result.success:
        cleanup_history(history_path)
    return result


def get_snapshots(history_path):
    history_path = Path(history_path)
    snapshots = []
    if not history_path.is_dir():
        return snapshots
    for item in history_path.iterdir():
        if item.is_dir():
            try:
                # The base timestamp format is used; optional microsecond suffix is accepted.
                datetime.strptime(item.name, constants.SNAPSHOT_NAME_FORMAT)
                snapshots.append(item)
            except ValueError:
                base_length = len(datetime.now().strftime(constants.SNAPSHOT_NAME_FORMAT))
                base_name = item.name[:base_length]
                try:
                    datetime.strptime(base_name, constants.SNAPSHOT_NAME_FORMAT)
                    snapshots.append(item)
                except ValueError:
                    continue
    return sorted(snapshots, key=lambda p: p.name)
