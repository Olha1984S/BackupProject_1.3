import tkinter as tk

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    CONTENT_WIDTH,
    CONTENT_HEIGHT,
    WINDOW_BORDER_WIDTH,
    MAX_SCALE,
    H2_FONT,
    H3_FONT,
    BODY_FONT,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    calculate_scale,
    sx,
    sy,
    create_button,
    set_button_state,
    BUTTON_STATE_DISABLED,
)


# ============================================================
# Backup Manager — Completing the initial setup
# ============================================================






# ============================================================
# Fonts
# ============================================================

SUMMARY_FONT = ("Zen Kaku Gothic Antique", 12)


# ============================================================
# Navigation buttons
# ============================================================

BACK_BUTTON_WIDTH = 160
BACK_BUTTON_HEIGHT = 60

SAVE_EXIT_BUTTON_WIDTH = 280
SAVE_EXIT_BUTTON_HEIGHT = 60


# ============================================================
# Positions
# ============================================================

TITLE_Y = 28

SUMMARY_LABEL_X = 0
SUMMARY_VALUE_X = 235
SUMMARY_Y = 170
SUMMARY_LINE_GAP = 36

NAV_BUTTON_Y = 560
BACK_BUTTON_X = 0


# ============================================================
# Default display data
# ============================================================
# These are GUI defaults only. Later the application can pass the
# actual values selected by the user into the window constructor.

DEFAULT_SOURCE = r"D:\Users\Olha\Documents"
DEFAULT_BACKUP_LOCATION = r"E:\BackupProject"
DEFAULT_COPIES = "10"
DEFAULT_FREQUENCY = "1 day"
DEFAULT_FIRST_BACKUP = "29.08.2026 17:30"


