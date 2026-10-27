from unittest.mock import patch
from exceptions import CopyFileError

import app
import config
import messages


def test_main_handles_permission_error(tmp_path, monkeypatch, capsys):
    source_path = tmp_path / "Source"
    source_path.mkdir()

    test_file = source_path / "problem.txt"
    original_error = PermissionError("Access denied")

    monkeypatch.setattr(
        config,
        "SOURCE_PATH",
        str(source_path),
    )

    with patch("app.backup_manager.start_backup") as mock_start_backup:
        mock_start_backup.side_effect = CopyFileError(
            test_file,
            original_error,
        )

        app.main()

    captured = capsys.readouterr()

    assert messages.COPY_FILE_ERROR.format(test_file) in captured.out