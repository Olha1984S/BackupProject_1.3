from __future__ import annotations

from gui.gui_style import (
    BACKGROUND_COLOR,
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
INSTALL_X = 320
BUTTON_Y = 224


class BackupManagerStartWindow:
    """
    GUI Block 1.

    This block does NOT create:
        - tk.Tk()
        - another main window
        - another Canvas
        - mainloop()

    The controller owns the main application window and Canvas.
    """

    def __init__(
        self,
        root,
        on_exit=None,
        on_install=None,
        parent=None,
        scale=1.0,
    ):
        self.root = root
        self.parent = parent
        self.scale = scale

        self.on_exit = on_exit
        self.on_install = on_install

        self._build_screen()

    # =========================================================
    # BUILD SCREEN
    # =========================================================

    def _build_screen(self):
        """
        Draw Window 1 inside the Canvas supplied by the controller.
        """

        canvas = self.parent

        if canvas is None:
            raise ValueError(
                "BackupManagerStartWindow requires a parent Canvas."
            )

        # -----------------------------------------------------
        # CONTENT POSITION
        # -----------------------------------------------------

        content_x = (
            DESIGN_WIDTH - CONTENT_WIDTH
        ) / 2

        content_y = (
            DESIGN_HEIGHT - CONTENT_HEIGHT
        ) / 2

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        canvas.create_text(
            scale_value(
                content_x + CONTENT_WIDTH / 2,
                self.scale,
            ),
            scale_value(
                content_y + 24,
                self.scale,
            ),
            text="Backup Manager",
            font=(
                H1_FONT[0],
                max(
                    1,
                    scale_value(
                        H1_FONT[1],
                        self.scale,
                    ),
                ),
                *H1_FONT[2:],
            ),
            fill=TEXT_COLOR,
            anchor="center",
            tags=("screen_content", "window1_content"),
        )

        # -----------------------------------------------------
        # EXIT BUTTON
        # -----------------------------------------------------

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
            tag="screen_content window1_exit_button",
        )

        # -----------------------------------------------------
        # INSTALL BUTTON
        # -----------------------------------------------------

        create_button(
            canvas,
            content_x + INSTALL_X,
            content_y + BUTTON_Y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Install",
            self._install,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            tag="screen_content window1_install_button",
        )

    # =========================================================
    # BUTTON ACTIONS
    # =========================================================

    def _exit(self):
        """
        Exit the application through the controller.
        """

        if self.on_exit is not None:
            self.on_exit()

    def _install(self):
        """
        Continue to GUI Block 2 through the controller.
        """

        if self.on_install is not None:
            self.on_install()

    # =========================================================
    # DESTROY
    # =========================================================

    def destroy(self):
        """
        Remove Window 1 content from the shared Canvas.
        """

        if self.parent is not None:
            self.parent.delete("window1_content")
            self.parent.delete("window1_exit_button")
            self.parent.delete("window1_install_button")