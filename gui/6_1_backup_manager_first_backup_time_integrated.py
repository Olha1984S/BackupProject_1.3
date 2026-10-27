import tkinter as tk
from pathlib import Path

from gui_style import (
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
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    calculate_scale,
    sx,
    sy,
    create_button,
)


# ============================================================
# Window 6.1 — Backup Manager: First backup time
# ============================================================





# ------------------------------------------------------------
# Fonts
# ------------------------------------------------------------

RADIO_FONT = ("Zen Kaku Gothic Antique", 12)

# ------------------------------------------------------------
# Radio buttons
# ------------------------------------------------------------

RADIO_SIZE = 20
RADIO_TEXT_GAP = 12
RADIO_ROW_GAP = 48

# ------------------------------------------------------------
# Navigation buttons
# ------------------------------------------------------------

NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60

# ------------------------------------------------------------
# Positions inside the Figma content area
# ------------------------------------------------------------

TITLE_Y = 28

QUESTION_Y = 240
RADIO_START_Y = 270

NAV_BUTTON_Y = 560

# ------------------------------------------------------------
# Radio button images
# ------------------------------------------------------------

IMAGE_DIR = Path(__file__).resolve().parent / "images"

ACTIVE_RADIO_PATH = IMAGE_DIR / "radio_button_active.png"
PASSIVE_RADIO_PATH = IMAGE_DIR / "radio_button_passive.png"


class FirstBackupTimeWindow:
    """GUI for selecting when the first backup should start."""

    def __init__(self, parent, controller, scale):
        self.parent = parent
        self.controller = controller
        self.root = controller.root
        self.canvas = parent
        self.scale = scale

        self.active_radio_image = None
        self.passive_radio_image = None

        self.selected_option = "Start after completing the settings"

        self._load_radio_images()
        self._draw_interface()

    # ========================================================
    # COORDINATE CONVERSION
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
    # RADIO BUTTON IMAGES
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
    # INTERFACE
    # ========================================================

    def _draw_interface(self):
        self.canvas.delete("all")

        width = self.sx(DESIGN_WIDTH)
        height = self.sy(DESIGN_HEIGHT)

        # ----------------------------------------------------
        # Background and window border
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Centered Figma content area
        # ----------------------------------------------------

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
        # Question
        # ----------------------------------------------------

        self.canvas.create_text(
            self.sx(content_x),
            self.sy(
                content_y
                + QUESTION_Y
            ),
            text="Specify the first backup time",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
        )

        # ----------------------------------------------------
        # Start now
        # ----------------------------------------------------

        start_now_y = (
            content_y
            + RADIO_START_Y
            + 16
        )

        self._create_radio_button(
            x=content_x + 24,
            y=start_now_y,
            value="Start after completing the settings",
            clickable=True,
        )

        # ----------------------------------------------------
        # Set start time
        # ----------------------------------------------------

        start_time_y = (
            content_y
            + RADIO_START_Y
            + RADIO_ROW_GAP
            + 16
        )

        self._create_radio_button(
            x=content_x + 24,
            y=start_time_y,
            value="Set start time",
            clickable=True,
        )

        # ----------------------------------------------------
        # Navigation buttons
        # ----------------------------------------------------

        self._create_main_button(
            x=content_x,
            y=content_y + NAV_BUTTON_Y,
            text="Back",
            command=self._back,
        )

        self._create_main_button(
            x=(
                content_x
                + CONTENT_WIDTH
                - NAV_BUTTON_WIDTH
            ),
            y=content_y + NAV_BUTTON_Y,
            text="Next",
            command=self._next,
        )

    # ========================================================
    # RADIO BUTTON
    # ========================================================

    def _create_radio_button(
        self,
        x,
        y,
        value,
        clickable=True,
    ):
        active = (
            self.selected_option == value
        )

        image = (
            self.active_radio_image
            if active
            else self.passive_radio_image
        )

        if image is not None:
            icon_id = self.canvas.create_image(
                self.sx(x),
                self.sy(y),
                image=image,
                anchor="nw",
            )

        else:
            icon_id = self.canvas.create_oval(
                self.sx(x),
                self.sy(y),
                self.sx(x + RADIO_SIZE),
                self.sy(y + RADIO_SIZE),
                fill=(
                    TEXT_COLOR
                    if active
                    else BACKGROUND_COLOR
                ),
                outline=TEXT_COLOR,
                width=max(
                    1,
                    self.sx(2),
                ),
            )

        text_id = self.canvas.create_text(
            self.sx(
                x
                + RADIO_SIZE
                + RADIO_TEXT_GAP
                + 16
            ),
            self.sy(
                y
                + RADIO_SIZE / 2
                + 4
            ),
            text=value,
            fill=TEXT_COLOR,
            font=self._scaled_font(RADIO_FONT),
            anchor="w",
        )

        if clickable:
            self.canvas.tag_bind(
                icon_id,
                "<Button-1>",
                lambda event, selected=value:
                self._select_option(selected),
            )

            self.canvas.tag_bind(
                text_id,
                "<Button-1>",
                lambda event, selected=value:
                self._select_option(selected),
            )

    # ========================================================
    # SELECT OPTION
    # ========================================================

    def _select_option(self, value):
        self.selected_option = value
        self._draw_interface()

        if value == "Set start time":
            self.controller.open_window_6_2()

    # ========================================================
    # BACK
    # ========================================================

    def _back(self):
        self.controller.back_from_window_6_1()

    # ========================================================
    # NEXT
    # ========================================================

    def _next(self):
        if self.selected_option == "Set start time":
            self.controller.open_window_6_2()
            return

        self.controller.next_from_window_6_1(self.selected_option)


    # ========================================================
    # MAIN BUTTON
    # ========================================================

    def _create_main_button(
        self,
        x,
        y,
        text,
        command,
    ):
        create_button(
            self.canvas,
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


    def destroy(self):
        pass


