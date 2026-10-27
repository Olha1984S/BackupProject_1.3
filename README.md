# BackupProject 1.3

BackupProject is a Windows desktop application designed to create and manage backups of a selected source directory on local storage, a USB drive, or a network location.

## Current status

Version 1.3 contains a Tkinter-based graphical interface and a controller that coordinates the application's screens and backup workflow. The documentation describes the current implementation; features should be verified by running the relevant tests before release.

## Main features

- Configure a source directory and a backup destination.
- Store the latest backup in `Current`.
- Keep previous backup snapshots in `History`.
- Configure the number of history copies to retain.
- Check available destination space before starting a backup.
- Display insufficient-space and backup-error screens.
- Save application settings in a user-specific configuration file.
- Perform disk-space scanning in a background thread and support cooperative cancellation.

## Storage layout

The backup destination uses the following folders:

- `Current` — the latest backup.
- `History` — previous snapshots, named with a timestamp in the format `YYYY-MM-DD_HH-MM-SS`.

## Configuration

Settings are stored outside the project directory at:

`%LOCALAPPDATA%\BackupManager\config.json`

The application creates or updates this file when settings are saved.

## Project structure

The project contains the application controller, backup and storage logic, configuration/constants, utility modules, GUI screen classes, and tests. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for module responsibilities and workflow details.

## Running the application

From the project directory, activate the intended Python environment and run:

```bash
python app.py
```

Use the project's configured virtual environment when running tests. For example:

```bash
python -m pytest
```

The exact test command may depend on the test files and local environment.

## Testing and release notes

The earlier BackupProject 1.1 baseline had 21 passing automated tests. That result does not establish that all BackupProject 1.3 GUI flows have been tested. Re-run the current test suite and manually verify the GUI workflow before publishing a release.

## Current limitations and follow-up

- Automatic scheduling through Windows Task Scheduler must be implemented and/or verified separately.
- Test coverage for all GUI screens and cancellation paths should be confirmed before release.
- The behavior of each supported storage type should be validated in the target environment.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for planned verification and follow-up work.
