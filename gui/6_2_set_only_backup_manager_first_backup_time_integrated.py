import tkinter as tk
from pathlib import Path
from datetime import datetime, timedelta

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
# Window 6.2 — Backup Manager: First backup time
# Time picker version
# ============================================================






# ============================================================
# Fonts
# ============================================================

RADIO_FONT = ("Zen Kaku Gothic Antique", 12)

# Time wheel:
# The center value is deliberately larger than the surrounding
# values, matching the Figma reference.
WHEEL_EDGE_FONT_SIZE = 8
WHEEL_NORMAL_FONT_SIZE = 12
WHEEL_SELECTED_FONT_SIZE = 16

WHEEL_SCROLL_DURATION = 180
WHEEL_SCROLL_FRAME_MS = 16
WHEEL_DRAG_THRESHOLD = 6

# ============================================================
# Radio buttons
# ============================================================

RADIO_SIZE = 20
RADIO_TEXT_GAP = 12
RADIO_ROW_GAP = 48


# ============================================================
# Time wheel
# ============================================================

WHEEL_VISIBLE_ITEMS = 5

WHEEL_ITEM_HEIGHT = 56

WHEEL_CENTER_Y = 300
WHEEL_HOURS_X = 660
WHEEL_MINUTES_X = 780

WHEEL_TEXT_OFFSET_Y = 0

WHEEL_SEPARATOR_X = 1020
WHEEL_SEPARATOR_FONT = ("Zen Kaku Gothic Antique", 16)
WHEEL_SEPARATOR_Y = 380

WHEEL_SCROLL_REGION_TOP = 250
WHEEL_SCROLL_REGION_BOTTOM = 480

# Initial selected time
DEFAULT_HOUR = 9
DEFAULT_MINUTE = 0


# ============================================================
# Navigation buttons
# ============================================================

NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60
NAV_BUTTON_Y = 560


# ============================================================
# Positions
# ============================================================

TITLE_Y = 28

QUESTION_Y = 240
RADIO_START_Y = 270


# ============================================================
# Selected time display
# ============================================================

# This is a display only. The user does not type into it.
# It is updated whenever either wheel changes.
SELECTED_TIME_X = 210
SELECTED_TIME_Y = 300

SELECTED_TIME_FONT = ("Zen Kaku Gothic Antique", 12)
SELECTED_TIME_UNDERLINE_WIDTH = 40
SELECTED_TIME_UNDERLINE_Y = 14

# Distance used for positioning the minute field.
SELECTED_TIME_SEPARATOR_GAP = 20

# Independent horizontal adjustment of ":".
# Negative = move ":" left, positive = move ":" right.
SELECTED_TIME_SEPARATOR_OFFSET_X = -40


# ============================================================
# Radio button images
# ============================================================

IMAGE_DIR = Path(__file__).resolve().parent / "images"

ACTIVE_RADIO_PATH = IMAGE_DIR / "radio_button_active.png"
PASSIVE_RADIO_PATH = IMAGE_DIR / "radio_button_passive.png"


