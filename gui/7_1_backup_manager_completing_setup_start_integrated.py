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

START_BUTTON_WIDTH = 160
START_BUTTON_HEIGHT = 60



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
DEFAULT_FIRST_BACKUP = "After completing the settings"


class CompletingSetupWindow:
    """Window 7.1 / 7.2 — final review of the initial setup."""

    def __init__(self, parent, controller, scale,
                 source=DEFAULT_SOURCE, backup_location=DEFAULT_BACKUP_LOCATION,
                 copies=DEFAULT_COPIES, frequency=DEFAULT_FREQUENCY,
                 first_backup=DEFAULT_FIRST_BACKUP, on_back=None, on_action=None):
        self.root = controller.root
        self.controller = controller
        self.parent = parent
        self.canvas = parent
        self.scale = scale

        self.source = source
        self.backup_location = backup_location
        self.copies = copies
        self.frequency = frequency
        self.first_backup = first_backup

        # Navigation is owned by the controller.
        self.on_back = on_back or controller.back_from_window_7_1
        self.on_action = on_action or controller.start_backup_from_window_7_1

        # This block uses the already-created root and shared Canvas.
        # It does not change the main window geometry or create a container.
        self._draw_interface()

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

    def destroy(self):
        # The shared Canvas belongs to the controller.
        # There are no child windows or scheduled callbacks to cancel here.
        pass

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
                - START_BUTTON_WIDTH
            ),
            y=(
                content_y
                + NAV_BUTTON_Y
            ),
            width=START_BUTTON_WIDTH,
            height=START_BUTTON_HEIGHT,
            text="Start",
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
        create_button(
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
        )

    # ========================================================
    # ACTIONS
    # ========================================================

    def _back(self):
        if self.on_back is not None:
            self.on_back()
        else:
            print("Back")

    def _action(self):
        if self.on_action is not None:
            self.on_action()
        else:
            print("Start")


# ============================================================
# Standalone test
# ============================================================

def main():
    root = tk.Tk()

    CompletingSetupWindow(
        root,
    )

    root.mainloop()


if __name__ == "__main__":
    print("Window 7.1 is intended to be launched by app_controller_7.py")
