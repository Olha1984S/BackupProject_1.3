import tkinter as tk
from pathlib import Path

from gui_style import (
    BACKGROUND_COLOR, TEXT_COLOR, DESIGN_WIDTH, DESIGN_HEIGHT,
    CONTENT_WIDTH, CONTENT_HEIGHT, WINDOW_BORDER_WIDTH, H2_FONT,
    H3_FONT, BODY_FONT, BUTTON_PRIMARY, BUTTON_ANCHOR_LEFT,
    create_button,
)

BUTTON_HEIGHT = 60
EXIT_BUTTON_WIDTH = 200
CONTINUE_BUTTON_WIDTH = 280
TITLE_Y = 28
STATUS_Y = 190
MESSAGE_Y = 250
BUTTON_Y = 500
ANIMATION_INTERVAL_MS = 140
POINT_COUNT = 5
POINT_STEP_PX = 12
POINTS_X_OFFSET = 100


class StoppingWindow:
    """Window 11: wait for a safe operation boundary, or resume the backup."""

    def __init__(self, root, parent, scale=0.5,
                 on_continue=None, on_exit=None):
        self.root = root
        self.canvas = parent
        self.scale = scale
        self.on_continue = on_continue
        self.on_exit = on_exit
        self.operation_completed_state = False
        self._animation_job = None
        self._active_point_index = 0
        assets_dir = Path(__file__).resolve().parent / "images"
        self._active_point = tk.PhotoImage(file=str(assets_dir / "active_point.png"))
        self._passive_point = tk.PhotoImage(file=str(assets_dir / "passive_point.png"))
        self._point_images = []
        self._draw_interface()
        self._schedule_animation()

    def sx(self, value):
        return int(round(value * self.scale))

    def sy(self, value):
        return int(round(value * self.scale))

    def _scaled_font(self, font):
        if len(font) == 2:
            family, size = font
            return family, max(1, int(round(size * self.scale)))
        family, size, weight = font
        return family, max(1, int(round(size * self.scale))), weight

    def _draw_interface(self):
        self.canvas.delete("all")
        width, height = self.sx(DESIGN_WIDTH), self.sy(DESIGN_HEIGHT)
        self.canvas.create_rectangle(
            0, 0, width, height, fill=BACKGROUND_COLOR, outline=TEXT_COLOR,
            width=max(1, self.sx(WINDOW_BORDER_WIDTH)),
        )
        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2
        self.canvas.create_text(
            self.sx(content_x + CONTENT_WIDTH / 2), self.sy(content_y + TITLE_Y),
            text="Backup Manager", fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT), anchor="center",
        )
        if self.operation_completed_state:
            self._draw_ready(content_x, content_y)
        else:
            self._draw_waiting(content_x, content_y)

    def _draw_waiting(self, content_x, content_y):
        self.canvas.create_text(
            self.sx(content_x), self.sy(content_y + STATUS_Y),
            text="Status: Stopping...", fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT), anchor="w",
        )
        self.canvas.create_text(
            self.sx(content_x), self.sy(content_y + MESSAGE_Y),
            text="Finishing the current operation.", fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT), anchor="w",
        )
        wait_y = content_y + MESSAGE_Y + 36
        self.canvas.create_text(
            self.sx(content_x), self.sy(wait_y),
            text="Please wait", fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT), anchor="w",
        )
        self._draw_animated_points(content_x, wait_y)
        self._create_button(content_x, content_y + BUTTON_Y, "Exit", None,
                            enabled=False, width=EXIT_BUTTON_WIDTH)
        self._create_button(
            content_x + CONTENT_WIDTH - CONTINUE_BUTTON_WIDTH,
            content_y + BUTTON_Y, "Continue", self._continue,
            width=CONTINUE_BUTTON_WIDTH,
        )

    def _draw_ready(self, content_x, content_y):
        self.canvas.create_text(
            self.sx(content_x), self.sy(content_y + STATUS_Y),
            text="Status: Stopping...", fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT), anchor="w",
        )
        self.canvas.create_text(
            self.sx(content_x), self.sy(content_y + MESSAGE_Y),
            text="The current operation has been safely completed.",
            fill=TEXT_COLOR, font=self._scaled_font(BODY_FONT), anchor="w",
        )
        self.canvas.create_text(
            self.sx(content_x), self.sy(content_y + MESSAGE_Y + 36),
            text="You can now exit the program or continue the backup.",
            fill=TEXT_COLOR, font=self._scaled_font(BODY_FONT), anchor="w",
        )
        self._create_button(content_x, content_y + BUTTON_Y, "Exit", self._exit,
                            width=EXIT_BUTTON_WIDTH)
        self._create_button(
            content_x + CONTENT_WIDTH - CONTINUE_BUTTON_WIDTH,
            content_y + BUTTON_Y, "Continue", self._continue,
            width=CONTINUE_BUTTON_WIDTH,
        )

    def _create_button(self, x, y, text, command, enabled=True, width=160):
        create_button(
            self.canvas, x=x, y=y, width=width, height=BUTTON_HEIGHT,
            text=text, command=command, style=BUTTON_PRIMARY,
            scale=self.scale, anchor=BUTTON_ANCHOR_LEFT,
            state="normal" if enabled else "disabled",
        )

    def _draw_animated_points(self, content_x, wait_y):
        """Draw ten 4x4 PNG dots; one active dot moves from left to right."""
        self._point_images = []
        for index in range(POINT_COUNT):
            image = self._active_point if index == self._active_point_index else self._passive_point
            self._point_images.append(image)
            x = self.sx(content_x + POINTS_X_OFFSET) + index * POINT_STEP_PX
            # Slight downward optical correction to align the smaller icons
            # with the visual center of the "Please wait" text.
            y = self.sy(wait_y + 4)
            self.canvas.create_image(x, y, image=image, anchor="w")

    def _schedule_animation(self):
        if self.operation_completed_state:
            return
        self._animation_job = self.root.after(
            ANIMATION_INTERVAL_MS, self._tick_animation
        )

    def _tick_animation(self):
        self._animation_job = None
        if self.operation_completed_state:
            return
        self._active_point_index = (self._active_point_index + 1) % POINT_COUNT
        self._draw_interface()
        self._schedule_animation()

    def operation_completed(self):
        """Called by the controller only after the backend confirms a safe boundary."""
        if self.operation_completed_state:
            return
        self.operation_completed_state = True
        if self._animation_job is not None:
            try:
                self.root.after_cancel(self._animation_job)
            except tk.TclError:
                pass
            self._animation_job = None
        self._draw_interface()

    def _continue(self):
        if self.on_continue is not None:
            self.on_continue()

    def _exit(self):
        if self.operation_completed_state and self.on_exit is not None:
            self.on_exit()

    def destroy(self):
        """Cancel the countdown callback when this screen is removed."""
        if self._animation_job is not None:
            try:
                self.root.after_cancel(self._animation_job)
            except tk.TclError:
                pass
            self._animation_job = None