class CompletingSetupWindow:
    """Window 7.1 / 7.2 — final review of the initial setup."""

    def __init__(self, parent, controller, scale,
                 source=DEFAULT_SOURCE, backup_location=DEFAULT_BACKUP_LOCATION,
                 copies=DEFAULT_COPIES, frequency=DEFAULT_FREQUENCY,
                 first_backup=DEFAULT_FIRST_BACKUP, scheduled_datetime=None,
                 on_back=None, on_action=None, on_timeout=None):
        self.root = controller.root
        self.controller = controller
        self.parent = parent
        self.canvas = parent
        self.scale = scale

        self.scheduled_datetime = scheduled_datetime
        self.on_timeout = on_timeout
        self._timeout_warning_shown = False
        self._timeout_after_id = None
        self.save_exit_enabled = True

        self.source = source
        self.backup_location = backup_location
        self.copies = copies
        self.frequency = frequency
        self.first_backup = first_backup

        # Navigation is owned by the controller.
        self.on_back = on_back or controller.back_from_window_7_2
        self.on_action = on_action or controller.save_and_exit_from_window_7_2

        # This block uses the already-created root and shared Canvas.
        # It does not change the main window geometry or create a container.
        self._draw_interface()
        self._start_timeout_monitor()

    # ========================================================
    # SCALE
    # ========================================================

    def _calculate_scale(self):
        if self._external_scale is not None:
            return self._external_scale

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        available_width = screen_width - 80
        available_height = screen_height - 120

        return calculate_scale(
            available_width,
            available_height,
            max_scale=MAX_SCALE,
        )

    def sx(self, value):
        return sx(value, self.scale)

    def sy(self, value):
        return sy(value, self.scale)

    def _scaled_font(self, font):
        if len(font) == 2:
            family, size = font
            return (family, max(1, int(round(size * self.scale))))

        family, size, weight = font
        return (family, max(1, int(round(size * self.scale))), weight)

    # ========================================================
    # SCALE / COORDINATE CONVERSION
    # ========================================================

    def sx(self, value):
        return sx(value, self.scale)

    def sy(self, value):
        return sy(value, self.scale)

    def _scaled_font(self, font):
        if len(font) == 2:
            family, size = font
            return (family, max(1, int(round(size * self.scale))))

        family, size, weight = font
        return (family, max(1, int(round(size * self.scale))), weight)

    # ========================================================
    # INTERFACE
    # ========================================================

    def _draw_interface(self):
        self.canvas.delete("all")

        width = self.sx(DESIGN_WIDTH)
        height = self.sy(DESIGN_HEIGHT)

        self.canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=max(
                1,
                self.sx(WINDOW_BORDER_WIDTH),
            ),
        )

        content_x = (
            DESIGN_WIDTH - CONTENT_WIDTH
        ) / 2

        content_y = (
            DESIGN_HEIGHT - CONTENT_HEIGHT
        ) / 2

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.canvas.create_text(
            self.sx(
                content_x
                + CONTENT_WIDTH / 2
            ),
            self.sy(
                content_y
                + TITLE_Y
            ),
            text="Backup Manager",
            fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT),
            anchor="center",
        )

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        self.canvas.create_text(
            self.sx(
                content_x
                + SUMMARY_LABEL_X
            ),
            self.sy(
                content_y
                + SUMMARY_Y
            ),
            text="Your backup schedule is ready.",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
        )

        summary_rows = [
            ("Source:", self.source),
            ("Backup location:", self.backup_location),
            ("Copies to keep:", self.copies),
            ("Frequency:", self.frequency),
            ("First backup:", self.first_backup),
        ]

        for index, (label, value) in enumerate(summary_rows, start=1):
            y = (36 +
                content_y
                + SUMMARY_Y
                + index * SUMMARY_LINE_GAP
            )

            self.canvas.create_text(
                self.sx(
                    content_x
                    + SUMMARY_LABEL_X
                ),
                self.sy(y),
                text=label,
                fill=TEXT_COLOR,
                font=self._scaled_font(BODY_FONT),
                anchor="w",
            )

            self.canvas.create_text(
                self.sx(
                    content_x
                    + SUMMARY_VALUE_X
                ),
                self.sy(y),
                text=value,
                fill=TEXT_COLOR,
                font=self._scaled_font(BODY_FONT),
                anchor="w",
            )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        self._create_button(
            x=(
                content_x
                + BACK_BUTTON_X
            ),
            y=(
                content_y
                + NAV_BUTTON_Y
            ),
            width=BACK_BUTTON_WIDTH,
            height=BACK_BUTTON_HEIGHT,
            text="Back",
            command=self._back,
        )

        self._create_button(
            x=(
                content_x
                + CONTENT_WIDTH
                - SAVE_EXIT_BUTTON_WIDTH
            ),
            y=(
                content_y
                + NAV_BUTTON_Y
            ),
            width=SAVE_EXIT_BUTTON_WIDTH,
            height=SAVE_EXIT_BUTTON_HEIGHT,
            text="Save settings",
            command=self._action,
        )

    # ========================================================
    # BUTTON
    # ========================================================

    def _create_button(
        self,
        x,
        y,
        width,
        height,
        text,
        command,
    ):
        rectangle_id, text_id = create_button(
            self.canvas,
            x=x,
            y=y,
            width=width,
            height=height,
            text=text,
            command=command,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            tag=("window7_2_save_exit_button" if text == "Save and exit" else None),
        )

        if text == "Save and exit":
            self.save_exit_rectangle_id = rectangle_id
            self.save_exit_text_id = text_id

        # create_button() installs mouse bindings when initially normal.
        # Keep those bindings, but make Save and exit state-aware so a
        # disabled button cannot react to hover/click.
        if text == "Save and exit":
            self._install_save_exit_state_bindings()
            self._update_save_exit_state()

    # ========================================================
    # SAVE AND EXIT STATE / TIMEOUT
    # ========================================================

    def _install_save_exit_state_bindings(self):
        tag = "window7_2_save_exit_button"

        self.canvas.tag_bind(
            tag, "<Enter>", self._save_exit_enter
        )
        self.canvas.tag_bind(
            tag, "<Leave>", self._save_exit_leave
        )
        self.canvas.tag_bind(
            tag, "<ButtonPress-1>", self._save_exit_press
        )
        self.canvas.tag_bind(
            tag, "<ButtonRelease-1>", self._save_exit_release
        )

    def _save_exit_enter(self, event=None):
        if self.save_exit_enabled:
            self.canvas.itemconfig(
                "window7_2_save_exit_button",
                state="normal",
            )

    def _save_exit_leave(self, event=None):
        if self.save_exit_enabled:
            self.canvas.itemconfig(
                "window7_2_save_exit_button",
                state="normal",
            )

    def _save_exit_press(self, event=None):
        if self.save_exit_enabled:
            self.canvas.itemconfig(
                "window7_2_save_exit_button",
                state="normal",
            )

    def _save_exit_release(self, event=None):
        if self.save_exit_enabled:
            self._action()

    def _update_save_exit_state(self):
        if self.save_exit_enabled:
            set_button_state(
                self.canvas,
                self.save_exit_rectangle_id,
                self.save_exit_text_id,
                BUTTON_PRIMARY,
                "normal",
                scale=self.scale,
            )
        else:
            set_button_state(
                self.canvas,
                self.save_exit_rectangle_id,
                self.save_exit_text_id,
                BUTTON_PRIMARY,
                BUTTON_STATE_DISABLED,
                scale=self.scale,
            )

    def set_scheduled_datetime(self, scheduled_datetime):
        """Update the scheduled time when the screen is shown again."""
        self._cancel_timeout_monitor()
        self.scheduled_datetime = scheduled_datetime
        self._timeout_warning_shown = False
        self.save_exit_enabled = True

        # Always synchronize the visible button with the logical state.
        # This is important when Window 7.2 is reused after a previous
        # timeout or after navigation back from another screen.
        self._update_save_exit_state()

        if self.scheduled_datetime is None:
            return

        self._start_timeout_monitor()

    def _start_timeout_monitor(self):
        if self.scheduled_datetime is None:
            return
        self._check_timeout()

    def _check_timeout(self):
        if self._timeout_warning_shown or not self.save_exit_enabled:
            return

        try:
            from datetime import datetime
            scheduled = self.scheduled_datetime
            if not isinstance(scheduled, datetime):
                return

            now = datetime.now(scheduled.tzinfo) if scheduled.tzinfo else datetime.now()
            seconds_remaining = (scheduled - now).total_seconds()

            # Save and exit becomes unavailable five minutes before the
            # scheduled time, providing a deliberate safety margin.
            if seconds_remaining <= 300:
                self.save_exit_enabled = False
                self._update_save_exit_state()
                self._timeout_warning_shown = True
                self._show_timeout_warning()
                return
        except Exception:
            # The controller remains responsible for supplying a valid
            # datetime. Do not break the GUI if it is absent/invalid.
            return

        self._timeout_after_id = self.root.after(250, self._check_timeout)

    def _show_timeout_warning(self):
        if self.on_timeout is not None:
            self.on_timeout()
        else:
            print("The timeout period has expired.")

    def _cancel_timeout_monitor(self):
        if self._timeout_after_id is not None:
            try:
                self.root.after_cancel(self._timeout_after_id)
            except tk.TclError:
                pass
            self._timeout_after_id = None

    def destroy(self):
        self._cancel_timeout_monitor()

    # ========================================================
    # ACTIONS
    # ========================================================

    def _back(self):
        # Window 7.2 may remain pre-created and hidden after navigation.
        # Stop its timeout monitor before leaving so a hidden screen cannot
        # later open the timeout warning by itself.
        self._cancel_timeout_monitor()

        if self.on_back is not None:
            self.on_back()
        else:
            print("Back")

    def _action(self):
        if not self.save_exit_enabled:
            return

        # Final guard against a race at the five-minute boundary.
        if self.scheduled_datetime is not None:
            try:
                from datetime import datetime
                scheduled = self.scheduled_datetime
                now = datetime.now(scheduled.tzinfo) if scheduled.tzinfo else datetime.now()
                if (scheduled - now).total_seconds() <= 60:
                    self.save_exit_enabled = False
                    self._update_save_exit_state()
                    self._timeout_warning_shown = True
                    self._show_timeout_warning()
                    return
            except Exception:
                pass

        self._cancel_timeout_monitor()

        if self.on_action is not None:
            self.on_action()
        else:
            print("Save and exit")


# ============================================================
# Standalone test
# ============================================================

def main():
    root = tk.Tk()

    CompletingSetupWindow(
        root,
        scheduled_datetime=None,
    )

    root.mainloop()


if __name__ == "__main__":
    print("Window 7.2 is intended to be launched by app_controller_7.py")
