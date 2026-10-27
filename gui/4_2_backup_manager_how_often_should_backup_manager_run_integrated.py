import tkinter as tk
from pathlib import Path

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    H2_FONT,
    H3_FONT,
    SMALL_FONT,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    sx,
    sy,
    create_button,
)


# ============================================================
# Window 4.2 — Custom interval
# ============================================================

CONTENT_WIDTH = 800
CONTENT_HEIGHT = 640

RADIO_SIZE = 20
RADIO_TEXT_GAP = 12
RADIO_ROW_GAP = 48
RADIO_FONT = ("Zen Kaku Gothic Antique", 12)

INTERVAL_ENTRY_WIDTH = 60
INTERVAL_ENTRY_HEIGHT = 34
ENTRY_INNER_PADDING = 8

INTERVAL_ENTRY_GAP = 16
DAYS_TEXT_GAP = 16

INPUT_HINT_TEXT = "* Use digital format"
HINT_X_OFFSET = 160

NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60

TITLE_Y = 28
QUESTION_Y = 180
RADIO_START_Y = 220
NAV_BUTTON_Y = 560

IMAGE_DIR = Path(__file__).resolve().parent / "images"
ACTIVE_RADIO_PATH = IMAGE_DIR / "radio_button_active.png"
PASSIVE_RADIO_PATH = IMAGE_DIR / "radio_button_passive.png"


