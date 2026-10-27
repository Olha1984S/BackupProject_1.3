import tkinter as tk
import calendar
from datetime import date
from pathlib import Path

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    DISABLED_COLOR,
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


CALENDAR_FONT = ("Zen Kaku Gothic Antique", 10)
CALENDAR_HEADER_FONT = ("Zen Kaku Gothic Antique", 12, "bold")
RADIO_FONT = ("Zen Kaku Gothic Antique", 12)
RADIO_SIZE = 20
RADIO_TEXT_GAP = 12
RADIO_ROW_GAP = 48
DATE_TEXT_GAP = 82
CALENDAR_WIDTH = 160
CALENDAR_HEADER_HEIGHT = 44
CALENDAR_CELL_WIDTH = 44
CALENDAR_CELL_HEIGHT = 44
CALENDAR_TITLE_GAP = 44
CALENDAR_WEEKDAY_GAP = 36
CALENDAR_YEAR_WIDTH = 86
CALENDAR_HEADER_GAP = 16
CALENDAR_MONTH_FIELD_WIDTH = 140
CALENDAR_ARROW_GAP = 12
CALENDAR_LEFT_ARROW_X = -1
CALENDAR_LEFT_ARROW_Y = 4
CALENDAR_RIGHT_ARROW_X = 0
CALENDAR_RIGHT_ARROW_Y = 4
SELECTED_DAY_CIRCLE_SIZE = 30
SELECTED_DAY_CIRCLE_Y = -12
NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60
TITLE_Y = 28
QUESTION_Y = 240
RADIO_START_Y = 270
CALENDAR_X = 500
CALENDAR_Y = 150
NAV_BUTTON_Y = 560

IMAGE_DIR = Path(__file__).resolve().parent / "images"
ACTIVE_RADIO_PATH = IMAGE_DIR / "radio_button_active.png"
PASSIVE_RADIO_PATH = IMAGE_DIR / "radio_button_passive.png"
RIGHT_ARROW_PATH = IMAGE_DIR / "left_arrow.png"
LEFT_ARROW_PATH = IMAGE_DIR / "right_arrow.png"


