import tkinter as tk
from pathlib import Path

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    H2_FONT,
    H3_FONT,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    WINDOW_BORDER_WIDTH,
    sx,
    sy,
    create_button,
)


# ============================================================
# Window 4.1 — How often should Backup Manager run?
# ============================================================

CONTENT_WIDTH = 800
CONTENT_HEIGHT = 640

RADIO_SIZE = 20
RADIO_TEXT_GAP = 12
RADIO_ROW_GAP = 48
RADIO_FONT = ("Zen Kaku Gothic Antique", 12)

NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60

TITLE_Y = 28
QUESTION_Y = 180
RADIO_START_Y = 220
NAV_BUTTON_Y = 560

IMAGE_DIR = Path(__file__).resolve().parent / "images"
ACTIVE_RADIO_PATH = IMAGE_DIR / "radio_button_active.png"
PASSIVE_RADIO_PATH = IMAGE_DIR / "radio_button_passive.png"


class BackupFrequencyWindow:
    """GUI Block 4.1 — uses the shared application Canvas."""

    def __init__(self, parent, controller, scale):
        self.parent = parent
        self.controller = controller
        self.scale = scale

        self.active_radio_image = None
        self.passive_radio_image = None

        selected = self.controller.state.get("backup_frequency", "1 day")
        if selected == "Custom interval":
            selected = "1 day"

        self.selected_frequency = selected

        self._load_radio_images()
        self._build_screen()

    # ========================================================
    # Coordinate conversion
    # ========================================================

    def sx(self, value):
        return sx(value, self.scale)

    def sy(self, value):
        return sy(value, self.scale)

    def _scaled_font(self, font_spec):
        family = font_spec[0]
        size = int(font_spec[1])
        rest = tuple(font_spec[2:])
        return (family, max(1, self.sx(size)), *rest)

    # ========================================================
    # Radio images
    # ========================================================

    def _load_radio_images(self):
        if ACTIVE_RADIO_PATH.exists():
            self.active_radio_image = tk.PhotoImage(
                file=str(ACTIVE_RADIO_PATH)
            )

        if PASSIVE_RADIO_PATH.exists():
            self.passive_radio_image = tk.PhotoImage(
                file=str(PASSIVE_RADIO_PATH)
            )

    # ========================================================
    # Screen
    # ========================================================

    def _build_screen(self):
        self._draw_interface()

    def _draw_interface(self):
        self.parent.delete("screen_content")

        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.parent.create_text(
            self.sx(content_x + CONTENT_WIDTH / 2),
            self.sy(content_y + TITLE_Y),
            text="Backup Manager",
            fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT),
            anchor="center",
            tags=("screen_content", "window4_1_content"),
        )

        # ----------------------------------------------------
        # Question
        # ----------------------------------------------------

        self.parent.create_text(
            self.sx(content_x),
            self.sy(content_y + QUESTION_Y),
            text="How often should Backup Manager run?",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
            tags=("screen_content", "window4_1_content"),
        )

        # ----------------------------------------------------
        # Radio buttons
        # ----------------------------------------------------

        frequencies = [
            "1 day",
            "1 week",
            "1 month",
            "Custom interval",
        ]

        for index, frequency in enumerate(frequencies):
            y = (
                content_y
                + RADIO_START_Y
                + index * RADIO_ROW_GAP
            ) + 16

            self._create_radio_button(
                x=content_x + 24,
                y=y,
                value=frequency,
            )

        # ----------------------------------------------------
        # Navigation
        # ----------------------------------------------------

        self._create_main_button(
            x=content_x,
            y=content_y + NAV_BUTTON_Y,
            text="Back",
            command=self._back,
        )

        self._create_main_button(
            x=content_x + CONTENT_WIDTH - NAV_BUTTON_WIDTH,
            y=content_y + NAV_BUTTON_Y,
            text="Next",
            command=self._next,
        )

    # ========================================================
    # Radio button
    # ========================================================

    def _create_radio_button(self, x, y, value):
        selected = self.selected_frequency == value

        image = (
            self.active_radio_image
            if selected
            else self.passive_radio_image
        )

        if image is not None:
            icon = self.parent.create_image(
                self.sx(x),
                self.sy(y),
                image=image,
                anchor="nw",
                tags=("screen_content", "window4_1_content"),
            )
        else:
            icon = self.parent.create_oval(
                self.sx(x),
                self.sy(y),
                self.sx(x + RADIO_SIZE),
                self.sy(y + RADIO_SIZE),
                fill=TEXT_COLOR if selected else BACKGROUND_COLOR,
                outline=TEXT_COLOR,
                width=max(1, self.sx(2)),
                tags=("screen_content", "window4_1_content"),
            )

        text = self.parent.create_text(
            self.sx(x + RADIO_SIZE + RADIO_TEXT_GAP + 16),
            self.sy(y + RADIO_SIZE / 2 + 4),
            text=value,
            fill=TEXT_COLOR,
            font=self._scaled_font(RADIO_FONT),
            anchor="w",
            tags=("screen_content", "window4_1_content"),
        )

        self.parent.tag_bind(
            icon,
            "<Button-1>",
            lambda event, selected_value=value:
                self._select_frequency(selected_value),
        )

        self.parent.tag_bind(
            text,
            "<Button-1>",
            lambda event, selected_value=value:
                self._select_frequency(selected_value),
        )

    # ========================================================
    # Selection
    # ========================================================

    def _select_frequency(self, value):
        if value == "Custom interval":
            self.controller.state["backup_frequency"] = "Custom interval"
            self.controller.show_screen("custom_interval")
            return

        self.selected_frequency = value
        self.controller.state["backup_frequency"] = value
        self.controller.state["custom_interval_days"] = ""

        self._draw_interface()

    # ========================================================
    # Navigation
    # ========================================================

    def _create_main_button(self, x, y, text, command):
        create_button(
            self.parent,
            x,
            y,
            NAV_BUTTON_WIDTH,
            NAV_BUTTON_HEIGHT,
            text,
            command,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            tag=f"window4_1_nav_{text}",
        )

    def _back(self):
        self.controller.show_screen("copies")

    def _next(self):
        self.controller.state["backup_frequency"] = self.selected_frequency
        self.controller.show_screen("window5")

    # ========================================================
    # Destroy
    # ========================================================

    def destroy(self):
        self.parent.delete("screen_content")
        self.active_radio_image = None
        self.passive_radio_image = None
