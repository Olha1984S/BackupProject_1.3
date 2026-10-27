"""Backup engine for BackupProject 1.3.

Uses the paths selected in the GUI. Builds a verified staging copy first so a
failed/cancelled copy does not clear the existing Current backup.
"""
from pathlib import Path
from datetime import datetime
import shutil
import threading

import config
import file_utils
import disk_space
import history_manager


class BackupCancelled(Exception):
    """Raised when the user requests a cooperative stop."""


class FileCopyError(Exception):
    """A failure tied to a specific source file during copying."""

    def __init__(self, source_file, cause):
        self.source_file = Path(source_file)
        self.cause = cause
        super().__init__(f"Could not copy source file {self.source_file}: {cause}")


def start_backup(source_path=None, backup_path=None, copies_to_keep=None,
                 progress_callback=None, cancel_event=None, resume_event=None,
                 exit_event=None):
    source = Path(source_path or config.SOURCE_PATH).resolve()
    destination = Path(backup_path or config.PROJECT_PATH).resolve()
    current = destination / "Current"
    history = destination / "History"
    staging = destination / ".Current_backup_staging"
    previous = destination / ".Current_backup_previous"
    cancel_event = cancel_event or threading.Event()
    resume_event = resume_event or threading.Event()
    exit_event = exit_event or threading.Event()
    report = progress_callback or (lambda copied, total, status: None)

    def check_cancel(copied=0, total=0):
        """Pause at a safe checkpoint until the user resumes or exits.

        Continue can cancel a stop request before this checkpoint is reached.
        If the worker has already reached the checkpoint, resume_event releases
        it. The worker thread never touches Tk widgets directly.
        """
        if not cancel_event.is_set():
            return

        report(copied, total, "StoppingReady")
        while True:
            # Wait in short intervals so shutdown remains responsive even if
            # an event is set independently of the normal GUI callback.
            if resume_event.wait(timeout=0.1):
                resume_event.clear()
                if exit_event.is_set():
                    raise BackupCancelled("Backup stopped by user after a safe operation boundary.")
                cancel_event.clear()
                return
            if exit_event.is_set():
                raise BackupCancelled("Backup stopped by user after a safe operation boundary.")

    if not source.is_dir():
        return {"status": "error", "message": f"Source folder does not exist: {source}"}
    if not destination.is_dir():
        return {"status": "error", "message": f"Backup destination does not exist: {destination}"}
    if source == destination or source in destination.parents or destination in source.parents:
        return {"status": "error", "message": "Source and backup destination must not contain each other."}

    try:
        files = sorted(p for p in source.rglob("*") if p.is_file())
        source_size = sum(p.stat().st_size for p in files)
        current_size = file_utils.get_directory_size(current) if current.is_dir() else 0
        required = source_size + current_size
        free = shutil.disk_usage(destination).free
        print(f"Backup precheck: required={required} bytes, available={free} bytes, destination={destination}")
        print("DEBUG: passed disk-space precheck")
        if free < required:
            return {"status": "low_space", "required_space": required, "available_space": free,
                    "message": "Not enough free disk space."}

        if staging.exists():
            shutil.rmtree(staging)
        print("DEBUG: preparing staging directory")
        staging.mkdir(parents=True, exist_ok=True)
        if history.exists() is False:
            history.mkdir(parents=True, exist_ok=True)

        report(0, len(files), "Copying")
        copied = 0
        for item in files:
            check_cancel(copied, len(files))
            relative = item.relative_to(source)
            target = staging / relative
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
            except OSError as exc:
                # Preserve the original source path for Window 13; do not
                # try to recover it by parsing the destination-side error text.
                raise FileCopyError(item, exc) from exc
            copied += 1
            report(copied, len(files), "Copying")

        check_cancel(copied, len(files))
        verification = file_utils.verify_directories(source, staging)
        if not verification.success:
            raise RuntimeError(f"Staging verification failed: {verification.result_code}")
        report(copied, len(files), "Verifying")

        # A stop requested during verification is handled before entering the
        # Current/History transaction. Once snapshot/replacement starts, finish
        # the transaction before pausing so Current is never left half-swapped.
        check_cancel(copied, len(files))

        # Preserve the existing Current as a History snapshot before replacing it.
        if current.is_dir() and file_utils.has_files(current):
            snapshot_path = history_manager.save_current_to_history(current, history)
            snapshot_verification = file_utils.verify_directories(current, snapshot_path)
            if not snapshot_verification.success:
                raise RuntimeError(f"History snapshot verification failed: {snapshot_verification.result_code}")

        # Replace Current with the verified staging directory; roll back on failure.
        if previous.exists():
            shutil.rmtree(previous)
        moved_current = False
        try:
            if current.exists():
                current.rename(previous)
                moved_current = True
            staging.rename(current)
        except Exception:
            if moved_current and not current.exists() and previous.exists():
                previous.rename(current)
            raise

        if previous.exists():
            shutil.rmtree(previous)

        # Cleanup is intentionally after successful snapshot creation and Current replacement.
        keep = copies_to_keep if copies_to_keep not in (None, "") else getattr(config, "MAX_HISTORY", 10)
        try:
            keep = max(1, int(keep))
        except (TypeError, ValueError):
            keep = max(1, int(getattr(config, "MAX_HISTORY", 10)))
        history_manager.cleanup_history(history, max_snapshots=keep)
        # Reaching this point means the complete backup transaction is done.
        # A stop requested during snapshot/replacement is therefore reported
        # as a completed backup rather than a cancellation of committed data.
        report(len(files), len(files), "Completed")
        print(f"Backup completed successfully: {destination}")
        return {"status": "success", "files_copied": len(files), "total_files": len(files),
                "message": "Backup completed successfully."}

    except FileCopyError as exc:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        print(f"Backup file-copy error: source={exc.source_file}; cause={exc.cause!r}")
        return {
            "status": "file_error",
            "error_file": str(exc.source_file),
            "reason": "The file may be unavailable or access may be restricted.",
            "message": str(exc),
        }
    except BackupCancelled:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        print("Backup stopped at a safe checkpoint before committing the new Current backup.")
        return {"status": "cancelled", "message": "Backup stopped safely. The previous Current backup was preserved."}
    except Exception as exc:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        print(f"Backup failed: {exc}")
        return {"status": "error", "message": str(exc)}


def compare_with_current(source_files, current_files):
    return source_files - current_files, current_files - source_files, source_files & current_files
