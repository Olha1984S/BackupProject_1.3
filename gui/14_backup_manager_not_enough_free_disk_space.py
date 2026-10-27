import tkinter as tk

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
    BODY_FONT,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    calculate_scale,
    sx,
    sy,
    create_button,
)


# ============================================================
# Backup Manager — insufficient free disk space
# ============================================================

BUTTON_WIDTH = 160
BUTTON_HEIGHT = 60

TITLE_Y = 28

WARNING_Y = 220
MESSAGE_Y = 270
REQUIRED_Y = 306
AVAILABLE_Y = 342

NAV_BUTTON_Y = 560
EXIT_BUTTON_X = 0

DEFAULT_REQUIRED_SPACE = "XXXXX"
DEFAULT_AVAILABLE_SPACE = "XXXXX"


class NotEnoughFreeDiskSpaceWindow:
    """Window 14 — warning about insufficient free disk space.

    This is a GUI block for the application's shared Canvas.
    The controller owns the root window, Canvas, screen changes,
    and button callbacks.
    """

    def __init__(
        self,
        parent,
        controller,
        scale,
        required_space=DEFAULT_REQUIRED_SPACE,
        available_space=DEFAULT_AVAILABLE_SPACE,
        on_exit=None,
        on_continue=None,
    ):
        self.root = controller.root
        self.controller = controller
        self.parent = parent
        self.canvas = parent
        self.scale = scale

        self.required_space = required_space
        self.available_space = available_space

        self.on_exit = on_exit
        self.on_continue = on_continue

        self._draw_interface()

    # ========================================================
    # SCALE / COORDINATE CONVERSION
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

    def destroy(self):
        # The Canvas and root window belong to the controller.
        # This GUI block creates no independent widgets or callbacks.
        pass

    # ========================================================
    # INTERFACE
    # ========================================================

    def _draw_interface(self):
        self.canvas.delete("all")

        width = self.sx(DESIGN_WIDTH)
        height = self.sy(DESIGN_HEIGHT)

        self.canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=max(1, self.sx(WINDOW_BORDER_WIDTH)),
        )

        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.canvas.create_text(
            self.sx(content_x + CONTENT_WIDTH / 2),
            self.sy(content_y + TITLE_Y),
            text="Backup Manager",
            fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT),
            anchor="center",
        )

        # ----------------------------------------------------
        # Warning
        # ----------------------------------------------------

        self.canvas.create_text(
            self.sx(content_x),
            self.sy(content_y + WARNING_Y),
            text="Warning",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
        )

        self.canvas.create_text(
            self.sx(content_x),
            self.sy(content_y + MESSAGE_Y),
            text="Not enough free disk space.",
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
        )

        self.canvas.create_text(
            self.sx(content_x),
            self.sy(content_y + REQUIRED_Y),
            text="Required:",
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
        )

        self.canvas.create_text(
            self.sx(content_x + 150),
            self.sy(content_y + REQUIRED_Y),
            text=str(self.required_space),
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
        )

        self.canvas.create_text(
            self.sx(content_x),
            self.sy(content_y + AVAILABLE_Y),
            text="Available:",
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
        )

        self.canvas.create_text(
            self.sx(content_x + 150),
            self.sy(content_y + AVAILABLE_Y),
            text=str(self.available_space),
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
        )

        # ----------------------------------------------------
        # Navigation buttons
        # ----------------------------------------------------

        self._create_button(
            x=content_x + EXIT_BUTTON_X,
            y=content_y + NAV_BUTTON_Y,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Exit",
            command=self._exit,
        )

        self._create_button(
            x=content_x + CONTENT_WIDTH - BUTTON_WIDTH,
            y=content_y + NAV_BUTTON_Y,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Continue",
            command=self._continue,
        )

    # ========================================================
    # BUTTON
    # ========================================================

    def _create_button(self, x, y, width, height, text, command):
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
        )

    # ========================================================
    # ACTIONS
    # ========================================================

    def _exit(self):
        if self.on_exit is not None:
            self.on_exit()
        elif hasattr(self.controller, "exit_application"):
            self.controller.exit_application()
        else:
            self.root.destroy()

    def _continue(self):
        if self.on_continue is not None:
            self.on_continue()


# ============================================================
# Standalone test note
# ============================================================

if __name__ == "__main__":
    print(
        "Window 14 is a GUI block and must be launched by the "
        "BackupProject 1.3 controller."
    )
