import tkinter as tk

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    H3_FONT,
    BODY_FONT,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    WINDOW_BORDER_WIDTH,
    MAX_SCALE,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    calculate_scale,
    scale_value,
    create_button,
)


# ============================================================
# Window 7.3 — Backup Manager: Timeout warning
# ============================================================
#
# IMPORTANT:
# The Figma frame is used for geometry/layout only.
# Colors, fonts and button styling come from gui_style.py.
# ============================================================

WINDOW_WIDTH = 810
WINDOW_HEIGHT = 356

TITLE_Y = 82
MESSAGE_Y = 145

BUTTON_WIDTH = 160
BUTTON_HEIGHT = 60
BUTTON_X = (WINDOW_WIDTH - BUTTON_WIDTH) / 2
BUTTON_Y = 212


class TimeoutWarningWindow:
    """Styled modal warning window for an expired scheduling window."""

    def __init__(
        self,
        root,
        title="The timeout period has expired.",
        message="Change the program's automatic startup time.",
        on_ok=None,
    ):
        self.root = root
        self.title_text = title
        self.message_text = message
        self.on_ok = on_ok

        self.window = tk.Toplevel(root)
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
            outline=TEXT_COLOR,
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
            tag="window7_3_ok_button",
        )

    # --------------------------------------------------------
    # Modal behavior
    # --------------------------------------------------------

    def _make_modal(self):
        self.window.transient(self.root)
        self.window.grab_set()
        self.window.focus_force()

    def _ok(self):
        try:
            self.window.grab_release()
        except tk.TclError:
            pass

        callback = self.on_ok
        self.destroy()
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
    # Standalone preview: use the dialog as the main Tk window
    # so it stays visible when this file is run directly.
    root = tk.Tk()
    root.title("Backup Manager")
    root.configure(bg=BACKGROUND_COLOR)
    root.resizable(False, False)

    scale = calculate_scale(
        root.winfo_screenwidth() - 80,
        root.winfo_screenheight() - 120,
        max_scale=MAX_SCALE,
    )

    width = scale_value(WINDOW_WIDTH, scale)
    height = scale_value(WINDOW_HEIGHT, scale)

    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

    canvas = tk.Canvas(
        root,
        bg=BACKGROUND_COLOR,
        highlightthickness=0,
        bd=0,
    )
    canvas.pack(fill="both", expand=True)

    def scaled_font(font_spec):
        family = font_spec[0]
        size = int(font_spec[1])
        rest = tuple(font_spec[2:])
        return (
            family,
            max(1, scale_value(size, scale)),
            *rest,
        )

    canvas.create_rectangle(
        scale_value(WINDOW_BORDER_WIDTH / 2, scale),
        scale_value(WINDOW_BORDER_WIDTH / 2, scale),
        width - scale_value(WINDOW_BORDER_WIDTH / 2, scale),
        height - scale_value(WINDOW_BORDER_WIDTH / 2, scale),
        fill=BACKGROUND_COLOR,
        outline=TEXT_COLOR,
        width=max(1, scale_value(WINDOW_BORDER_WIDTH, scale)),
    )

    canvas.create_text(
        scale_value(WINDOW_WIDTH / 2, scale),
        scale_value(TITLE_Y, scale),
        text="The timeout period has expired.",
        fill=TEXT_COLOR,
        font=scaled_font(H3_FONT),
        anchor="center",
    )

    canvas.create_text(
        scale_value(WINDOW_WIDTH / 2, scale),
        scale_value(MESSAGE_Y, scale),
        text="Change the program's automatic startup time.",
        fill=TEXT_COLOR,
        font=scaled_font(BODY_FONT),
        anchor="center",
    )

    create_button(
        canvas,
        BUTTON_X,
        BUTTON_Y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "OK",
        root.destroy,
        style=BUTTON_PRIMARY,
        scale=scale,
        anchor=BUTTON_ANCHOR_LEFT,
        tag="window7_3_ok_button",
    )

    root.mainloop()


if __name__ == "__main__":
    main()
