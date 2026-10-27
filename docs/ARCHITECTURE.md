# Architecture

## 1. Overview

BackupProject 1.3 is a Windows desktop backup application implemented in Python. Its GUI uses a single Tkinter root window, one shared Canvas, and a controller that switches between screen classes.

The controller coordinates navigation, configuration persistence, disk-space checks, and transitions into the backup workflow. Existing working behavior should not be changed unless a specific requirement or defect calls for it.

## 2. Storage model

The destination contains two main directories:

- `Current`: the latest completed backup.
- `History`: retained previous snapshots.

History snapshot directories use timestamp names in the format `YYYY-MM-DD_HH-MM-SS`. The application generates these names; users are not expected to name snapshot folders manually.

The number of retained history copies is controlled by configuration. Cleanup must be handled carefully so that only eligible older snapshots are removed.

## 3. GUI architecture

- A single `tk.Tk` root is created for the application.
- A single Canvas is shared by the screens.
- The controller selects and displays GUI screen classes as the user moves through the workflow.
- Screen classes must not create additional Tk roots, Canvases, or independent `mainloop()` calls.

The controller dynamically loads GUI classes from the `gui/` package.

## 4. Configuration

Configuration is stored at:

`%LOCALAPPDATA%\BackupManager\config.json`

This keeps user settings outside the source-code directory. Saving uses a temporary file followed by replacement of the target file to reduce the risk of leaving a partially written configuration.

Known configuration keys include:

- `source_path`
- `backup_path`
- `copies_to_keep`
- `backup_frequency`
- `custom_interval_days`
- `frequency_screen`
- `first_backup_date`
- `first_backup_time`
- `first_backup_start_mode`
- `first_backup_actual_start`
- `setup_completed`

## 5. Disk-space check

Before a backup begins, the controller checks the size of the source data and the existing `Current` data, then checks destination disk usage. The directory-size routine can accept a cancellation event and checks for cancellation while traversing filesystem entries.

The disk-space scan runs in a background thread so that the GUI can remain responsive. The worker returns its result to the Tkinter thread using `root.after`.

The space-check routine can return:
- `True` when there is enough space.
- `False` when space is insufficient.
- `None` when the check encounters an error.
- `"cancelled"` when the scan is cancelled.

Callers must handle these outcomes explicitly. A cancelled or failed scan must not be treated as a successful space check.

## 6. Cancellation behavior

Cancellation during a disk-space scan is cooperative: the controller sets a cancellation event, and the scan stops when it reaches a cancellation check.

- **Continue:** waits for the cancelled scan to finish, then starts a new scan from the beginning. Partial size results are not reused.
- **Exit:** waits for the scan to finish before exiting the application.
- **Stop:** displays the stopping screen while cancellation is being processed.

The backup worker uses separate cancellation/resume/exit events. These controls should remain distinct from the disk-scan cancellation event.

## 7. Screen flow

The controller connects GUI screens for setup, returning users, backup start, progress, stopping, success, errors, and insufficient disk space. The relevant controller and screen classes define the precise navigation flow.

Known screen roles include:
- Window 10: backup progress.
- Window 11: stopping/cancellation in progress.
- Window 12: successful completion.
- Window 13: backup error.
- Window 14: insufficient disk space.

When a file-related problem can be corrected by the user, the intended behavior is to show the error screen rather than instructing a non-technical user to inspect the console.

## 8. Module responsibilities

The project includes modules such as:

| Module | Responsibility |
| --- | --- |
| `app.py` | Application entry point. |
| `app_controller.py` | GUI navigation, orchestration, and coordination of the workflow. |
| `backup_manager.py` | Backup execution logic. |
| `history_manager.py` | History snapshots and retention cleanup. |
| `disk_space.py` | Disk-space-related operations. |
| `file_utils.py` | File and directory utilities. |
| `project_initializer.py` | Initial project/storage setup. |
| `storage_validator.py` | Storage destination validation. |
| `messages.py` | User-facing messages. |
| `config.py` | Configuration loading and saving. |
| `constants.py` | Shared constants. |
| `gui/` | Tkinter screen classes. |

Confirm the exact responsibility of each module against the current source before making architectural changes.

## 9. Important safety rules

- Do not delete history snapshots until the backup workflow has determined which snapshots are eligible for cleanup.
- Do not use partial results from a cancelled disk-space scan.
- Keep all Tkinter UI updates on the Tkinter thread.
- Preserve the single-root, shared-Canvas architecture.
- Avoid changing working logic as part of documentation or GUI-only changes.
