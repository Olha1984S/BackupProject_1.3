# Configuration

## Location

User settings are stored outside the project directory:

`%LOCALAPPDATA%\BackupManager\config.json`

On Windows, `%LOCALAPPDATA%` resolves to the current user's local application-data directory. The application uses the `BackupManager` subdirectory.

## Configuration keys

The current controller uses the following configuration keys:

| Key | Purpose |
| --- | --- |
| `source_path` | Path to the directory selected for backup. |
| `backup_path` | Backup destination path. |
| `copies_to_keep` | Number of history copies to retain. |
| `backup_frequency` | Selected backup frequency. |
| `custom_interval_days` | Number of days for a custom interval. |
| `frequency_screen` | Scheduling screen/state used by the setup flow. |
| `first_backup_date` | Configured date for the first backup. |
| `first_backup_time` | Configured time for the first backup. |
| `first_backup_start_mode` | Selected mode for starting the first backup. |
| `first_backup_actual_start` | Recorded actual start value for the first backup flow. |
| `setup_completed` | Indicates whether initial setup has been completed. |

Values and validation rules should be confirmed against the current implementation before editing the configuration manually.

## Saving settings

The controller saves settings through a temporary file and then replaces the target configuration file. This helps reduce the risk of corrupting the file if writing is interrupted.

## Notes

- Do not store configuration in the project source directory.
- Avoid editing `config.json` while the application is running.
- Keep a copy of the file before making manual changes.
- A configuration change can affect the next screen or backup workflow; verify the result through the application.
