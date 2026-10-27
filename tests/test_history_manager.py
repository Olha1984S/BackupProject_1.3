from pathlib import Path
from unittest.mock import patch

import config
import history_manager


def make_snapshots(history_path, names):
    history_path.mkdir(parents=True, exist_ok=True)
    for name in names:
        (history_path / name).mkdir()


def test_save_current_to_history_copies_files(tmp_path):
    current_path = tmp_path / "Current"
    history_path = tmp_path / "History"
    current_path.mkdir()
    (current_path / "file.txt").write_text("snapshot content", encoding="utf-8")

    snapshot_path = history_manager.save_current_to_history(current_path, history_path)

    assert snapshot_path.is_dir()
    assert (snapshot_path / "file.txt").read_text(encoding="utf-8") == "snapshot content"
    assert history_manager.get_snapshots(history_path) == [snapshot_path]


def test_cleanup_history_removes_oldest_until_limit(tmp_path):
    history_path = tmp_path / "History"
    names = [
        "2026-08-12_10-00-00",
        "2026-08-13_10-00-00",
        "2026-08-14_10-00-00",
    ]
    make_snapshots(history_path, names)

    history_manager.cleanup_history(history_path, max_snapshots=2)

    snapshots = history_manager.get_snapshots(history_path)
    assert [p.name for p in snapshots] == names[1:]


def test_cleanup_history_keeps_snapshots_when_at_limit(tmp_path):
    history_path = tmp_path / "History"
    names = ["2026-08-12_10-00-00", "2026-08-13_10-00-00"]
    make_snapshots(history_path, names)

    history_manager.cleanup_history(history_path, max_snapshots=2)

    assert [p.name for p in history_manager.get_snapshots(history_path)] == names


def test_cleanup_history_propagates_permission_error_when_deletion_is_needed(tmp_path):
    history_path = tmp_path / "History"
    make_snapshots(
        history_path,
        ["2026-08-12_10-00-00", "2026-08-13_10-00-00", "2026-08-14_10-00-00"],
    )

    with patch("history_manager.shutil.rmtree", side_effect=PermissionError("Access denied")):
        try:
            history_manager.cleanup_history(history_path, max_snapshots=2)
        except PermissionError:
            pass
        else:
            raise AssertionError("PermissionError should propagate when an old snapshot must be removed")


def test_cleanup_history_ignores_invalid_folder_names(tmp_path):
    history_path = tmp_path / "History"
    make_snapshots(
        history_path,
        ["2026-08-12_10-00-00", "2026-08-13_10-00-00", "2026-08-14_10-00-00", "MyImportantFolder"],
    )

    history_manager.cleanup_history(history_path, max_snapshots=2)

    assert (history_path / "MyImportantFolder").exists()
    assert len(history_manager.get_snapshots(history_path)) == 2


def test_cleanup_history_does_nothing_when_history_directory_is_missing(tmp_path):
    history_path = tmp_path / "History"

    history_manager.cleanup_history(history_path, max_snapshots=2)

    assert not history_path.exists()
