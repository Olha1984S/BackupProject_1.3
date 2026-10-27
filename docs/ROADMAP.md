# Roadmap

This roadmap separates implemented behavior from work that still requires verification or implementation.

## Current implementation to verify

- [x] Single Tkinter root, shared Canvas, and controller-based screen navigation.
- [x] User configuration stored in `%LOCALAPPDATA%\BackupManager\config.json`.
- [x] `Current` and timestamped `History` storage model.
- [x] Disk-space scanning in a background thread.
- [x] Cooperative cancellation of the disk-space scan.
- [x] Restart the space check from the beginning after choosing to continue.
- [x] Wait for an active disk-space scan to finish before exiting.
- [x] Separate screen paths for insufficient space and backup errors.

These checkmarks describe behavior present in the reviewed controller/documentation context. They do not mean every path has been fully regression-tested.

## Before publishing a release

- [ ] Run the current automated test suite in the BackupProject 1.3 environment.
- [ ] Manually test first-time setup and returning-user flows.
- [ ] Verify that settings persist after closing and reopening the application.
- [ ] Test sufficient-space, insufficient-space, and disk-space-check error cases.
- [ ] Test cancellation during a long disk-space scan.
- [ ] Confirm that Continue starts a fresh scan and does not reuse partial results.
- [ ] Confirm that Exit closes only after the scan has finished.
- [ ] Test backup success, backup failure, and the relevant user-facing screens.
- [ ] Verify history retention and cleanup order with multiple timestamped snapshots.
- [ ] Test local, USB, and network destinations in the intended environment.
- [ ] Review logs and user-facing messages for clarity.

## Scheduling

- [ ] Implement and/or verify automatic execution through Windows Task Scheduler.
- [ ] Verify daily, weekly, monthly, and custom-interval scheduling.
- [ ] Confirm behavior when a configured backup date/time is in the past or the destination is unavailable.

## Documentation and maintenance

- [ ] Keep documentation aligned with the current source code.
- [ ] Update this roadmap when a feature is verified or a decision changes.
- [ ] Preserve the known-good version before making changes to backup or history-cleanup logic.
