from __future__ import annotations

from gui.gui_style import (
    TEXT_COLOR,
    H1_FONT,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    scale_value,
    create_button,
)


# =========================================================
# WINDOW-SPECIFIC CONTENT AREA
# =========================================================

CONTENT_WIDTH = 480
CONTENT_HEIGHT = 284

BUTTON_WIDTH = 160
BUTTON_HEIGHT = 60

EXIT_X = 0
START_X = 320
BUTTON_Y = 224


class BackupManagerMainWindow:
    """
    GUI Block 8: main window shown after the initial setup.

    The controller owns the Tk root, shared Canvas, and mainloop.
    This class only draws its content on the Canvas supplied as parent.
    """

    def __init__(
        self,
        root,
        on_exit=None,
        on_start=None,
        parent=None,
        scale=1.0,
    ):
        self.root = root
        self.parent = parent
        self.scale = scale

        self.on_exit = on_exit
        self.on_start = on_start

        self._build_screen()

    def _build_screen(self):
        """Draw Window 8 inside the shared Canvas."""

        canvas = self.parent
        if canvas is None:
            raise ValueError(
                "BackupManagerMainWindow requires a parent Canvas."
            )

        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        canvas.create_text(
            scale_value(content_x + CONTENT_WIDTH / 2, self.scale),
            scale_value(content_y + 24, self.scale),
            text="Backup Manager",
            font=(
                H1_FONT[0],
                max(1, scale_value(H1_FONT[1], self.scale)),
                *H1_FONT[2:],
            ),
            fill=TEXT_COLOR,
            anchor="center",
            tags=("screen_content", "window8_content"),
        )

        create_button(
            canvas,
            content_x + EXIT_X,
            content_y + BUTTON_Y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Exit",
            self._exit,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            tag="screen_content window8_exit_button",
        )

        create_button(
            canvas,
            content_x + START_X,
            content_y + BUTTON_Y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Start",
            self._start,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            tag="screen_content window8_start_button",
        )

    def _exit(self):
        """Ask the controller to close the application."""
        if self.on_exit is not None:
            self.on_exit()

    def _start(self):
        """Ask the controller to continue to the backup workflow."""
        if self.on_start is not None:
            self.on_start()

    def destroy(self):
        """Remove Window 8 items from the shared Canvas."""
        if self.parent is not None:
            self.parent.delete("window8_content")
            self.parent.delete("window8_exit_button")
            self.parent.delete("window8_start_button")