class TimeWheel:
    """
    Continuous cyclic time wheel.

    The wheel has one continuous vertical position instead of a
    one-step visual shift. This is important for mouse dragging:
    while the mouse button is held, the wheel can move through any
    number of values without waiting for mouse release.

    Normally three values are visible:
        previous
        selected
        next

    During movement, the outgoing value leaves through one edge and
    the incoming value enters through the opposite edge.
    """

    def __init__(
        self,
        owner,
        center_x,
        center_y,
        values,
        selected_index,
        wrap=True,
    ):
        self.owner = owner
        self.canvas = owner.canvas

        self.center_x = center_x
        self.center_y = center_y

        self.values = values
        self.wrap = wrap

        self.selected_index = selected_index

        # Continuous position of the selected value.
        # Integer position = perfectly centered value.
        self.position = float(selected_index)

        self.animation_after_id = None
        self.animation_start = 0.0
        self.animation_from = 0.0
        self.animation_to = 0.0
        self.animation_callback = None

        self.drag_start_y = None
        self.drag_start_position = 0.0
        self.drag_wheel_active = False

        self.item_ids = []

        self.draw()

    # ========================================================
    # VALUE
    # ========================================================

    def _value_at_index(self, index):
        if self.wrap:
            index %= len(self.values)
        else:
            if (
                index < 0
                or index >= len(self.values)
            ):
                return None

        return self.values[index]

    # ========================================================
    # FONT SIZE
    # ========================================================

    def _font_size_for_distance(self, distance):
        """
        Three visual sizes:

            0.0  -> large selected value
            1.0  -> small value
            1.5  -> very small edge value
        """

        if distance <= 1.0:
            start = WHEEL_SELECTED_FONT_SIZE
            end = WHEEL_NORMAL_FONT_SIZE
            amount = distance
        else:
            start = WHEEL_NORMAL_FONT_SIZE
            end = WHEEL_EDGE_FONT_SIZE
            amount = min(
                1.0,
                distance - 1.0,
            )

        return max(
            1,
            round(
                start
                + (end - start)
                * amount
            ),
        )

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):
        for item_id in self.item_ids:
            self.canvas.delete(item_id)

        self.item_ids.clear()

        base_index = int(
            self.position // 1
        )

        # A value can enter/leave while moving.
        # At rest, only -1, 0 and +1 are inside the
        # visible region.
        for offset in range(-3, 4):
            absolute_index = (
                base_index
                + offset
            )

            value = self._value_at_index(
                absolute_index
            )

            if value is None:
                continue

            relative_position = (
                absolute_index
                - self.position
            )

            # The visible wheel occupies three rows.
            # During movement, the next/previous value may
            # partially enter at the edge.
            if abs(relative_position) > 2.5:
                continue

            y = (
                self.center_y
                + relative_position
                * WHEEL_ITEM_HEIGHT
                + WHEEL_TEXT_OFFSET_Y
            )

            distance = abs(
                relative_position
            )

            font_size = (
                self._font_size_for_distance(
                    distance
                )
            )

            item_id = self.canvas.create_text(
                self.owner.sx(
                    self.center_x
                ),
                self.owner.sy(y),
                text=f"{value:02d}",
                fill=TEXT_COLOR,
                font=self.owner._scaled_font(("Zen Kaku Gothic Antique", font_size)),
                anchor="center",
            )

            self.item_ids.append(item_id)

    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def scroll(self, direction):
        """
        Scroll exactly one value with smooth animation.

        direction > 0:
            move to previous value

        direction < 0:
            move to next value
        """

        if self.drag_wheel_active:
            return

        if self.animation_after_id is not None:
            return

        current = round(self.position)

        if direction > 0:
            target = current - 1
        else:
            target = current + 1

        self._animate_to(
            target,
            self._finish_animation,
        )

    def _on_mousewheel(self, event):
        if event.delta > 0:
            self.scroll(1)
        else:
            self.scroll(-1)

    # ========================================================
    # SMOOTH ANIMATION
    # ========================================================

    def _animate_to(
        self,
        target,
        callback=None,
    ):
        if self.animation_after_id is not None:
            self.owner.root.after_cancel(
                self.animation_after_id
            )
            self.animation_after_id = None

        import time

        self.animation_from = self.position
        self.animation_to = float(target)
        self.animation_callback = callback
        self.animation_start = (
            time.perf_counter()
        )

        self._animation_frame()

    def _animation_frame(self):
        import time

        elapsed = (
            time.perf_counter()
            - self.animation_start
        )

        duration = (
            WHEEL_SCROLL_DURATION
            / 1000
        )

        progress = min(
            1.0,
            elapsed / duration,
        )

        eased = (
            progress
            * progress
            * (
                3
                - 2 * progress
            )
        )

        self.position = (
            self.animation_from
            + (
                self.animation_to
                - self.animation_from
            )
            * eased
        )

        self.draw()

        if progress < 1.0:
            self.animation_after_id = (
                self.owner.root.after(
                    WHEEL_SCROLL_FRAME_MS,
                    self._animation_frame,
                )
            )
            return

        self.animation_after_id = None
        self.position = self.animation_to

        callback = self.animation_callback
        self.animation_callback = None

        if callback is not None:
            callback()

    def _finish_animation(self):
        selected = round(
            self.position
        )

        if self.wrap:
            selected %= len(
                self.values
            )
        else:
            selected = max(
                0,
                min(
                    len(self.values) - 1,
                    selected,
                ),
            )

        self.selected_index = selected
        self.position = float(selected)

        self.draw()

        self.owner._time_changed()

    # ========================================================
    # DRAG
    # ========================================================

    def begin_drag(self, start_y):
        if self.animation_after_id is not None:
            self.owner.root.after_cancel(
                self.animation_after_id
            )
            self.animation_after_id = None

        self.animation_callback = None

        self.drag_wheel_active = True
        self.drag_start_y = start_y
        self.drag_start_position = (
            self.position
        )

    def drag(self, current_y):
        if not self.drag_wheel_active:
            return

        delta = (
            current_y
            - self.drag_start_y
        )

        self.position = (
            self.drag_start_position
            - delta
            / self.owner.sy(
                WHEEL_ITEM_HEIGHT
            )
        )

        self.draw()

        # Update the logical selected value continuously as the
        # center crosses values. The visual wheel itself remains
        # completely continuous.
        selected = round(
            self.position
        )

        if self.wrap:
            selected %= len(
                self.values
            )
        else:
            selected = max(
                0,
                min(
                    len(self.values) - 1,
                    selected,
                ),
            )

        if selected != self.selected_index:
            self.selected_index = selected
            self.owner._time_changed()

    def end_drag(self):
        if not self.drag_wheel_active:
            return

        self.drag_wheel_active = False
        self.drag_start_y = None

        target = round(
            self.position
        )

        self._animate_to(
            target,
            self._finish_animation,
        )


