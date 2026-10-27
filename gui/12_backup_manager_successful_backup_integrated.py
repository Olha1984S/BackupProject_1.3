import tkinter as tk

from gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    WINDOW_BORDER_WIDTH,
    MAX_SCALE,
    H2_FONT,
    H3_FONT,
    BODY_FONT,
    BUTTON_PRIMARY,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    create_button,
    sx,
    sy,
)

# Window-specific geometry, in design coordinates.
CONTENT_WIDTH = 800
CONTENT_HEIGHT = 640
EXIT_BUTTON_WIDTH = 160
EXIT_BUTTON_HEIGHT = 60
TITLE_Y = 28
SUMMARY_LABEL_X = 0
SUMMARY_VALUE_X = 150
SUMMARY_Y = 230
SUMMARY_LINE_GAP = 36
EXIT_BUTTON_X = 0
EXIT_BUTTON_Y = 560

DEFAULT_FILES_COPIED = "—"
DEFAULT_BACKUP_SIZE = "—"


class CompletingSetupWindow:
    """Window 12 — successful backup summary, using the shared Canvas."""

    def __init__(self, root, parent, scale=MAX_SCALE,
                 files_copied=DEFAULT_FILES_COPIED,
                 backup_size=DEFAULT_BACKUP_SIZE,
                 on_back=None, on_action=None):
        self.root = root
        self.canvas = parent
        self.scale = scale
        self.files_copied = files_copied
        self.backup_size = backup_size
        self.on_back = on_back
        self.on_action = on_action
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

    def _draw_interface(self):
        self.canvas.delete("all")
        width = self.sx(DESIGN_WIDTH)
        height = self.sy(DESIGN_HEIGHT)
        self.canvas.create_rectangle(
            0, 0, width, height,
            fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=max(1, self.sx(WINDOW_BORDER_WIDTH)),
        )
        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        self.canvas.create_text(
            self.sx(content_x + CONTENT_WIDTH / 2),
            self.sy(content_y + TITLE_Y),
            text="Backup Manager",
            fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT),
            anchor="center",
        )
        self.canvas.create_text(
            self.sx(content_x + SUMMARY_LABEL_X),
            self.sy(content_y + SUMMARY_Y),
            text="Backup completed successfully",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
        )

        rows = [
            ("Files copied:", self.files_copied),
            ("Backup size:", self.backup_size),
        ]
        for index, (label, value) in enumerate(rows, start=1):
            y = content_y + SUMMARY_Y + index * SUMMARY_LINE_GAP
            self.canvas.create_text(
                self.sx(content_x + SUMMARY_LABEL_X), self.sy(y),
                text=label, fill=TEXT_COLOR,
                font=self._scaled_font(BODY_FONT), anchor="w",
            )
            self.canvas.create_text(
                self.sx(content_x + SUMMARY_VALUE_X), self.sy(y),
                text=str(value), fill=TEXT_COLOR,
                font=self._scaled_font(BODY_FONT), anchor="w",
            )

        # The mockup places Exit below the summary, aligned with its left edge.
        create_button(
            canvas=self.canvas,
            x=content_x + EXIT_BUTTON_X,
            y=content_y + EXIT_BUTTON_Y,
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


def main():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=int(DESIGN_WIDTH * MAX_SCALE),
                       height=int(DESIGN_HEIGHT * MAX_SCALE),
                       bg=BACKGROUND_COLOR, highlightthickness=0, bd=0)
    canvas.pack()
    CompletingSetupWindow(root, canvas, scale=MAX_SCALE)
    root.mainloop()


if __name__ == "__main__":
    main()
