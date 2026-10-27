from pathlib import Path
from collections import namedtuple

import backup_manager
import config


DiskUsage = namedtuple("DiskUsage", "total used free")


def configure_paths(monkeypatch, project_path, source_path):
    monkeypatch.setattr(config, "PROJECT_PATH", str(project_path))
    monkeypatch.setattr(config, "SOURCE_PATH", str(source_path))


def patch_disk_usage(monkeypatch, free_space=10_000_000):
    monkeypatch.setattr(
        backup_manager.shutil,
        "disk_usage",
        lambda _path: DiskUsage(free_space, 0, free_space),
    )


def test_start_backup_creates_verified_current(tmp_path, monkeypatch):
    source_path = tmp_path / "Source"
    destination_path = tmp_path / "Destination"
    current_path = destination_path / "Current"
    source_path.mkdir()
    current_path.mkdir(parents=True)
    destination_path.mkdir(exist_ok=True)

    source_file = source_path / "test.txt"
    source_file.write_text("backup content", encoding="utf-8")

    configure_paths(monkeypatch, destination_path, source_path)
    patch_disk_usage(monkeypatch)

    result = backup_manager.start_backup()

    assert result["status"] == "success"
    assert (current_path / "test.txt").read_text(encoding="utf-8") == "backup content"
    assert not (destination_path / ".Current_backup_staging").exists()
    assert not (destination_path / ".Current_backup_previous").exists()


def test_start_backup_returns_low_space_without_replacing_current(tmp_path, monkeypatch):
    source_path = tmp_path / "Source"
    destination_path = tmp_path / "Destination"
    current_path = destination_path / "Current"
    source_path.mkdir()
    current_path.mkdir(parents=True)
    (source_path / "new.txt").write_text("new", encoding="utf-8")
    (current_path / "old.txt").write_text("old backup", encoding="utf-8")

    configure_paths(monkeypatch, destination_path, source_path)
    patch_disk_usage(monkeypatch, free_space=0)

    result = backup_manager.start_backup()

    assert result["status"] == "low_space"
    assert (current_path / "old.txt").read_text(encoding="utf-8") == "old backup"
    assert not (current_path / "new.txt").exists()


def test_copy_error_preserves_existing_current_and_cleans_staging(tmp_path, monkeypatch):
    source_path = tmp_path / "Source"
    destination_path = tmp_path / "Destination"
    current_path = destination_path / "Current"
    source_path.mkdir()
    current_path.mkdir(parents=True)
    source_file = source_path / "problem.txt"
    source_file.write_text("source", encoding="utf-8")
    old_file = current_path / "old.txt"
    old_file.write_text("known good backup", encoding="utf-8")

    configure_paths(monkeypatch, destination_path, source_path)
    patch_disk_usage(monkeypatch)

    def fail_copy(_source, _destination):
        raise PermissionError("Access denied")

    monkeypatch.setattr(backup_manager.shutil, "copy2", fail_copy)

    result = backup_manager.start_backup()

    assert result["status"] == "file_error"
    assert result["error_file"] == str(source_file)
    assert old_file.read_text(encoding="utf-8") == "known good backup"
    assert not (current_path / "problem.txt").exists()
    assert not (destination_path / ".Current_backup_staging").exists()


def test_start_backup_rejects_missing_source(tmp_path, monkeypatch):
    destination_path = tmp_path / "Destination"
    destination_path.mkdir()
    configure_paths(monkeypatch, destination_path, tmp_path / "MissingSource")

    result = backup_manager.start_backup()

    assert result["status"] == "error"
    assert "Source folder does not exist" in result["message"]


def test_start_backup_rejects_source_and_destination_containment(tmp_path, monkeypatch):
    source_path = tmp_path / "Source"
    destination_path = source_path / "Backups"
    destination_path.mkdir(parents=True)
    configure_paths(monkeypatch, destination_path, source_path)

    result = backup_manager.start_backup()

    assert result["status"] == "error"
    assert "must not contain each other" in result["message"]


def test_start_backup_saves_previous_current_to_history(tmp_path, monkeypatch):
    source_path = tmp_path / "Source"
    destination_path = tmp_path / "Destination"
    current_path = destination_path / "Current"
    source_path.mkdir()
    current_path.mkdir(parents=True)
    (source_path / "new.txt").write_text("new backup", encoding="utf-8")
    (current_path / "old.txt").write_text("previous backup", encoding="utf-8")

    configure_paths(monkeypatch, destination_path, source_path)
    patch_disk_usage(monkeypatch)

    result = backup_manager.start_backup()

    assert result["status"] == "success"
    assert (current_path / "new.txt").read_text(encoding="utf-8") == "new backup"
    assert not (current_path / "old.txt").exists()

    snapshots = list((destination_path / "History").iterdir())
    assert len(snapshots) == 1
    assert (snapshots[0] / "old.txt").read_text(encoding="utf-8") == "previous backup"
