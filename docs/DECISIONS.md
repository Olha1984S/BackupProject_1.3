# Architecture and Design Decisions

This document records the decisions that should be preserved unless a specific requirement justifies a change.

## Core decisions

### Single Tkinter root and shared Canvas

The application uses one `tk.Tk` root, one shared Canvas, and a controller that switches between GUI screen classes. Individual screens must not create additional roots, Canvases, or their own `mainloop()` calls.

**Reason:** A single GUI lifecycle keeps navigation and event handling centralized.

### User configuration outside the project

Settings are stored at `%LOCALAPPDATA%\BackupManager\config.json`.

**Reason:** User-specific settings should persist independently of the source-code directory and project updates.

### `Current` and `History` storage model

`Current` holds the latest backup, while `History` stores previous snapshots. Snapshot directories are named by the application using the `YYYY-MM-DD_HH-MM-SS` format.

**Reason:** The latest backup is easy to identify, and timestamped snapshots support retention and history management without requiring manual folder naming.

### Background disk-space scan

The disk-space scan runs in a background thread, and results are passed back to the GUI thread using `root.after`.

**Reason:** Traversing large directories should not freeze the interface.

### Cooperative cancellation

The disk-space scan accepts a cancellation event and checks it while traversing filesystem entries.

**Reason:** Cancellation should be responsive without unsafe thread termination.

### Restart after cancellation

When the user chooses to continue after cancelling a disk-space scan, the application waits for the old scan to finish and starts a new scan from the beginning. Partial results are not reused.

**Reason:** A partial scan cannot reliably establish whether sufficient space is available.

### Safe exit during scanning

When the user chooses to exit during a disk-space scan, the controller waits for the scan to finish before closing the application.

**Reason:** The application avoids leaving the scan workflow in an undefined state.

### Separate backup and scan controls

The backup worker's cancellation/resume/exit events are separate from the disk-space scan cancellation event.

**Reason:** These are different operations and must not accidentally control one another.

## Additional implementation notes

- Keep date-handling behavior unchanged unless a separate requirement calls for a change.
- Preserve working behavior when making isolated GUI or documentation changes.
- History cleanup order is safety-critical. Remove only snapshots identified as eligible for retention cleanup.
- User-facing errors should explain a corrective action where possible; avoid telling non-technical users to inspect the console.

## Verification records

The earlier BackupProject 1.1 baseline had 21 passing automated tests. This is historical information and must not be presented as proof that every BackupProject 1.3 workflow has passed testing.
