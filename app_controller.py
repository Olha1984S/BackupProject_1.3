from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
import tkinter as tk
import threading
import queue
from pathlib import Path
from datetime import datetime

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    MAX_SCALE,
    WINDOW_BORDER_WIDTH,
    BUTTON_PRIMARY,
    BUTTON_STATE_DISABLED,
    center_window,
    set_button_state,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
GUI_DIR = BASE_DIR / "gui"

# Persistent configuration
LOCAL_APP_DATA = Path(
    os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
)
CONFIG_DIR = LOCAL_APP_DATA / "BackupManager"
CONFIG_FILE = CONFIG_DIR / "config.json"

WINDOW_1_FILE = GUI_DIR / "1_backup_manager_start_integrated.py"
WINDOW_2_FILE = GUI_DIR / "2_0_backup_manager_first_launch_choice_of_paths_integrated.py"
WINDOW_2_1_FILE = GUI_DIR / "2_1_backup_manager_error_path.py"
WINDOW_3_FILE = GUI_DIR / "3_backup_manager_select_the_number_of_copies_to_keep_integrated.py"
WINDOW_4_1_FILE = GUI_DIR / "4_1_backup_manager_how_often_should_backup_manager_run_integrated.py"
WINDOW_4_2_FILE = GUI_DIR / "4_2_backup_manager_how_often_should_backup_manager_run_integrated.py"
WINDOW_5_1_FILE = GUI_DIR / "5_1_backup_manager_first_backup_date_integrated.py"
WINDOW_5_2_FILE = GUI_DIR / "5_2_backup_manager_first_backup_date_integrated.py"
WINDOW_6_1_FILE = GUI_DIR / "6_1_backup_manager_first_backup_time_integrated.py"
WINDOW_6_2_FILE = GUI_DIR / "6_2_backup_manager_first_backup_time_integrated.py"
WINDOW_6_2_SET_ONLY_FILE = (
    GUI_DIR / "6_2_set_only_backup_manager_first_backup_time_integrated.py"
)
WINDOW_6_3_FILE = GUI_DIR / "6_3_backup_manager_time_error.py"
WINDOW_7_1_FILE = GUI_DIR / "7_1_backup_manager_completing_setup_start_integrated.py"
WINDOW_7_2_FILE = GUI_DIR / "7_2_backup_manager_completing_setup_save_and_exit_integrated.py"
WINDOW_7_3_FILE = GUI_DIR / "7_3_backup_manager_error_the_timeout_period_has_expired.py"
WINDOW_7_4_FILE = GUI_DIR / "7_4_backup_manager_save_and_exit.py"
WINDOW_8_FILE = GUI_DIR / "8_backup_manager_the_main_window_after_setup_integrated.py"
WINDOW_9_FILE = GUI_DIR / "9_0_backup_manager_settings_window_or_start_now_integrated.py"
WINDOW_9_1_FILE = GUI_DIR / "9_1_backup_manager_attention_creating_an_unscheduled_backup_integrated.py"
WINDOW_10_FILE = GUI_DIR / "10_backup_manager_backup_in_progress_integrated.py"
WINDOW_11_FILE = GUI_DIR / "11_backup_manager_stopping_updated_integrated.py"
WINDOW_12_FILE = GUI_DIR / "12_backup_manager_successful_backup_integrated.py"
WINDOW_13_FILE = GUI_DIR / "13_backup_manager_error_integrated.py"
WINDOW_14_FILE = GUI_DIR / "14_backup_manager_not_enough_free_disk_space.py"


if str(GUI_DIR) not in sys.path:
    sys.path.insert(0, str(GUI_DIR))

import backup_manager


# ============================================================
# MODULE LOADER
# ============================================================

