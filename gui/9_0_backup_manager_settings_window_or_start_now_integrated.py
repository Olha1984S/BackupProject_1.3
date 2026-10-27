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
# Backup Manager — Settings overview / Start now
# ============================================================

# ============================================================
# Navigation buttons
# ============================================================

SETTINGS_BUTTON_WIDTH = 240
SETTINGS_BUTTON_HEIGHT = 60

START_NOW_BUTTON_WIDTH = 240
START_NOW_BUTTON_HEIGHT = 60


# ============================================================
# Positions
# ============================================================

TITLE_Y = 28

SUMMARY_LABEL_X = 0
SUMMARY_VALUE_X = 235
SUMMARY_Y = 170
SUMMARY_LINE_GAP = 36

NAV_BUTTON_Y = 560
SETTINGS_BUTTON_X = 0
START_NOW_BUTTON_X = 560


# ============================================================
# Default display data
# ============================================================
# These are GUI defaults only. Later the application can pass the
# actual values selected by the user into the window constructor.

DEFAULT_SOURCE = r"D:\Users\Olha\Documents"
DEFAULT_BACKUP_LOCATION = r"E:\BackupProject"
DEFAULT_COPIES = "10"
DEFAULT_FREQUENCY = "1 day"
DEFAULT_FIRST_BACKUP = "Today"


class BackupManagerSettingsWindow:
    """GUI Block 9 — settings overview and immediate backup start."""

    def __init__(
        self,
        root,
        source=DEFAULT_SOURCE,
        backup_location=DEFAULT_BACKUP_LOCATION,
        copies=DEFAULT_COPIES,
        frequency=DEFAULT_FREQUENCY,
        first_backup=DEFAULT_FIRST_BACKUP,
        on_settings=None,
        on_start_now=None,
        parent=None,
        scale=1.0,
    ):
        self.root = root
        self.parent = parent
        self.source = source
        self.backup_location = backup_location
        self.copies = copies
        self.frequency = frequency
        self.first_backup = first_backup

        self.on_settings = on_settings
        self.on_start_now = on_start_now

        self.scale = scale
        self.canvas = self.parent
        if self.canvas is None:
            raise ValueError("BackupManagerSettingsWindow requires the shared Canvas.")
        self._draw_interface()

    # ========================================================
    # SCALE
    # ========================================================

    def sx(self, value):
        return sx(value, self.scale)

    def sy(self, value):
        return sy(value, self.scale)

    def _scaled_font(self, font):
        if len(font) == 2:
            family, size = font
            return (
                family,
                max(1, int(round(size * self.scale))),
            )

        family, size, weight = font
        return (
            family,
            max(1, int(round(size * self.scale))),
            weight,
        )

    # ========================================================
    # INTERFACE
    # ========================================================

    def _draw_interface(self):
        self.canvas.delete("window9_content")

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
            tags=("screen_content", "window9_content"),
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
            tags=("screen_content", "window9_content"),
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
            tags=("screen_content", "window9_content"),
        )

        summary_rows = [
            ("Source:", self.source),
            ("Backup location:", self.backup_location),
            ("Copies to keep:", self.copies),
            ("Frequency:", self.frequency),
            ("Next backup:", self.first_backup),
        ]

        for index, (label, value) in enumerate(
            summary_rows,
            start=1,
        ):
            y = (
                36
                + content_y
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
                tags=("screen_content", "window9_content"),
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
                tags=("screen_content", "window9_content"),
            )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        self._create_button(
            x=(
                content_x
                + SETTINGS_BUTTON_X
            ),
            y=(
                content_y
                + NAV_BUTTON_Y
            ),
            width=SETTINGS_BUTTON_WIDTH,
            height=SETTINGS_BUTTON_HEIGHT,
            text="Settings",
            command=self._settings,
        )

        self._create_button(
            x=(
                content_x
                + START_NOW_BUTTON_X
            ),
            y=(
                content_y
                + NAV_BUTTON_Y
            ),
            width=START_NOW_BUTTON_WIDTH,
            height=START_NOW_BUTTON_HEIGHT,
            text="Start now",
            command=self._start_now,
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
            tag=("screen_content window9_settings_button" if text == "Settings" else "screen_content window9_start_now_button"),
        )

    # ========================================================
    # ACTIONS
    # ========================================================

    def _settings(self):
        if self.on_settings is not None:
            self.on_settings()
        else:
            print("Settings")

    def _start_now(self):
        if self.on_start_now is not None:
            self.on_start_now()
        else:
            print("Start now")


# ============================================================
# Standalone test
# ============================================================

def main():
    root = tk.Tk()

    canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)
    BackupManagerSettingsWindow(root, parent=canvas)

    root.geometry(f"{DESIGN_WIDTH // 2}x{DESIGN_HEIGHT // 2}")
    root.mainloop()


if __name__ == "__main__":
    main()
