import tkinter as tk
from pathlib import Path
from datetime import date

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    CONTENT_WIDTH,
    CONTENT_HEIGHT,
    WINDOW_BORDER_WIDTH,
    H2_FONT,
    H3_FONT,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    sx,
    sy,
    create_button,
)


RADIO_FONT = ("Zen Kaku Gothic Antique", 12)
DATE_FONT = ("Zen Kaku Gothic Antique", 12)
RADIO_SIZE = 20
RADIO_TEXT_GAP = 12
RADIO_ROW_GAP = 48
NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60
TITLE_Y = 28
QUESTION_Y = 240
RADIO_START_Y = 270
NAV_BUTTON_Y = 560

IMAGE_DIR = Path(__file__).resolve().parent / "images"
ACTIVE_RADIO_PATH = IMAGE_DIR / "radio_button_active.png"
PASSIVE_RADIO_PATH = IMAGE_DIR / "radio_button_passive.png"


class FirstBackupDateWindow:
    """GUI Block 5.1 — select Today or open the calendar."""

    def __init__(self, parent, controller, scale):
        self.parent = parent
        self.controller = controller
        self.scale = scale

        self.active_radio_image = None
        self.passive_radio_image = None
        self.today_date = date.today().strftime("%d.%m.%Y")

        self._load_radio_images()
        self._draw_interface()

    def _scaled_font(self, font):
        if len(font) == 2:
            family, size = font
            return family, max(1, round(size * self.scale))
        family, size, weight = font
        return family, max(1, round(size * self.scale)), weight

    def _load_radio_images(self):
        if ACTIVE_RADIO_PATH.exists():
            self.active_radio_image = tk.PhotoImage(file=str(ACTIVE_RADIO_PATH))
        if PASSIVE_RADIO_PATH.exists():
            self.passive_radio_image = tk.PhotoImage(file=str(PASSIVE_RADIO_PATH))

    def _draw_interface(self):
        self.parent.delete("screen_content")

        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        self.parent.create_rectangle(
            0, 0,
            sx(DESIGN_WIDTH, self.scale),
            sy(DESIGN_HEIGHT, self.scale),
            fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=max(1, sx(WINDOW_BORDER_WIDTH, self.scale)),
            tags=("screen_content",),
        )

        self.parent.create_text(
            sx(content_x + CONTENT_WIDTH / 2, self.scale),
            sy(content_y + TITLE_Y, self.scale),
            text="Backup Manager",
            fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT),
            anchor="center",
            tags=("screen_content",),
        )

        self.parent.create_text(
            sx(content_x, self.scale),
            sy(content_y + QUESTION_Y, self.scale),
            text="Specify the first backup date",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
            tags=("screen_content",),
        )

        today_y = content_y + RADIO_START_Y + 16
        self._create_radio_button(content_x + 24, today_y, "Today", True)

        self.parent.create_text(
            sx(content_x + 24 + RADIO_SIZE + RADIO_TEXT_GAP + 82, self.scale),
            sy(today_y + RADIO_SIZE / 2 + 4, self.scale),
            text=self.today_date,
            fill=TEXT_COLOR,
            font=self._scaled_font(DATE_FONT),
            anchor="w",
            tags=("screen_content",),
        )

        start_date_y = content_y + RADIO_START_Y + RADIO_ROW_GAP + 16
        self._create_radio_button(content_x + 24, start_date_y, "Set start date", False)

        self._create_main_button(
            content_x, content_y + NAV_BUTTON_Y, "Back", self._back
        )
        self._create_main_button(
            content_x + CONTENT_WIDTH - NAV_BUTTON_WIDTH,
            content_y + NAV_BUTTON_Y,
            "Next",
            self._next,
        )

    def _create_radio_button(self, x, y, value, selected):
        image = self.active_radio_image if selected else self.passive_radio_image

        if image is not None:
            icon_id = self.parent.create_image(
                sx(x, self.scale), sy(y, self.scale),
                image=image, anchor="nw", tags=("screen_content",)
            )
        else:
            icon_id = self.parent.create_oval(
                sx(x, self.scale), sy(y, self.scale),
                sx(x + RADIO_SIZE, self.scale), sy(y + RADIO_SIZE, self.scale),
                fill=TEXT_COLOR if selected else BACKGROUND_COLOR,
                outline=TEXT_COLOR,
                width=max(1, sx(2, self.scale)),
                tags=("screen_content",),
            )

        text_id = self.parent.create_text(
            sx(x + RADIO_SIZE + RADIO_TEXT_GAP + 16, self.scale),
            sy(y + RADIO_SIZE / 2 + 4, self.scale),
            text=value,
            fill=TEXT_COLOR,
            font=self._scaled_font(RADIO_FONT),
            anchor="w",
            tags=("screen_content",),
        )

        self.parent.tag_bind(
            icon_id, "<Button-1>",
            lambda event, value=value: self._select_option(value),
        )
        self.parent.tag_bind(
            text_id, "<Button-1>",
            lambda event, value=value: self._select_option(value),
        )

    def _select_option(self, value):
        if value == "Set start date":
            self.controller.show_screen("first_backup_calendar")

    def _create_main_button(self, x, y, text, command):
        create_button(
            self.parent,
            x=x,
            y=y,
            width=NAV_BUTTON_WIDTH,
            height=NAV_BUTTON_HEIGHT,
            text=text,
            command=command,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
        )

    def _back(self):
        self.controller.show_screen(
            self.controller.state.get("frequency_screen", "frequency")
        )

    def _next(self):
        self.controller.state["first_backup_date"] = date.today().strftime("%d.%m.%Y")
        self.controller.show_screen("window6")

    def destroy(self):
        self.parent.delete("screen_content")
