"""Window 7.4: confirmation that setup settings were saved.

This screen is a block on the application's shared Tkinter Canvas.
It does not create a new Tk instance, Canvas, or mainloop.
"""

import tkinter as tk

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
    BODY_FONT,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    sx,
    sy,
    create_button,
)


# Button dimensions and layout use the project's 1400 x 804 design grid.
NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60
TITLE_Y = 28
SAVED_MESSAGE_Y = 240
SCHEDULE_MESSAGE_Y = 310
NAV_BUTTON_Y = 560
TEXT_INSET_X = 0


class SaveAndExitWindow:
    """Confirmation screen with Back and Exit actions."""

    def __init__(
        self,
        root,
        on_exit=None,
        on_back=None,
        parent=None,
        scale=None,
        scheduled_launch_text="",
    ):
        if parent is None:
            raise ValueError(
                "SaveAndExitWindow requires parent=shared Canvas."
            )

        self.root = root
        self.on_exit = on_exit
        self.on_back = on_back
        self.canvas = parent
        self.scale = scale if scale is not None else MAX_SCALE
        self.scheduled_launch_text = scheduled_launch_text
        self._draw_interface()

    def _sx(self, value):
        return sx(value, self.scale)

    def _sy(self, value):
        return sy(value, self.scale)

    def _scaled_font(self, font):
        family, size, *rest = font
        scaled = max(1, int(round(size * self.scale)))
        return (family, scaled, *rest)

    def _draw_interface(self):
        self.canvas.delete("screen_content")

        width = self._sx(DESIGN_WIDTH)
        height = self._sy(DESIGN_HEIGHT)
        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2
        tag = ("screen_content",)

        # Main background and frame.
        self.canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=max(1, self._sx(WINDOW_BORDER_WIDTH)),
            tags=tag,
        )

        # Heading.
        self.canvas.create_text(
            self._sx(content_x + CONTENT_WIDTH / 2),
            self._sy(content_y + TITLE_Y),
            text="Backup Manager",
            fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT),
            anchor="center",
            tags=tag,
        )

        # Confirmation message.
        self.canvas.create_text(
            self._sx(content_x + TEXT_INSET_X),
            self._sy(content_y + SAVED_MESSAGE_Y),
            text="Your settings have been saved.",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
            tags=tag,
        )

        # Optional schedule text. The controller supplies the real value;
        # this screen deliberately does not hard-code a date or time.
        if self.scheduled_launch_text:
            self.canvas.create_text(
                self._sx(content_x + TEXT_INSET_X),
                self._sy(content_y + SCHEDULE_MESSAGE_Y),
                text=self.scheduled_launch_text,
                fill=TEXT_COLOR,
                font=self._scaled_font(BODY_FONT),
                anchor="w",
                tags=tag,
            )

        button_y = content_y + NAV_BUTTON_Y

        # Back on the left, Exit on the right, matching the supplied mockup.
        self._create_button(
            x=content_x,
            y=button_y,
            text="Back",
            command=self._back,
        )
        self._create_button(
            x=content_x + CONTENT_WIDTH - NAV_BUTTON_WIDTH,
            y=button_y,
            text="Exit",
            command=self._exit,
        )

    def _create_button(self, x, y, text, command):
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

    def _back(self):
        """Return to the previous screen without closing the application."""
        if self.on_back is not None:
            self.on_back()

    def _exit(self):
        """Delegate application shutdown to the controller."""
        if self.on_exit is not None:
            self.on_exit()
        else:
            self.root.destroy()

    def destroy(self):
        """Remove this screen's Canvas items, preserving the shared Canvas."""
        if self.canvas is not None:
            self.canvas.delete("screen_content")


# Temporary compatibility alias for a controller that still imports the old name.
UnscheduledBackupWarningWindow = SaveAndExitWindow