class FirstBackupTimeWindow:
    """
    Window 6.2 with two vertical time wheels.

    The user does not type the time. Hours and minutes are selected
    by scrolling their respective wheels.
    """

    def __init__(self, parent, controller, scale):
        self.parent = parent
        self.controller = controller
        self.root = controller.root
        self.canvas = parent
        self.scale = scale

        self.active_radio_image = None
        self.passive_radio_image = None

        self.hour_wheel = None
        self.minute_wheel = None

        saved_time = self.controller.state.get("first_backup_time", "")
        self.selected_hour, self.selected_minute = self._get_initial_time(
            saved_time
        )

        self._load_images()
        self._draw_interface()
        self._create_wheels()

    # ========================================================
    # SCALE
    # ========================================================

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
            return (family, max(1, int(round(size * self.scale))))
        family, size, weight = font
        return (family, max(1, int(round(size * self.scale))), weight)

    # ========================================================
    # INITIAL TIME
    # ========================================================

    def _get_initial_time(self, saved_time):
        if saved_time:
            try:
                hour, minute = saved_time.split(":")
                hour = int(hour)
                minute = int(minute)
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    return hour, minute
            except (ValueError, AttributeError):
                pass

        selected_date = self.controller.state.get("first_backup_date", "")
        parsed_date = self._parse_date(selected_date)
        now = datetime.now()

        if parsed_date is not None and parsed_date.date() == now.date():
            target = now + timedelta(minutes=5)
            return target.hour, target.minute

        return DEFAULT_HOUR, DEFAULT_MINUTE

    @staticmethod
    def _parse_date(value):
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

    # ========================================================
    # IMAGES
    # ========================================================

    def _load_images(self):
        if ACTIVE_RADIO_PATH.exists():
            self.active_radio_image = tk.PhotoImage(
                file=str(ACTIVE_RADIO_PATH)
            )

        if PASSIVE_RADIO_PATH.exists():
            self.passive_radio_image = tk.PhotoImage(
                file=str(PASSIVE_RADIO_PATH)
            )

    # ========================================================
    # DRAW
    # ========================================================

    def _draw_interface(self):
        self.canvas.delete("all")

        content_x = (
            DESIGN_WIDTH - CONTENT_WIDTH
        ) / 2

        content_y = (
            DESIGN_HEIGHT - CONTENT_HEIGHT
        ) / 2

        # Border
        self.canvas.create_rectangle(
            0,
            0,
            self.sx(DESIGN_WIDTH),
            self.sy(DESIGN_HEIGHT),
            fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=max(
                1,
                self.sx(WINDOW_BORDER_WIDTH),
            ),
        )

        # Title
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

        # Question
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

        # Set start time — active
        start_time_y = (
            content_y
            + RADIO_START_Y
            + 16
        )

        self._create_radio_button(
            x=content_x + 24,
            y=start_time_y,
            value="Set start time",
            active=True,
        )

        # ----------------------------------------------------
        # Selected time display
        # ----------------------------------------------------

        self._draw_selected_time()

        # Separator between the two time wheels.
        self.canvas.create_text(
            self.sx(WHEEL_SEPARATOR_X),
            self.sy(WHEEL_SEPARATOR_Y),
            text=":",
            fill=TEXT_COLOR,
            font=self._scaled_font(WHEEL_SEPARATOR_FONT),
            anchor="center",
        )

        # Navigation buttons
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
    # WHEELS
    # ========================================================

    def _create_wheels(self):
        content_x = (
            DESIGN_WIDTH - CONTENT_WIDTH
        ) / 2

        content_y = (
            DESIGN_HEIGHT - CONTENT_HEIGHT
        ) / 2

        hour_x = (
            content_x
            + WHEEL_HOURS_X
        )

        minute_x = (
            content_x
            + WHEEL_MINUTES_X
        )

        center_y = (
            content_y
            + WHEEL_CENTER_Y
        )

        self.hour_wheel = TimeWheel(
            owner=self,
            center_x=hour_x,
            center_y=center_y,
            values=list(range(24)),
            selected_index=self.selected_hour,
            wrap=True,
        )

        self.minute_wheel = TimeWheel(
            owner=self,
            center_x=minute_x,
            center_y=center_y,
            values=list(range(60)),
            selected_index=self.selected_minute,
            wrap=True,
        )

        self._bind_wheel_regions()

    def _bind_wheel_regions(self):
        self.canvas.bind(
            "<MouseWheel>",
            self._on_mousewheel,
        )

        self.canvas.bind(
            "<ButtonPress-1>",
            self._on_wheel_press,
        )

        self.canvas.bind(
            "<B1-Motion>",
            self._on_wheel_drag,
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self._on_wheel_release,
        )

        self.drag_wheel = None

    def _wheel_at(self, x, y):
        design_x = x / self.scale
        design_y = y / self.scale

        if not (
            WHEEL_SCROLL_REGION_TOP
            <= design_y
            <= WHEEL_SCROLL_REGION_BOTTOM
        ):
            return None

        for wheel in (
            self.hour_wheel,
            self.minute_wheel,
        ):
            if wheel is None:
                continue

            if (
                wheel.center_x - 75
                <= design_x
                <= wheel.center_x + 75
            ):
                return wheel

        return None

    def _on_mousewheel(self, event):
        wheel = self._wheel_at(
            event.x,
            event.y,
        )

        if wheel is None:
            return

        wheel._on_mousewheel(event)

    def _on_wheel_press(self, event):
        wheel = self._wheel_at(
            event.x,
            event.y,
        )

        if wheel is None:
            self.drag_wheel = None
            return

        self.drag_wheel = wheel
        wheel.begin_drag(event.y)

    def _on_wheel_drag(self, event):
        if self.drag_wheel is None:
            return

        self.drag_wheel.drag(event.y)

    def _on_wheel_release(self, event):
        if self.drag_wheel is None:
            return

        wheel = self.drag_wheel
        self.drag_wheel = None

        wheel.end_drag()

    def _time_changed(self):
        self.selected_hour = (
            self.hour_wheel.values[
                self.hour_wheel.selected_index
            ]
        )

        self.selected_minute = (
            self.minute_wheel.values[
                self.minute_wheel.selected_index
            ]
        )

        # The selected time shown beside "Set start time"
        # always follows the wheel selection.
        self._draw_selected_time()

    # ========================================================
    # SELECTED TIME DISPLAY
    # ========================================================

    def _draw_selected_time(self):
        # Remove only the display values, not the wheels.
        self.canvas.delete("selected_time")

        content_x = (
            DESIGN_WIDTH - CONTENT_WIDTH
        ) / 2

        content_y = (
            DESIGN_HEIGHT - CONTENT_HEIGHT
        ) / 2

        selected_time_x = (
            content_x
            + SELECTED_TIME_X
        )

        selected_time_y = (
            content_y
            + SELECTED_TIME_Y
        )

        hour_display_x = selected_time_x

        separator_display_x = (
            hour_display_x
            + SELECTED_TIME_UNDERLINE_WIDTH
            + SELECTED_TIME_SEPARATOR_GAP
            + SELECTED_TIME_SEPARATOR_OFFSET_X
        )

        minute_display_x = (
            separator_display_x
            + SELECTED_TIME_SEPARATOR_GAP
        )

        self.canvas.create_text(
            self.sx(hour_display_x),
            self.sy(selected_time_y),
            text=f"{self.selected_hour:02d}",
            fill=TEXT_COLOR,
            font=self._scaled_font(SELECTED_TIME_FONT),
            anchor="center",
            tags=("selected_time",),
        )

        self.canvas.create_text(
            self.sx(separator_display_x),
            self.sy(selected_time_y),
            text=":",
            fill=TEXT_COLOR,
            font=self._scaled_font(SELECTED_TIME_FONT),
            anchor="center",
            tags=("selected_time",),
        )

        self.canvas.create_text(
            self.sx(minute_display_x),
            self.sy(selected_time_y),
            text=f"{self.selected_minute:02d}",
            fill=TEXT_COLOR,
            font=self._scaled_font(SELECTED_TIME_FONT),
            anchor="center",
            tags=("selected_time",),
        )

        self.canvas.create_line(
            self.sx(
                hour_display_x
                - SELECTED_TIME_UNDERLINE_WIDTH / 2
            ),
            self.sy(
                selected_time_y
                + SELECTED_TIME_UNDERLINE_Y
            ),
            self.sx(
                hour_display_x
                + SELECTED_TIME_UNDERLINE_WIDTH / 2
            ),
            self.sy(
                selected_time_y
                + SELECTED_TIME_UNDERLINE_Y
            ),
            fill=TEXT_COLOR,
            width=max(1, self.sx(1)),
            tags=("selected_time",),
        )

        self.canvas.create_line(
            self.sx(
                minute_display_x
                - SELECTED_TIME_UNDERLINE_WIDTH / 2
            ),
            self.sy(
                selected_time_y
                + SELECTED_TIME_UNDERLINE_Y
            ),
            self.sx(
                minute_display_x
                + SELECTED_TIME_UNDERLINE_WIDTH / 2
            ),
            self.sy(
                selected_time_y
                + SELECTED_TIME_UNDERLINE_Y
            ),
            fill=TEXT_COLOR,
            width=max(1, self.sx(1)),
            tags=("selected_time",),
        )

    # ========================================================
    # RADIO BUTTON
    # ========================================================

    def _create_radio_button(
        self,
        x,
        y,
        value,
        active,
        command=None,
    ):
        tag = f"radio_{value}"

        image = (
            self.active_radio_image
            if active
            else self.passive_radio_image
        )

        if image is not None:
            self.canvas.create_image(
                self.sx(x),
                self.sy(y),
                image=image,
                anchor="nw",
                tags=(tag,),
            )
        else:
            self.canvas.create_oval(
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
                tags=(tag,),
            )

        self.canvas.create_text(
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
            tags=(tag,),
        )


        if command is not None:
            self.canvas.tag_bind(
                tag,
                "<Button-1>",
                command,
            )

    # ========================================================
    # BUTTONS
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

    # ========================================================
    # ACTIONS
    # ========================================================

    def _back(self):
        self.controller.return_to_window_6_1()

    def _next(self):
        self._time_changed()

        selected_time = (
            f"{self.selected_hour:02d}:"
            f"{self.selected_minute:02d}"
        )

        self.controller.next_from_window_6_2(selected_time)

    def destroy(self):
        self.canvas.unbind("<MouseWheel>")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")


