"""Window 13 — user-facing details for a failed backup."""

import tkinter as tk

from gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    H2_FONT,
    H3_FONT,
    BODY_FONT,
    BUTTON_PRIMARY,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    WINDOW_BORDER_WIDTH,
    create_button,
    calculate_scale,
    sx,
    sy,
)

CONTENT_WIDTH = 800
CONTENT_HEIGHT = 640
EXIT_BUTTON_WIDTH = 160
EXIT_BUTTON_HEIGHT = 60
TITLE_Y = 28
SUMMARY_Y = 200
SUMMARY_TEXT_Y = 250
NAV_BUTTON_Y = 560


class ErrorWindow:
    """Window 13, rendered inside the application's shared Canvas."""

    def __init__(
        self,
        root,
        error_file=None,
        reason="The file may be unavailable or access may be restricted.",
        on_back=None,
        on_action=None,
        parent=None,
        scale=None,
        critical=False,
    ):
        self.root = root
        self.error_file = error_file
        self.reason = reason
        self.on_back = on_back
        self.on_action = on_action
        self.critical = critical

        if parent is None:
            # Standalone preview mode for testing the window by itself.
            self.root.title("Backup Manager")
            self.root.configure(bg=BACKGROUND_COLOR)
            self.root.resizable(False, False)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.scale = scale or calculate_scale(
                screen_width - 80, screen_height - 120
            )
            self.canvas = tk.Canvas(
                self.root, bg=BACKGROUND_COLOR, highlightthickness=0, bd=0
            )
            self.canvas.pack(fill="both", expand=True)
            self.root.geometry(
                f"{int(DESIGN_WIDTH * self.scale)}x{int(DESIGN_HEIGHT * self.scale)}"
            )
            self._draw_frame()
        else:
            self.canvas = parent
            self.scale = scale or 1.0

        self._draw_interface()

    def sx(self, value):
        return sx(value, self.scale)

    def sy(self, value):
        return sy(value, self.scale)

    def _scaled_font(self, font):
        if len(font) == 2:
            family, size = font
            return family, max(1, int(round(size * self.scale)))
        family, size, weight = font
        return family, max(1, int(round(size * self.scale))), weight

    def _draw_frame(self):
        width = self.sx(DESIGN_WIDTH)
        height = self.sy(DESIGN_HEIGHT)
        self.canvas.create_rectangle(
            0, 0, width, height, fill=BACKGROUND_COLOR, outline=TEXT_COLOR,
            width=max(1, self.sx(WINDOW_BORDER_WIDTH)), tags=("screen_content",)
        )

    def _text(self, x, y, text, font, anchor="w"):
        self.canvas.create_text(
            self.sx(x), self.sy(y), text=text, fill=TEXT_COLOR,
            font=self._scaled_font(font), anchor=anchor, tags=("screen_content",)
        )

    def _draw_interface(self):
        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        self._text(
            content_x + CONTENT_WIDTH / 2, content_y + TITLE_Y,
            "Backup Manager", H2_FONT, anchor="center"
        )

        if self.critical or not self.error_file:
            self._text(content_x, content_y + SUMMARY_Y,
                       "Critical program error.", H3_FONT)
            self._text(content_x, content_y + SUMMARY_TEXT_Y,
                       "The backup could not be completed.", BODY_FONT)
            self._text(content_x, content_y + SUMMARY_TEXT_Y + 55,
                       "Please contact the developer.", BODY_FONT)
        else:
            self._text(content_x, content_y + SUMMARY_Y,
                       "Backup failed.", H3_FONT)
            self._text(content_x, content_y + SUMMARY_TEXT_Y,
                       "The following file could not be copied:", BODY_FONT)
            self._text(content_x, content_y + SUMMARY_TEXT_Y + 30,
                       self.error_file, BODY_FONT)
            self._text(content_x, content_y + SUMMARY_TEXT_Y + 90,
                       self.reason, BODY_FONT)
            self._text(content_x, content_y + SUMMARY_TEXT_Y + 120,
                       "Ensure that the file is available for copying.", BODY_FONT)

        create_button(
            canvas=self.canvas,
            x=content_x + CONTENT_WIDTH - EXIT_BUTTON_WIDTH,
            y=content_y + NAV_BUTTON_Y,
            width=EXIT_BUTTON_WIDTH,
            height=EXIT_BUTTON_HEIGHT,
            text="Exit",
            command=self._action,
            style=BUTTON_PRIMARY,
            scale=self.scale,
        )

    def _action(self):
        if self.on_action is not None:
            self.on_action()
        else:
            self.root.destroy()

    def destroy(self):
        # All elements are Canvas items; the controller clears screen content.
        pass


def main():
    root = tk.Tk()
    ErrorWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
