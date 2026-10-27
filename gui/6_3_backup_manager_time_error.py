import tkinter as tk
from datetime import datetime

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    H3_FONT,
    BODY_FONT,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    WINDOW_BORDER_WIDTH,
    WINDOW_BORDER_COLOR,
    MAX_SCALE,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    calculate_scale,
    scale_value,
    create_button,
)


# ============================================================
# Window 2.1 — Backup Manager: Error path
# ============================================================
#
# IMPORTANT:
# The Figma frame is used for geometry/layout only.
# Colors, fonts and button styling come from gui_style.py.
# ============================================================

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 360

TITLE_Y = 82
MESSAGE_Y = 145

BUTTON_WIDTH = 160
BUTTON_HEIGHT = 60
BUTTON_X = (WINDOW_WIDTH - BUTTON_WIDTH) / 2
BUTTON_Y = 212


class ErrorPathWindow:
    """Styled modal error window for an invalid path."""

    def __init__(
        self,
        root,
        title="Ensure the timing is correct",
        message=None,
        on_ok=None,
    ):
        self.root = root
        self.title_text = title

        # Show the actual current system time.
        if message is None:
            current_time = datetime.now().strftime("%H:%M")
            self.message_text = f"The current time is {current_time}."
        else:
            self.message_text = message

        self.on_ok = on_ok

        self.window = tk.Toplevel(root)
        self.window.withdraw()

        self.window.title("Backup Manager")
        self.window.configure(bg=BACKGROUND_COLOR)
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self._ok)

        self.scale = self._calculate_scale()

        self.canvas = tk.Canvas(
            self.window,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self._update_geometry()
        self._make_modal()
        self.window.deiconify()

    # --------------------------------------------------------
    # Window setup
    # --------------------------------------------------------

    def _calculate_scale(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        return calculate_scale(
            screen_width - 80,
            screen_height - 120,
            max_scale=MAX_SCALE,
        )

    def _scaled_font(self, font_spec):
        family = font_spec[0]
        size = int(font_spec[1])
        rest = tuple(font_spec[2:])
        return (
            family,
            max(1, scale_value(size, self.scale)),
            *rest,
        )

    def _update_geometry(self):
        width = scale_value(WINDOW_WIDTH, self.scale)
        height = scale_value(WINDOW_HEIGHT, self.scale)

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.update_idletasks()

        self._draw_interface()

    # --------------------------------------------------------
    # Interface
    # --------------------------------------------------------

    def _draw_interface(self):
        self.canvas.delete("all")

        width = scale_value(WINDOW_WIDTH, self.scale)
        height = scale_value(WINDOW_HEIGHT, self.scale)

        # Same project background and border as the main GUI.
        self.canvas.create_rectangle(
            scale_value(WINDOW_BORDER_WIDTH / 2, self.scale),
            scale_value(WINDOW_BORDER_WIDTH / 2, self.scale),
            width - scale_value(WINDOW_BORDER_WIDTH / 2, self.scale),
            height - scale_value(WINDOW_BORDER_WIDTH / 2, self.scale),
            fill=BACKGROUND_COLOR,
            outline=WINDOW_BORDER_COLOR,
            width=max(
                1,
                scale_value(WINDOW_BORDER_WIDTH, self.scale),
            ),
        )

        # Error title.
        self.canvas.create_text(
            scale_value(WINDOW_WIDTH / 2, self.scale),
            scale_value(TITLE_Y, self.scale),
            text=self.title_text,
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="center",
        )

        # Error message.
        self.canvas.create_text(
            scale_value(WINDOW_WIDTH / 2, self.scale),
            scale_value(MESSAGE_Y, self.scale),
            text=self.message_text,
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="center",
        )

        # Project button style.
        create_button(
            self.canvas,
            BUTTON_X,
            BUTTON_Y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "OK",
            self._ok,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            tag="window2_1_ok_button",
        )

    # --------------------------------------------------------
    # Modal behavior
    # --------------------------------------------------------

    def _make_modal(self):
        self.window.transient(self.root)
        self.window.grab_set()
        self.window.focus_force()

    def _ok(self):
        """
        Close the modal error window and then notify the controller.

        When an on_ok callback is supplied, the previous implementation
        released the grab and called the callback but never destroyed the
        Toplevel window. The modal window therefore remained visible.
        """

        try:
            self.window.grab_release()
        except tk.TclError:
            pass

        callback = self.on_ok

        # Always destroy the modal window.
        self.destroy()

        # Continue the controller's flow after the dialog is closed.
        if callback is not None:
            callback()

    def destroy(self):
        try:
            self.window.grab_release()
        except tk.TclError:
            pass

        if self.window.winfo_exists():
            self.window.destroy()


# ------------------------------------------------------------
# Standalone visual preview
# ------------------------------------------------------------

def main():
    root = tk.Tk()
    root.withdraw()

    ErrorPathWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