def load_class_from_file(file_path: Path, module_name: str, class_name: str):
    """Load a GUI class from a Python file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"GUI file was not found:\n{file_path}"
        )

    spec = importlib.util.spec_from_file_location(
        module_name,
        file_path,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Cannot load GUI file:\n{file_path}"
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return getattr(module, class_name)


# ============================================================
# LOAD GUI CLASSES
# ============================================================

BackupManagerStartWindow = load_class_from_file(
    WINDOW_1_FILE,
    "window_1_module",
    "BackupManagerStartWindow",
)

ChoiceOfPathsScreen = load_class_from_file(
    WINDOW_2_FILE,
    "window_2_module",
    "ChoiceOfPathsScreen",
)

ErrorPathWindow = load_class_from_file(
    WINDOW_2_1_FILE,
    "window_2_1_module",
    "ErrorPathWindow",
)

CopiesToKeepWindow = load_class_from_file(
    WINDOW_3_FILE,
    "window_3_module",
    "CopiesToKeepWindow",
)

BackupFrequencyWindow = load_class_from_file(
    WINDOW_4_1_FILE,
    "window_4_1_module",
    "BackupFrequencyWindow",
)

CustomIntervalWindow = load_class_from_file(
    WINDOW_4_2_FILE,
    "window_4_2_module",
    "CustomIntervalWindow",
)

FirstBackupDateWindow = load_class_from_file(
    WINDOW_5_1_FILE,
    "window_5_1_module",
    "FirstBackupDateWindow",
)

FirstBackupDateCalendarWindow = load_class_from_file(
    WINDOW_5_2_FILE,
    "window_5_2_module",
    "FirstBackupDateCalendarWindow",
)

FirstBackupTimeWindow = load_class_from_file(
    WINDOW_6_1_FILE,
    "window_6_1_module",
    "FirstBackupTimeWindow",
)

TimePickerWindow = load_class_from_file(
    WINDOW_6_2_FILE,
    "window_6_2_module",
    "FirstBackupTimeWindow",
)

SetOnlyTimePickerWindow = load_class_from_file(
    WINDOW_6_2_SET_ONLY_FILE,
    "window_6_2_set_only_module",
    "FirstBackupTimeWindow",
)

TimeErrorWindow = load_class_from_file(
    WINDOW_6_3_FILE,
    "window_6_3_module",
    "ErrorPathWindow",
)

CompletingSetupStartWindow = load_class_from_file(
    WINDOW_7_1_FILE,
    "window_7_1_module",
    "CompletingSetupWindow",
)

CompletingSetupSaveExitWindow = load_class_from_file(
    WINDOW_7_2_FILE,
    "window_7_2_module",
    "CompletingSetupWindow",
)

TimeoutWarningWindow = load_class_from_file(
    WINDOW_7_3_FILE,
    "window_7_3_module",
    "TimeoutWarningWindow",
)

SaveAndExitWindow = load_class_from_file(
    WINDOW_7_4_FILE,
    "window_7_4_module",
    "SaveAndExitWindow",
)

BackupManagerMainWindow = load_class_from_file(
    WINDOW_8_FILE,
    "window_8_module",
    "BackupManagerMainWindow",
)

BackupManagerSettingsWindow = load_class_from_file(
    WINDOW_9_FILE,
    "window_9_module",
    "BackupManagerSettingsWindow",
)

UnscheduledBackupWarningWindow = load_class_from_file(
    WINDOW_9_1_FILE,
    "window_9_1_module",
    "UnscheduledBackupWarningWindow",
)

BackupInProgressWindow = load_class_from_file(
    WINDOW_10_FILE,
    "window_10_module",
    "BackupInProgressWindow",
)

StoppingWindow = load_class_from_file(
    WINDOW_11_FILE,
    "window_11_module",
    "StoppingWindow",
)

CompletingBackupSuccessWindow = load_class_from_file(
    WINDOW_12_FILE,
    "window_12_module",
    "CompletingSetupWindow",
)

BackupErrorWindow = load_class_from_file(
    WINDOW_13_FILE,
    "window_13_module",
    "ErrorWindow",
)

NotEnoughFreeDiskSpaceWindow = load_class_from_file(
    WINDOW_14_FILE,
    "window_14_module",
    "NotEnoughFreeDiskSpaceWindow",
)


# ============================================================
# APPLICATION CONTROLLER
# ============================================================

class BackupManagerApp:
    """
    Main controller for BackupProject_1.3.

    Architecture:
        ONE Tk root
        ONE shared Canvas
        ONE active GUI Block at a time

    app_controller_5.py remains the control version.
    This file is the next development checkpoint:
        app_controller_7.py
    """

    def __init__(self):
        # ----------------------------------------------------
        # ONE Tk root
        # ----------------------------------------------------
        self.root = tk.Tk()
        self.root.withdraw()

        self.root.title("Backup Manager")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)

        # ----------------------------------------------------
        # Application state
        # ----------------------------------------------------
        self.state = {
            "source_path": "",
            "backup_path": "",
            "copies_to_keep": "",
            "backup_frequency": "1 day",
            "custom_interval_days": "",

            # Remembers whether Window 5.1 was opened
            # from Window 4.1 or Window 4.2.
            "frequency_screen": "frequency",

            # Selected first backup date.
            "first_backup_date": "",
            "first_backup_time": "",
            "first_backup_start_mode": "",
            "first_backup_actual_start": "",

            # Time-picker routing state.
            # Normal route: 6.1 -> 6.2 -> 7.2
            # Future-date route: 5.2 -> 6.2_set_only -> 7.2
            "time_picker_return_screen": "window6",
            "time_picker_screen": "window6_2",

            "backup_start_requested": False,
            "save_and_exit_requested": False,
            "setup_completed": False,
            "main_start_requested": False,
            "backup_error_file": None,
            "backup_error_reason": "",
            "backup_error_critical": False,
        }

        # Load persisted settings before selecting the startup screen.
        self._load_state()

        # ----------------------------------------------------
        # Scale
        # ----------------------------------------------------
        self.scale = MAX_SCALE

        self.window_width = round(
            DESIGN_WIDTH * self.scale
        )
        self.window_height = round(
            DESIGN_HEIGHT * self.scale
        )

        center_window(
            self.root,
            self.window_width,
            self.window_height,
        )

        # ----------------------------------------------------
        # ONE shared Canvas
        # ----------------------------------------------------
        self.canvas = tk.Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack()

        self.current_block = None
        self.backup_queue = queue.Queue()
        self.backup_cancel_event = threading.Event()
        self.backup_resume_event = threading.Event()
        self.backup_exit_event = threading.Event()
        self.stop_window_ready = False
        self.exit_after_stop = False
        self.backup_result_status = None
        self.show_progress_without_worker = False
        self.backup_thread = None
        self.backup_run_id = 0
        self.current_screen = None
        self.disk_check_in_progress = False
        self.disk_check_thread = None
        self.disk_check_cancel_event = threading.Event()
        self.disk_check_cancel_requested = False
        self.disk_check_was_cancelled = False

        self._draw_application_frame()

        # First run (or incomplete setup) starts at Window 1.
        # Completed setup opens the main Window 8.
        startup_screen = (
            "main" if self.state.get("setup_completed") else "start"
        )
        self.show_screen(startup_screen)

        self.root.update_idletasks()
        self.root.deiconify()

    # ========================================================
    # CONFIGURATION PERSISTENCE
    # ========================================================

    _PERSISTED_KEYS = (
        "source_path",
        "backup_path",
        "copies_to_keep",
        "backup_frequency",
        "custom_interval_days",
        "frequency_screen",
        "first_backup_date",
        "first_backup_time",
        "first_backup_start_mode",
        "first_backup_actual_start",
        "setup_completed",
    )

    def _load_state(self):
        """Load saved settings; missing or invalid files are treated as first run."""
        try:
            with CONFIG_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                return False
            for key in self._PERSISTED_KEYS:
                if key in data:
                    self.state[key] = data[key]
            self.state["setup_completed"] = (
                data.get("setup_completed") is True
            )
            return True
        except (OSError, json.JSONDecodeError):
            return False

    def _save_state(self):
        """Save the current user settings to config.json."""

        data = {
            key: self.state.get(key, "")
            for key in self._PERSISTED_KEYS
        }

        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            # Write to a temporary file first so an interrupted write does
            # not leave a partially written configuration file.
            temp_file = CONFIG_FILE.with_suffix(".tmp")
            with temp_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            temp_file.replace(CONFIG_FILE)
            print(f"Configuration saved to: {CONFIG_FILE}")
            return True

        except OSError as exc:
            print(f"Could not save configuration: {exc}")
            return False

    # ========================================================
    # APPLICATION FRAME
    # ========================================================

    def _draw_application_frame(self):
        """Draw the common frame of the single application window."""

        border_width = max(
            1,
            round(WINDOW_BORDER_WIDTH * self.scale),
        )

        self.canvas.create_rectangle(
            border_width / 2,
            border_width / 2,
            self.window_width - border_width / 2,
            self.window_height - border_width / 2,
            fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=border_width,
            tags=("application_frame",),
        )

    # ========================================================
    # SCREEN NAVIGATION
    # ========================================================

    def show_screen(self, screen_name):
        """
        Switch the GUI Block inside the SAME Canvas.

        The root window and Canvas are never recreated.

        Special routing:
            5.2 -> show_screen("window6")
        is converted here into either:
            6.1             when the selected date is Today
            6.2_set_only    when the selected date is another date
        """

        # ----------------------------------------------------
        # FINAL ROUTING FROM WINDOW 5.2
        #
        # The current Window 5.2 GUI calls show_screen("window6")
        # directly. We must not allow that call to create Window 6.1
        # for a future date.
        # ----------------------------------------------------
        if (
            screen_name == "window6"
            and self.current_screen == "first_backup_calendar"
        ):
            selected_date = self._parse_controller_date(
                self.state.get("first_backup_date", "")
            )
            today = datetime.now().date()

            if (
                selected_date is not None
                and selected_date.date() != today
            ):
                self.state["time_picker_return_screen"] = "first_backup_date"
                self.state["time_picker_screen"] = "window6_2_set_only"
                screen_name = "window6_2_set_only"
            else:
                self.state["time_picker_return_screen"] = "window6"
                self.state["time_picker_screen"] = "window6_2"

        # ----------------------------------------------------
        # Remember where Window 5.1 was opened from.
        # ----------------------------------------------------
        if screen_name == "window5":
            if self.current_screen in (
                "frequency",
                "custom_interval",
            ):
                self.state["frequency_screen"] = self.current_screen

        # ----------------------------------------------------
        # Save Window 4.2 input before leaving the screen.
        #
        # This is important when the user:
        #
        # 4.1 -> 4.2 -> enters 10 -> 4.1 -> 4.2
        #
        # The value must remain in the field when 4.2 is opened
        # again. The value is stored in controller.state.
        # ----------------------------------------------------
        if self.current_screen == "custom_interval":
            current_entry = getattr(
                self.current_block,
                "interval_entry",
                None,
            )

            if current_entry is not None:
                self.state["custom_interval_days"] = (
                    current_entry.get().strip()
                )

        # ----------------------------------------------------
        # Destroy previous block.
        # ----------------------------------------------------
        self.clear_current_block()

        self.current_screen = screen_name

        # ----------------------------------------------------
        # WINDOW 1
        # ----------------------------------------------------
        if screen_name == "start":
            self.current_block = BackupManagerStartWindow(
                root=self.root,
                on_exit=self.exit_application,
                on_install=lambda: self.show_screen("paths"),
                parent=self.canvas,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 8 — MAIN WINDOW AFTER INITIAL SETUP
        # ----------------------------------------------------
        if screen_name == "main":
            self.current_block = BackupManagerMainWindow(
                root=self.root,
                on_exit=self.exit_application,
                on_start=self.start_from_window_8,
                parent=self.canvas,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 9 — SAVED SETTINGS / START NOW
        # ----------------------------------------------------
        if screen_name == "settings_overview":
            self.current_block = BackupManagerSettingsWindow(
                root=self.root,
                source=self.state.get("source_path", ""),
                backup_location=self.state.get("backup_path", ""),
                copies=str(self.state.get("copies_to_keep", "")),
                frequency=self._frequency_display(),
                first_backup=self._next_backup_display(),
                on_settings=lambda: self.show_screen("paths"),
                on_start_now=self.start_backup_from_window_9,
                parent=self.canvas,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 9_1 — UNSCHEDULED BACKUP WARNING
        # ----------------------------------------------------
        if screen_name == "unscheduled_backup_warning":
            self.current_block = UnscheduledBackupWarningWindow(
                root=self.root,
                on_exit=self.exit_application,
                on_back=lambda: self.show_screen("settings_overview"),
                on_start=self.confirm_unscheduled_backup_start,
                parent=self.canvas,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 12 — SUCCESSFUL BACKUP SUMMARY
        # ----------------------------------------------------
        if screen_name == "backup_success":
            self.current_block = CompletingBackupSuccessWindow(
                root=self.root,
                parent=self.canvas,
                scale=self.scale,
                files_copied=self.state.get("last_backup_files_copied", "—"),
                backup_size=self.state.get("last_backup_size", "—"),
                on_action=self.exit_application,
            )
            return

        # ----------------------------------------------------
        # WINDOW 13 — BACKUP ERROR DETAILS
        # ----------------------------------------------------
        if screen_name == "backup_error":
            self.current_block = BackupErrorWindow(
                root=self.root,
                parent=self.canvas,
                scale=self.scale,
                error_file=self.state.get("backup_error_file"),
                reason=self.state.get("backup_error_reason") or
                       "The file may be unavailable or access may be restricted.",
                critical=self.state.get("backup_error_critical", False),
                on_action=self.exit_application,
            )
            return

        # ----------------------------------------------------
        # WINDOW 11 — STOPPING / WAITING FOR SAFE BOUNDARY
        # ----------------------------------------------------
        if screen_name == "stopping":
            self.current_block = StoppingWindow(
                root=self.root,
                parent=self.canvas,
                scale=self.scale,
                on_continue=self.continue_backup_from_window_11,
                on_exit=self.exit_from_window_11,
            )
            return

        # ----------------------------------------------------
        # WINDOW 14 — NOT ENOUGH FREE DISK SPACE
        # ----------------------------------------------------
        if screen_name == "not_enough_disk_space":
            self.current_block = NotEnoughFreeDiskSpaceWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
                required_space=self._format_bytes(
                    self.state.get("required_space_bytes", 0)
                ),
                available_space=self._format_bytes(
                    self.state.get("available_space_bytes", 0)
                ),
                on_exit=self.exit_application,
                on_continue=self.retry_disk_space_check,
            )
            return

        # ----------------------------------------------------
        # WINDOW 10 — BACKUP IN PROGRESS
        # ----------------------------------------------------
        if screen_name == "backup_in_progress":
            if self.show_progress_without_worker:
                self.show_progress_without_worker = False
                final_status = {
                    "success": "Completed",
                    "cancelled": "Stopped",
                    "error": "Error",
                    "file_error": "Error",
                    "low_space": "Not enough free disk space",
                }.get(self.backup_result_status, "Completed")
                self.current_block = BackupInProgressWindow(
                    root=self.root,
                    parent=self.canvas,
                    scale=self.scale,
                    files_copied=0,
                    total_files=0,
                    status=final_status,
                    on_stop=self.stop_backup_from_window_10,
                )
                return
            initial_status = (
                "Checking free space"
                if self.disk_check_in_progress
                else "Preparing"
            )
            self.current_block = BackupInProgressWindow(
                root=self.root,
                parent=self.canvas,
                scale=self.scale,
                files_copied=0,
                total_files=0,
                status=initial_status,
                on_stop=self.stop_backup_from_window_10,
            )
            # The disk-space check runs separately. Do not start copying
            # until its result has been handled on the Tk main thread.
            if not self.disk_check_in_progress:
                self._start_backup_worker()
            return

        # ----------------------------------------------------
        # WINDOW 2
        # ----------------------------------------------------
        if screen_name == "paths":
            self.current_block = ChoiceOfPathsScreen(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 3
        # ----------------------------------------------------
        if screen_name == "copies":
            self.current_block = CopiesToKeepWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 4.1
        #
        # Next is always active.
        # ----------------------------------------------------
        if screen_name == "frequency":
            self.current_block = BackupFrequencyWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 4.2
        #
        # Next must be disabled until a positive number
        # is entered into the days field.
        # ----------------------------------------------------
        if screen_name == "custom_interval":
            self.current_block = CustomIntervalWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )

            self._setup_window_4_2_next_state()
            return

        # ----------------------------------------------------
        # WINDOW 5.1
        #
        # Two route names are accepted:
        #
        # "window5"           - entry from 4.1 / 4.2
        # "first_backup_date" - return from 5.2
        # ----------------------------------------------------
        if screen_name in (
            "window5",
            "first_backup_date",
        ):
            self.current_block = FirstBackupDateWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 5.2
        # ----------------------------------------------------
        if screen_name == "first_backup_calendar":
            self.current_block = FirstBackupDateCalendarWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 6.1
        # ----------------------------------------------------
        if screen_name == "window6":
            self.current_block = FirstBackupTimeWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 6.2
        #
        # Normal time picker opened from Window 6.1.
        # ----------------------------------------------------
        if screen_name == "window6_2":
            self.current_block = TimePickerWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 6.2 — SET ONLY
        #
        # Used when a future date was selected in Window 5.2.
        # This block contains only "Set start time".
        # ----------------------------------------------------
        if screen_name == "window6_2_set_only":
            self.current_block = SetOnlyTimePickerWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
            )
            return

        # ----------------------------------------------------
        # WINDOW 7.1 — START AFTER COMPLETING SETTINGS
        # ----------------------------------------------------
        if screen_name == "window7_1":
            self.current_block = CompletingSetupStartWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
                source=self.state.get("source_path", ""),
                backup_location=self.state.get("backup_path", ""),
                copies=self.state.get("copies_to_keep", ""),
                frequency=self._frequency_display(),
                first_backup=self._first_backup_display(),
                on_back=self.back_from_window_7_1,
                on_action=self.start_backup_from_window_7_1,
            )
            return

        # ----------------------------------------------------
        # WINDOW 7.2 — SCHEDULED START / SAVE AND EXIT
        # ----------------------------------------------------
        if screen_name == "window7_2":
            self.current_block = CompletingSetupSaveExitWindow(
                parent=self.canvas,
                controller=self,
                scale=self.scale,
                source=self.state.get("source_path", ""),
                backup_location=self.state.get("backup_path", ""),
                copies=self.state.get("copies_to_keep", ""),
                frequency=self._frequency_display(),
                first_backup=self._first_backup_display(),
                scheduled_datetime=self._scheduled_datetime(),
                on_back=self.back_from_window_7_2,
                on_action=self.save_and_exit_from_window_7_2,
                on_timeout=self.show_window_7_3,
            )
            return

        # ----------------------------------------------------
        # WINDOW 7.4 — SETTINGS SAVED / BACK OR EXIT
        # ----------------------------------------------------
        if screen_name == "window7_4":
            scheduled = self._scheduled_datetime()
            scheduled_text = ""
            if scheduled is not None:
                scheduled_text = (
                    "Scheduled program launch: "
                    + scheduled.strftime("%B %d, %Y, at %H:%M")
                )

            self.current_block = SaveAndExitWindow(
                root=self.root,
                on_exit=self.exit_application,
                on_back=self.back_from_window_7_4,
                parent=self.canvas,
                scale=self.scale,
                scheduled_launch_text=scheduled_text,
            )
            return

        raise ValueError(
            f"Unknown screen: {screen_name!r}"
        )

    # ========================================================
    # WINDOW 4.2 — NEXT BUTTON STATE
    # ========================================================

    def _setup_window_4_2_next_state(self):
        """
        Configure Window 4.2 Next button.

        Initial state:
            disabled

        Enabled when:
            a positive whole number is entered

        Disabled when:
            field is empty
            or value is 0
        """

        entry = getattr(
            self.current_block,
            "interval_entry",
            None,
        )

        if entry is None:
            return

        # Listen to every change made in the input field.
        entry.bind(
            "<KeyRelease>",
            self._on_window_4_2_input_changed,
            add="+",
        )

        # Set the correct initial state immediately.
        self._update_window_4_2_next_state()

    def _on_window_4_2_input_changed(self, _event=None):
        """Update Window 4.2 Next after input changes."""

        self._update_window_4_2_next_state()

    def _update_window_4_2_next_state(self):
        """
        Enable Next only when the input contains a
        positive whole number.
        """

        if self.current_screen != "custom_interval":
            return

        entry = getattr(
            self.current_block,
            "interval_entry",
            None,
        )

        if entry is None:
            return

        value = entry.get().strip()

        try:
            enabled = bool(value) and int(value) >= 1
        except ValueError:
            enabled = False

        button_ids = self.canvas.find_withtag(
            "window4_2_nav_Next"
        )

        if len(button_ids) < 2:
            return

        state = "normal" if enabled else BUTTON_STATE_DISABLED

        set_button_state(
            self.canvas,
            button_ids[0],
            button_ids[1],
            BUTTON_PRIMARY,
            state,
            self.scale,
        )

    # ========================================================
    # WINDOW 5 NAVIGATION
    # ========================================================

    def open_first_backup_date_calendar(self):
        """5.1 -> 5.2."""

        self.show_screen("first_backup_calendar")

    def return_to_first_backup_date(self):
        """5.2 -> 5.1."""

        self.show_screen("first_backup_date")

    def back_from_window_5(self):
        """
        5.1 -> the original Window 4 screen.
        """

        previous_screen = self.state.get(
            "frequency_screen",
            "frequency",
        )

        if previous_screen not in (
            "frequency",
            "custom_interval",
        ):
            previous_screen = "frequency"

        self.show_screen(previous_screen)

    def next_from_window_5(self, selected_date):
        """
        Final Window 5 -> Window 6 routing.

        Today:
            5.1 / 5.2 -> 6.1

        Another date:
            5.2 -> 6.2_set_only

        The set-only picker is a separate GUI block because
        "Start after completing the settings" is not available
        for a future date.
        """

        self.state["first_backup_date"] = selected_date

        selected_datetime = self._parse_controller_date(selected_date)
        today = datetime.now().date()

        # A date other than Today:
        # skip Window 6.1 completely.
        if (
            selected_datetime is not None
            and selected_datetime.date() != today
        ):
            self.state["time_picker_return_screen"] = "first_backup_date"
            self.state["time_picker_screen"] = "window6_2_set_only"
            self.show_screen("window6_2_set_only")
            return

        # Today:
        # show Window 6.1, where the user chooses Start now or Set time.
        self.state["time_picker_return_screen"] = "window6"
        self.state["time_picker_screen"] = "window6_2"
        self.show_screen("window6")

    # ========================================================
    # WINDOW 6 NAVIGATION
    # ========================================================

    def open_window_6_2(self):
        """
        6.1 -> normal 6.2.
        """

        self.state["time_picker_return_screen"] = "window6"
        self.state["time_picker_screen"] = "window6_2"
        self.show_screen("window6_2")

    def open_window_6_2_set_only(self):
        """
        5.2 -> dedicated 6.2_set_only.
        """

        self.state["time_picker_return_screen"] = "first_backup_date"
        self.state["time_picker_screen"] = "window6_2_set_only"
        self.show_screen("window6_2_set_only")

    def return_to_window_6_1(self):
        """
        Back button from Window 6.

        The Back button in all Window 6 variants always returns
        to Window 5.1. It never switches between 6.1 and 6.2.
        The method name is kept for compatibility with the existing
        Window 6 GUI files.
        """

        self.show_screen("first_backup_date")

    def back_from_window_6_1(self):
        self.show_screen("first_backup_date")

    def next_from_window_6_1(self, selected_option):
        """
        6.1:
            Start after completing the settings -> 7.1
            Set start time -> 6.2
        """

        self.state["first_backup_start_mode"] = selected_option

        if selected_option == "Set start time":
            self.open_window_6_2()
        else:
            self.show_screen("window7_1")

    def next_from_window_6_2(self, selected_time):
        self.state["first_backup_time"] = selected_time

        selected_date = self.state.get("first_backup_date", "")
        parsed_date = self._parse_controller_date(selected_date)

        if parsed_date is not None:
            now = datetime.now()

            if parsed_date.date() == now.date():
                try:
                    hour, minute = map(int, selected_time.split(":"))
                    selected_datetime = datetime(
                        parsed_date.year,
                        parsed_date.month,
                        parsed_date.day,
                        hour,
                        minute,
                    )

                    if selected_datetime < now:
                        self.show_window_6_3()
                        return
                except (ValueError, TypeError):
                    pass

        self.state["first_backup_start_mode"] = "Set start time"
        self.show_screen("window7_2")

    @staticmethod
    def _parse_controller_date(value):
        if not value:
            return None

        value = str(value).strip()

        for fmt in (
            "%d.%m.%Y",
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%m/%d/%Y",
        ):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    def show_window_6_3(self):
        def return_to_time_picker():
            self.show_screen("window6_2")

        TimeErrorWindow(
            self.root,
            title="Ensure the timing is correct",
            message=None,
            on_ok=return_to_time_picker,
        )

    # ========================================================
    # WINDOW 7 ACTIONS
    # ========================================================

    def _frequency_display(self):
        frequency = self.state.get("backup_frequency", "")
        custom = self.state.get("custom_interval_days", "")
        if frequency == "Custom interval" and custom:
            return f"Every {custom} day(s)"
        return frequency

    def _first_backup_display(self):
        mode = self.state.get("first_backup_start_mode", "")
        date = self.state.get("first_backup_date", "")
        time = self.state.get("first_backup_time", "")
        if mode == "Start after completing the settings":
            return "After completing the settings"
        if date and time:
            return f"{date} {time}"
        return date or time or ""

    def _backup_interval_delta(self, start):
        """Return the next scheduled datetime based on the configured interval."""
        frequency = self.state.get("backup_frequency", "1 day")
        if frequency == "1 day":
            from datetime import timedelta
            return start + timedelta(days=1)
        if frequency == "1 week":
            from datetime import timedelta
            return start + timedelta(weeks=1)
        if frequency == "1 month":
            # Advance one calendar month, clamping the day to that month's length.
            import calendar
            year = start.year + (1 if start.month == 12 else 0)
            month = 1 if start.month == 12 else start.month + 1
            day = min(start.day, calendar.monthrange(year, month)[1])
            return start.replace(year=year, month=month, day=day)
        if frequency == "Custom interval":
            from datetime import timedelta
            try:
                days = max(1, int(self.state.get("custom_interval_days", 1)))
            except (TypeError, ValueError):
                days = 1
            return start + timedelta(days=days)
        return None

    def _next_backup_display(self):
        """Build Window 9's Next backup value from the saved schedule."""
        mode = self.state.get("first_backup_start_mode", "")
        actual_start_raw = self.state.get("first_backup_actual_start", "")
        start = None

        if actual_start_raw:
            try:
                start = datetime.fromisoformat(actual_start_raw)
            except (TypeError, ValueError):
                start = None

        if start is None and mode != "Start after completing the settings":
            start = self._scheduled_datetime()

        # Older config.json files do not contain the actual start timestamp.
        # For those files, use the config's last-modified time as a fallback estimate.
        if start is None and mode == "Start after completing the settings":
            try:
                start = datetime.fromtimestamp(CONFIG_FILE.stat().st_mtime)
            except OSError:
                return "Not available"

        if start is None:
            return "Not configured"

        now = datetime.now()
        next_start = self._backup_interval_delta(start)
        if next_start is None:
            return "Not configured"

        # If a configured first run is still in the future, show that first run.
        if not actual_start_raw and start > now:
            next_start = start
        # If a saved scheduled date is already past and there is no actual-start
        # timestamp, advance it by intervals until the next occurrence is future.
        elif not actual_start_raw and mode != "Start after completing the settings":
            while next_start <= now:
                advanced = self._backup_interval_delta(next_start)
                if advanced is None or advanced <= next_start:
                    break
                next_start = advanced

        return next_start.strftime("%d.%m.%Y %H:%M")

    def _scheduled_datetime(self):
        date = self._parse_controller_date(self.state.get("first_backup_date", ""))
        time = self.state.get("first_backup_time", "")
        if date is None or not time:
            return None
        try:
            hour, minute = map(int, time.split(":"))
            return datetime(date.year, date.month, date.day, hour, minute)
        except (ValueError, TypeError):
            return None

    def back_from_window_7_1(self):
        self.show_screen("window6")

    def back_from_window_7_2(self):
        """
        Return from Window 7.2 to the time picker that opened it.

        Normal route:
            7.2 -> 6.2

        Future-date route:
            7.2 -> 6.2_set_only
        """

        return_screen = self.state.get(
            "time_picker_screen",
            "window6_2",
        )

        if return_screen not in (
            "window6_2",
            "window6_2_set_only",
        ):
            return_screen = "window6_2"

        self.show_screen(return_screen)

    @staticmethod
    def _format_bytes(value):
        """Format a byte count for display in Window 14."""
        try:
            value = float(value)
        except (TypeError, ValueError):
            return str(value)

        units = ("B", "KB", "MB", "GB", "TB")
        for unit in units:
            if value < 1024 or unit == units[-1]:
                return f"{value:,.1f} {unit}"
            value /= 1024
        return f"{value:,.1f} TB"

    @staticmethod
    def _directory_size(directory, cancel_event=None):
        """Return directory size, allowing a long scan to be cancelled safely."""
        total = 0
        for item in Path(directory).rglob("*"):
            # Cooperative cancellation: stop between filesystem entries. A
            # single filesystem call already in progress is allowed to finish.
            if cancel_event is not None and cancel_event.is_set():
                return None
            try:
                if item.is_file():
                    total += item.stat().st_size
            except OSError:
                # Do not underestimate required space if a file cannot be read.
                raise
        return total

    def _check_disk_space(self, cancel_event=None):
        """Check destination space before writes; return 'cancelled' if stopped."""
        source_value = self.state.get("source_path", "")
        backup_value = self.state.get("backup_path", "")

        if not source_value or not backup_value:
            print("Disk-space check failed: source path or backup path is empty.")
            return None

        source_path = Path(source_value)
        backup_path = Path(backup_value)

        if not source_path.is_dir():
            print(f"Disk-space check failed: source folder does not exist: {source_path}")
            return None

        if not backup_path.is_dir():
            print(
                "Disk-space check failed: backup destination does not exist: "
                f"{backup_path}"
            )
            return None

        current_path = backup_path / "Current"
        try:
            source_size = self._directory_size(source_path, cancel_event)
            if source_size is None or (cancel_event is not None and cancel_event.is_set()):
                return "cancelled"
            current_size = (
                self._directory_size(current_path, cancel_event)
                if current_path.is_dir() else 0
            )
            if current_size is None or (cancel_event is not None and cancel_event.is_set()):
                return "cancelled"
            required_space = source_size + current_size
            available_space = shutil.disk_usage(backup_path).free
            if cancel_event is not None and cancel_event.is_set():
                return "cancelled"
        except OSError as exc:
            print(f"Disk-space check failed: {exc}")
            return None

        self.state["required_space_bytes"] = required_space
        self.state["available_space_bytes"] = available_space
        print(
            "Disk-space check: "
            f"required={self._format_bytes(required_space)}, "
            f"available={self._format_bytes(available_space)}, "
            f"destination={backup_path}"
        )
        return available_space >= required_space

    def _begin_backup_after_space_check(self):
        """Show Window 10 immediately, then check destination space in a worker."""
        # Prevent repeated clicks from starting duplicate checks or backups.
        if self.disk_check_in_progress or (
            self.backup_thread and self.backup_thread.is_alive()
        ):
            return

        self.disk_check_cancel_event.clear()
        self.disk_check_cancel_requested = False
        self.disk_check_was_cancelled = False
        self.disk_check_in_progress = True
        self.show_screen("backup_in_progress")

        def check_worker():
            try:
                result = self._check_disk_space(self.disk_check_cancel_event)
            except Exception as exc:
                print(f"Disk-space check failed unexpectedly: {exc!r}")
                result = None
            try:
                self.root.after(0, lambda result=result: self._finish_disk_space_check(result))
            except tk.TclError:
                pass

        self.disk_check_thread = threading.Thread(
            target=check_worker, daemon=True
        )
        self.disk_check_thread.start()

    def _finish_disk_space_check(self, enough_space):
        """Handle the disk-space result on Tk's main thread."""
        self.disk_check_in_progress = False
        self.disk_check_thread = None

        if enough_space == "cancelled" or self.disk_check_cancel_requested:
            self.disk_check_cancel_requested = False
            self.disk_check_was_cancelled = True
            # Window 11 remains visible. Enable its Continue/Exit actions only
            # after the scanner has actually stopped.
            if self.exit_after_stop:
                self.disk_check_was_cancelled = False
                self.exit_application()
                return
            if (self.current_screen == "stopping" and self.current_block
                    and hasattr(self.current_block, "operation_completed")):
                self.current_block.operation_completed()
            return

        if enough_space is None:
            self.state["backup_error_file"] = None
            self.state["backup_error_reason"] = (
                "The program could not check the available disk space. "
                "Check that the source and backup locations are accessible, then try again."
            )
            self.state["backup_error_critical"] = True
            self.show_screen("backup_error")
            return

        if not enough_space:
            self.show_screen("not_enough_disk_space")
            return

        if self.state.get("pending_setup_completion"):
            self.state["setup_completed"] = True
            self.state["first_backup_actual_start"] = (
                datetime.now().replace(microsecond=0).isoformat()
            )
            self.state["pending_setup_completion"] = False

        self.state["backup_start_requested"] = True
        self._save_state()

        # Keep Window 10 visible and change from the checking phase to copying.
        if self.current_block and hasattr(self.current_block, "update_progress"):
            self.current_block.update_progress(
                files_copied=0, total_files=0, status="Preparing"
            )
        self._start_backup_worker()

    def retry_disk_space_check(self):
        """Window 14 Continue: show Window 10 and repeat the check."""
        self._begin_backup_after_space_check()

    def start_backup_from_window_7_1(self):
        # First backup requested after completing the setup.
        self.state["pending_setup_completion"] = True
        self._begin_backup_after_space_check()

    def save_and_exit_from_window_7_2(self):
        """Save setup settings, then open Window 7.4 without closing the app."""

        self.state["save_and_exit_requested"] = True
        self.state["setup_completed"] = True

        if not self._save_state():
            return

        self.show_screen("window7_4")

    def back_from_window_7_4(self):
        """Return to Window 7.2 without closing the application."""
        self.show_screen("window7_2")

    def start_from_window_8(self):
        """Open Window 9 and display the saved configuration."""
        self.state["main_start_requested"] = True
        self.show_screen("settings_overview")

    def start_backup_from_window_9(self):
        """Open the warning before an unscheduled backup is started."""
        self.show_screen("unscheduled_backup_warning")

    def confirm_unscheduled_backup_start(self):
        """Check free space before opening Window 10 for an unscheduled backup."""
        self.state["pending_setup_completion"] = False
        self._begin_backup_after_space_check()

    def stop_backup_from_window_10(self):
        """Cancel the read-only space scan or request a safe stop during copying."""
        if self.disk_check_in_progress:
            self.disk_check_cancel_requested = True
            self.disk_check_cancel_event.set()
            self.stop_window_ready = False
            self.exit_after_stop = False
            self.show_screen("stopping")
            print("Stop requested during disk-space check.")
            return

        if self.backup_thread and self.backup_thread.is_alive():
            self.stop_window_ready = False
            self.exit_after_stop = False
            # Clear any stale decision from an earlier stop request before
            # asking the worker to pause at the next safe checkpoint.
            self.backup_resume_event.clear()
            self.backup_exit_event.clear()
            self.backup_cancel_event.set()
            self.show_screen("stopping")
            print("Stop requested. Waiting for a safe operation boundary.")
        else:
            print("No backup operation is running.")

    def continue_backup_from_window_11(self):
        """Resume backup, or restart a cancelled disk-space scan from the beginning."""
        if self.disk_check_in_progress and self.disk_check_cancel_requested:
            # Do not run a second scan alongside the first. Let the current
            # scan observe cancellation, then Continue will start a fresh scan.
            return

        if self.disk_check_was_cancelled:
            self.disk_check_was_cancelled = False
            self.backup_result_status = None
            self._begin_backup_after_space_check()
            return

        if self.backup_result_status is not None:
            self.show_progress_without_worker = True
            self.show_screen("backup_in_progress")
            return
        # Always signal resume before returning to Window 10. This covers both
        # cases: the worker is already waiting at the safe boundary, or it has
        # not reached that boundary yet (the pending stop is cancelled).
        self.backup_cancel_event.clear()
        self.backup_resume_event.set()
        self.stop_window_ready = False
        self.show_screen("backup_in_progress")

    def exit_from_window_11(self):
        """Exit only after a disk scan or backup worker has safely stopped."""
        if self.disk_check_in_progress:
            self.disk_check_cancel_requested = True
            self.disk_check_cancel_event.set()
            self.exit_after_stop = True
            return

        if self.disk_check_was_cancelled:
            self.disk_check_was_cancelled = False
            self.exit_application()
            return

        if self.backup_result_status is not None:
            self.exit_application()
            return
        self.exit_after_stop = True
        self.backup_exit_event.set()
        self.backup_resume_event.set()
        # The worker reports its final result; the queue handler then exits.

    def _start_backup_worker(self):
        """Run file operations off the Tk thread and poll progress on the Tk thread."""
        if self.backup_thread and self.backup_thread.is_alive():
            return
        source_path = self.state.get("source_path", "")
        backup_path = self.state.get("backup_path", "")
        if not source_path or not backup_path:
            print("Backup not started: source or destination path is empty.")
            return
        self.backup_cancel_event = threading.Event()
        self.backup_resume_event = threading.Event()
        self.backup_exit_event = threading.Event()
        self.stop_window_ready = False
        self.exit_after_stop = False
        self.backup_result_status = None
        self.backup_run_id += 1
        run_id = self.backup_run_id

        def report(copied, total, status):
            self.backup_queue.put((run_id, "progress", copied, total, status))

        def worker():
            try:
                result = backup_manager.start_backup(
                    source_path=source_path,
                    backup_path=backup_path,
                    copies_to_keep=self.state.get("copies_to_keep"),
                    progress_callback=report,
                    cancel_event=self.backup_cancel_event,
                    resume_event=self.backup_resume_event,
                    exit_event=self.backup_exit_event,
                )
                if not isinstance(result, dict):
                    result = {
                        "status": "error",
                        "message": "Backup engine returned an invalid result.",
                    }
            except Exception as exc:
                # Do not let a worker exception silently kill queue polling.
                result = {"status": "error", "message": str(exc)}
                print(f"Backup worker exception: {exc!r}")
            self.backup_queue.put((run_id, "result", result))

        self.backup_thread = threading.Thread(target=worker, daemon=True)
        self.backup_thread.start()
        self.root.after(100, self._poll_backup_queue)

    def _poll_backup_queue(self):
        """Apply queued worker updates to Tk widgets only on the main thread."""
        try:
            while True:
                item = self.backup_queue.get_nowait()
                run_id, kind = item[0], item[1]
                if run_id != self.backup_run_id:
                    continue
                if kind == "progress":
                    _, _, copied, total, status = item
                    if status == "StoppingReady":
                        self.stop_window_ready = True
                        if (
                            self.current_screen == "stopping"
                            and self.current_block
                            and hasattr(self.current_block, "operation_completed")
                        ):
                            self.current_block.operation_completed()
                    elif self.current_block and hasattr(self.current_block, "update_progress"):
                        self.current_block.update_progress(copied, total, status)
                elif kind == "result":
                    result = item[2]
                    status = result.get("status", "error")
                    self.backup_result_status = status
                    print(f"Backup result: {result}")

                    if self.exit_after_stop:
                        self.exit_application()
                        return

                    if (
                        self.current_screen == "stopping"
                        and status in ("success", "cancelled")
                    ):
                        self.stop_window_ready = True
                        if self.current_block and hasattr(self.current_block, "operation_completed"):
                            self.current_block.operation_completed()

                    if status == "low_space":
                        self.state["required_space_bytes"] = result.get("required_space", 0)
                        self.state["available_space_bytes"] = result.get("available_space", 0)
                        self.show_screen("not_enough_disk_space")
                    elif status == "success":
                        self.state["last_backup_files_copied"] = result.get(
                            "files_copied", result.get("total_files", "—")
                        )
                        backup_size = result.get("backup_size")
                        if backup_size is None:
                            try:
                                source_dir = Path(self.state.get("source_path", ""))
                                total_bytes = sum(
                                    item.stat().st_size
                                    for item in source_dir.rglob("*")
                                    if item.is_file()
                                )
                                backup_size = self._format_bytes(total_bytes)
                            except (OSError, ValueError, TypeError):
                                backup_size = "—"
                        self.state["last_backup_size"] = backup_size
                        # print("DEBUG: switching to Window 12")
                        self.show_screen("backup_success")
                    elif status == "cancelled":
                        if self.current_block and hasattr(self.current_block, "update_progress"):
                            self.current_block.update_progress(status="Stopped")
                    elif status == "file_error":
                        self.state["backup_error_file"] = result.get("error_file")
                        self.state["backup_error_reason"] = result.get(
                            "reason",
                            "The file may be unavailable or access may be restricted.",
                        )
                        self.state["backup_error_critical"] = False
                        if self.current_block and hasattr(self.current_block, "update_progress"):
                            self.current_block.update_progress(status="Error")
                        self.show_screen("backup_error")
                    else:
                        self.state["backup_error_file"] = None
                        self.state["backup_error_reason"] = result.get("message", "")
                        self.state["backup_error_critical"] = True
                        if self.current_block and hasattr(self.current_block, "update_progress"):
                            self.current_block.update_progress(status="Error")
                        self.show_screen("backup_error")
        except queue.Empty:
            pass
        if self.backup_thread and self.backup_thread.is_alive():
            self.root.after(100, self._poll_backup_queue)

    def show_window_7_3(self):
        def return_to_window_5_1():
            self.show_screen("first_backup_date")

        TimeoutWarningWindow(
            self.root,
            title="The timeout period has expired.",
            message="Change the program's automatic startup time.",
            on_ok=return_to_window_5_1,
        )

    # ========================================================
    # WINDOW 3 CALLBACK
    # ========================================================

    def _next_from_window_3(self, copies):
        """Save copies and open Window 4.1."""

        self.state["copies_to_keep"] = copies
        self.show_screen("frequency")

    def on_window_3_next(self, copies):
        """Compatibility callback for Window 3."""

        self._next_from_window_3(copies)

    # ========================================================
    # CLEAR CURRENT BLOCK
    # ========================================================

    def clear_current_block(self):
        """
        Destroy the current GUI Block.

        The root and shared Canvas remain alive.
        """

        if self.current_block is not None:
            destroy_method = getattr(
                self.current_block,
                "destroy",
                None,
            )

            if callable(destroy_method):
                destroy_method()

            self.current_block = None

        self.canvas.delete("screen_content")

        # Compatibility cleanup for older GUI Blocks.
        self.canvas.delete("window1_content")
        self.canvas.delete("window1_exit_button")
        self.canvas.delete("window1_install_button")
        self.canvas.delete("window3_content")
        self.canvas.delete("window8_content")
        self.canvas.delete("window8_exit_button")
        self.canvas.delete("window8_start_button")
        self.canvas.delete("window9_content")
        self.canvas.delete("window9_settings_button")
        self.canvas.delete("window9_start_now_button")

        # Redraw the common frame.
        self.canvas.delete("application_frame")
        self._draw_application_frame()

    # ========================================================
    # EXIT
    # ========================================================

    def exit_application(self):
        """Save settings and close the application."""

        self._save_state()
        self.clear_current_block()

        if self.root.winfo_exists():
            self.root.destroy()

    # ========================================================
    # RUN
    # ========================================================

    def run(self):
        self.root.mainloop()


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    app = BackupManagerApp()
    app.run()


if __name__ == "__main__":
    main()