class FirstBackupDateCalendarWindow:
    """GUI Block 5.2 — choose a first backup date from today onward."""

    def __init__(self, parent, controller, scale):
        self.parent = parent
        self.controller = controller
        self.scale = scale

        self.active_radio_image = None
        self.passive_radio_image = None
        self.left_arrow_image = None
        self.right_arrow_image = None

        self.selected_date = date.today()
        self.display_month = self.selected_date.month
        self.display_year = self.selected_date.year

        self._load_images()
        self._draw_interface()

    def _scaled_font(self, font):
        if len(font) == 2:
            family, size = font
            return family, max(1, round(size * self.scale))
        family, size, weight = font
        return family, max(1, round(size * self.scale)), weight

    def _load_images(self):
        if ACTIVE_RADIO_PATH.exists():
            self.active_radio_image = tk.PhotoImage(file=str(ACTIVE_RADIO_PATH))
        if PASSIVE_RADIO_PATH.exists():
            self.passive_radio_image = tk.PhotoImage(file=str(PASSIVE_RADIO_PATH))
        if LEFT_ARROW_PATH.exists():
            self.left_arrow_image = tk.PhotoImage(file=str(LEFT_ARROW_PATH))
        if RIGHT_ARROW_PATH.exists():
            self.right_arrow_image = tk.PhotoImage(file=str(RIGHT_ARROW_PATH))

    def _draw_interface(self):
        self.parent.delete("screen_content")

        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        self.parent.create_rectangle(
            0, 0,
            sx(DESIGN_WIDTH, self.scale), sy(DESIGN_HEIGHT, self.scale),
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
        self._create_radio_button(content_x + 24, today_y, "Today", False)

        start_date_y = content_y + RADIO_START_Y + RADIO_ROW_GAP + 16
        self._create_radio_button(content_x + 24, start_date_y, "Set start date", True)

        date_x = (
            content_x + 24 + RADIO_SIZE + RADIO_TEXT_GAP + 68 + DATE_TEXT_GAP
        )
        self.parent.create_text(
            sx(date_x, self.scale),
            sy(start_date_y + RADIO_SIZE / 2 + 4, self.scale),
            text=self.selected_date.strftime("%d.%m.%Y"),
            fill=TEXT_COLOR,
            font=self._scaled_font(RADIO_FONT),
            anchor="w",
            tags=("screen_content",),
        )

        self._draw_calendar(content_x, content_y)

        self._create_main_button(
            content_x, content_y + NAV_BUTTON_Y, "Back", self._back
        )
        self._create_main_button(
            content_x + CONTENT_WIDTH - NAV_BUTTON_WIDTH,
            content_y + NAV_BUTTON_Y,
            "Next",
            self._next,
        )

    def _create_radio_button(self, x, y, value, active):
        image = self.active_radio_image if active else self.passive_radio_image

        if image is not None:
            image_id = self.parent.create_image(
                sx(x, self.scale), sy(y, self.scale),
                image=image, anchor="nw", tags=("screen_content",)
            )
        else:
            image_id = self.parent.create_oval(
                sx(x, self.scale), sy(y, self.scale),
                sx(x + RADIO_SIZE, self.scale), sy(y + RADIO_SIZE, self.scale),
                fill=TEXT_COLOR if active else BACKGROUND_COLOR,
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

        if value == "Today":
            self.parent.tag_bind(
                image_id, "<Button-1>",
                lambda event: self.controller.show_screen("first_backup_date"),
            )
            self.parent.tag_bind(
                text_id, "<Button-1>",
                lambda event: self.controller.show_screen("first_backup_date"),
            )

    def _draw_calendar(self, content_x, content_y):
        calendar_x = content_x + CALENDAR_X
        calendar_y = content_y + CALENDAR_Y
        month_name = calendar.month_name[self.display_month]

        self.parent.create_text(
            sx(calendar_x, self.scale), sy(calendar_y, self.scale),
            text=str(self.display_year), fill=TEXT_COLOR,
            font=self._scaled_font(CALENDAR_HEADER_FONT), anchor="nw",
            tags=("screen_content",),
        )

        header_x = calendar_x + CALENDAR_YEAR_WIDTH + CALENDAR_HEADER_GAP
        left_arrow_x = header_x
        right_arrow_x = (
            header_x + CALENDAR_ARROW_GAP + CALENDAR_MONTH_FIELD_WIDTH + CALENDAR_ARROW_GAP
        )
        month_center_x = (left_arrow_x + right_arrow_x) / 2

        current_month = date.today().replace(day=1)
        displayed_month = date(self.display_year, self.display_month, 1)

        if displayed_month > current_month:
            if self.left_arrow_image is not None:
                left_id = self.parent.create_image(
                    sx(left_arrow_x + CALENDAR_LEFT_ARROW_X, self.scale),
                    sy(calendar_y - 2 + CALENDAR_LEFT_ARROW_Y, self.scale),
                    image=self.left_arrow_image, anchor="nw", tags=("screen_content",)
                )
            else:
                left_id = self.parent.create_text(
                    sx(left_arrow_x + CALENDAR_LEFT_ARROW_X, self.scale),
                    sy(calendar_y + CALENDAR_LEFT_ARROW_Y, self.scale),
                    text="<", fill=TEXT_COLOR,
                    font=self._scaled_font(CALENDAR_HEADER_FONT), anchor="nw",
                    tags=("screen_content",),
                )
            self.parent.tag_bind(left_id, "<Button-1>", lambda event: self._previous_month())

        self.parent.create_text(
            sx(month_center_x + 8, self.scale), sy(calendar_y, self.scale),
            text=month_name, fill=TEXT_COLOR,
            font=self._scaled_font(CALENDAR_HEADER_FONT), anchor="n",
            tags=("screen_content",),
        )

        if self.right_arrow_image is not None:
            right_id = self.parent.create_image(
                sx(right_arrow_x + CALENDAR_RIGHT_ARROW_X, self.scale),
                sy(calendar_y - 2 + CALENDAR_RIGHT_ARROW_Y, self.scale),
                image=self.right_arrow_image, anchor="nw", tags=("screen_content",)
            )
        else:
            right_id = self.parent.create_text(
                sx(right_arrow_x + CALENDAR_RIGHT_ARROW_X, self.scale),
                sy(calendar_y + CALENDAR_RIGHT_ARROW_Y, self.scale),
                text=">", fill=TEXT_COLOR,
                font=self._scaled_font(CALENDAR_HEADER_FONT), anchor="nw",
                tags=("screen_content",),
            )
        self.parent.tag_bind(right_id, "<Button-1>", lambda event: self._next_month())

        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        weekday_y = calendar_y + CALENDAR_HEADER_HEIGHT
        for index, weekday in enumerate(weekdays):
            x = calendar_x + index * CALENDAR_CELL_WIDTH
            self.parent.create_text(
                sx(x, self.scale), sy(weekday_y, self.scale),
                text=weekday, fill=TEXT_COLOR,
                font=self._scaled_font(CALENDAR_FONT), anchor="nw",
                tags=("screen_content",),
            )

        month_matrix = calendar.monthcalendar(self.display_year, self.display_month)
        days_start_y = weekday_y + CALENDAR_WEEKDAY_GAP + 14
        today = date.today()

        for row_index, week in enumerate(month_matrix):
            for col_index, day_number in enumerate(week):
                if day_number == 0:
                    continue

                x = calendar_x + col_index * CALENDAR_CELL_WIDTH
                y = days_start_y + row_index * CALENDAR_CELL_HEIGHT
                current_day = date(self.display_year, self.display_month, day_number)
                is_past = current_day < today

                if current_day == self.selected_date:
                    circle_x_offset = (CALENDAR_CELL_WIDTH - SELECTED_DAY_CIRCLE_SIZE) / 2
                    circle_y_offset = (
                        (CALENDAR_CELL_HEIGHT - SELECTED_DAY_CIRCLE_SIZE) / 2
                        + SELECTED_DAY_CIRCLE_Y
                    )
                    self.parent.create_oval(
                        sx(x + circle_x_offset, self.scale),
                        sy(y + circle_y_offset, self.scale),
                        sx(x + circle_x_offset + SELECTED_DAY_CIRCLE_SIZE, self.scale),
                        sy(y + circle_y_offset + SELECTED_DAY_CIRCLE_SIZE, self.scale),
                        outline=TEXT_COLOR,
                        width=max(1, sx(1, self.scale)),
                        tags=("screen_content",),
                    )

                day_id = self.parent.create_text(
                    sx(x + CALENDAR_CELL_WIDTH / 2, self.scale),
                    sy(y, self.scale),
                    text=str(day_number),
                    fill=DISABLED_COLOR if is_past else TEXT_COLOR,
                    font=self._scaled_font(CALENDAR_FONT),
                    anchor="n",
                    tags=("screen_content",),
                )

                # Past dates are deliberately not bound to a click event.
                if not is_past:
                    self.parent.tag_bind(
                        day_id, "<Button-1>",
                        lambda event, selected=current_day: self._select_date(selected),
                    )

    def _previous_month(self):
        current_month = date.today().replace(day=1)
        displayed_month = date(self.display_year, self.display_month, 1)
        if displayed_month <= current_month:
            return

        if self.display_month == 1:
            self.display_month = 12
            self.display_year -= 1
        else:
            self.display_month -= 1
        self._draw_interface()

    def _next_month(self):
        if self.display_month == 12:
            self.display_month = 1
            self.display_year += 1
        else:
            self.display_month += 1
        self._draw_interface()

    def _select_date(self, selected_date):
        if selected_date < date.today():
            return
        self.selected_date = selected_date
        self.display_month = selected_date.month
        self.display_year = selected_date.year
        self._draw_interface()

    def _create_main_button(self, x, y, text, command):
        create_button(
            self.parent,
            x=x, y=y,
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
        self.controller.state["first_backup_date"] = self.selected_date.strftime("%d.%m.%Y")
        self.controller.show_screen("window6")

    def destroy(self):
        self.parent.delete("screen_content")