class CustomIntervalWindow:
    """GUI Block 4.2 — uses the shared application Canvas."""

    def __init__(self, parent, controller, scale):
        self.parent = parent
        self.controller = controller
        self.scale = scale

        self.interval_entry = None
        self.active_radio_image = None
        self.passive_radio_image = None

        self.selected_frequency = "Custom interval"

        self._load_radio_images()
        self._build_screen()

        self.interval_entry.focus_set()

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
        self.interval_entry = self._create_entry()
        self._draw_interface()

        self.interval_entry.focus_set()

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
            tags=("screen_content", "window4_2_content"),
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
            tags=("screen_content", "window4_2_content"),
        )

        # ----------------------------------------------------
        # Regular radio buttons
        # ----------------------------------------------------

        frequencies = [
            "1 day",
            "1 week",
            "1 month",
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
        # Custom interval row
        # ----------------------------------------------------

        custom_y = (
            content_y
            + RADIO_START_Y
            + 3 * RADIO_ROW_GAP
        ) + 16

        self._create_custom_interval_row(
            x=content_x + 24,
            y=custom_y,
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
    # Radio buttons
    # ========================================================

    def _create_radio_button(self, x, y, value):
        image = self.passive_radio_image

        if image is not None:
            icon = self.parent.create_image(
                self.sx(x),
                self.sy(y),
                image=image,
                anchor="nw",
                tags=("screen_content", "window4_2_content"),
            )
        else:
            icon = self.parent.create_oval(
                self.sx(x),
                self.sy(y),
                self.sx(x + RADIO_SIZE),
                self.sy(y + RADIO_SIZE),
                fill=BACKGROUND_COLOR,
                outline=TEXT_COLOR,
                width=max(1, self.sx(2)),
                tags=("screen_content", "window4_2_content"),
            )

        text = self.parent.create_text(
            self.sx(x + RADIO_SIZE + RADIO_TEXT_GAP + 16),
            self.sy(y + RADIO_SIZE / 2 + 4),
            text=value,
            fill=TEXT_COLOR,
            font=self._scaled_font(RADIO_FONT),
            anchor="w",
            tags=("screen_content", "window4_2_content"),
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
    # Custom interval row
    # ========================================================

    def _create_custom_interval_row(self, x, y):
        value = "Custom interval"

        if self.active_radio_image is not None:
            icon = self.parent.create_image(
                self.sx(x),
                self.sy(y),
                image=self.active_radio_image,
                anchor="nw",
                tags=("screen_content", "window4_2_content"),
            )
        else:
            icon = self.parent.create_oval(
                self.sx(x),
                self.sy(y),
                self.sx(x + RADIO_SIZE),
                self.sy(y + RADIO_SIZE),
                fill=TEXT_COLOR,
                outline=TEXT_COLOR,
                width=max(1, self.sx(2)),
                tags=("screen_content", "window4_2_content"),
            )

        text_x = x + RADIO_SIZE + RADIO_TEXT_GAP + 16

        text = self.parent.create_text(
            self.sx(text_x),
            self.sy(y + RADIO_SIZE / 2 + 4),
            text=value,
            fill=TEXT_COLOR,
            font=self._scaled_font(RADIO_FONT),
            anchor="w",
            tags=("screen_content", "window4_2_content"),
        )

        text_bbox = self.parent.bbox(text)

        if text_bbox is not None:
            entry_x = (
                x
                + (text_bbox[2] / self.scale - x)
                + INTERVAL_ENTRY_GAP
            )
        else:
            entry_x = text_x + 120

        self._draw_entry_border(entry_x, y)
        self._place_entry(entry_x, y)

        days_x = (
            entry_x
            + INTERVAL_ENTRY_WIDTH
            + DAYS_TEXT_GAP
        )

        days_text = self.parent.create_text(
            self.sx(days_x),
            self.sy(y + RADIO_SIZE / 2 + 4),
            text="days",
            fill=TEXT_COLOR,
            font=self._scaled_font(RADIO_FONT),
            anchor="w",
            tags=("screen_content", "window4_2_content"),
        )

        # Input hint — on the same line as Custom interval.
        self.parent.create_text(
            self.sx(days_x + 70),
            self.sy(y + RADIO_SIZE / 2 + 4),
            text=INPUT_HINT_TEXT,
            fill=TEXT_COLOR,
            font=self._scaled_font(SMALL_FONT),
            anchor="w",
            tags=("screen_content", "window4_2_content"),
        )

        # Only the regular radio options return to Window 4.1.
        # The custom radio remains selected on this screen.
        self.parent.tag_bind(
            icon,
            "<Button-1>",
            lambda event: None,
        )

        self.parent.tag_bind(
            text,
            "<Button-1>",
            lambda event: None,
        )

        self.parent.tag_bind(
            days_text,
            "<Button-1>",
            lambda event: None,
        )

    # ========================================================
    # Entry
    # ========================================================

    def _create_entry(self):
        validate_command = self.parent.register(
            self._validate_interval_input
        )

        return tk.Entry(
            self.parent,
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=self._scaled_font(RADIO_FONT),
            justify="left",
            validate="key",
            validatecommand=(validate_command, "%P"),
        )

    def _validate_interval_input(self, value):
        return value == "" or value.isdigit()

    def _draw_entry_border(self, x, y):
        line_y = self.sy(y + INTERVAL_ENTRY_HEIGHT)

        self.parent.create_rectangle(
            self.sx(x),
            line_y,
            self.sx(x + INTERVAL_ENTRY_WIDTH),
            line_y + max(1, self.sx(1)),
            fill=TEXT_COLOR,
            outline="",
            tags=("screen_content", "window4_2_content"),
        )

    def _place_entry(self, x, y):
        self.interval_entry.place(
            x=self.sx(x + ENTRY_INNER_PADDING),
            y=self.sy(y),
            width=self.sx(
                INTERVAL_ENTRY_WIDTH - 2 * ENTRY_INNER_PADDING
            ),
            height=self.sy(INTERVAL_ENTRY_HEIGHT - 6),
        )

        saved = self.controller.state.get("custom_interval_days", "")
        if saved not in ("", None):
            self.interval_entry.insert(0, str(saved))

    # ========================================================
    # Selection
    # ========================================================

    def _select_frequency(self, value):
        self.controller.state["backup_frequency"] = value
        self.controller.show_screen("frequency")

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
            tag=f"window4_2_nav_{text}",
        )

    def _back(self):
        self._save_interval()
        self.controller.show_screen("copies")

    def _next(self):
        interval = self.interval_entry.get().strip()

        if not interval.isdigit() or int(interval) <= 0:
            self.interval_entry.focus_set()
            return

        self._save_interval()
        self.controller.state["backup_frequency"] = "Custom interval"
        self.controller.show_screen("window5")

    def _save_interval(self):
        self.controller.state["custom_interval_days"] = (
            self.interval_entry.get().strip()
        )

    # ========================================================
    # Destroy
    # ========================================================

    def destroy(self):
        if self.interval_entry is not None:
            try:
                self.interval_entry.destroy()
            except tk.TclError:
                pass

        self.interval_entry = None
        self.active_radio_image = None
        self.passive_radio_image = None

        self.parent.delete("screen_content")
