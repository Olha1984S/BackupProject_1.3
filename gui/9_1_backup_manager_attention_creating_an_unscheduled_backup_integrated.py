import tkinter as tk
from pathlib import Path

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
    calculate_scale,
    sx,
    sy,
    create_button,
)


# ============================================================
# Backup Manager — Attention: Creating an unscheduled backup
# ============================================================

# ============================================================
# Warning block
# ============================================================

WARNING_ICON_WIDTH = 40
WARNING_ICON_HEIGHT = 35
WARNING_TEXT_GAP = 14

# warning_icon.svg is kept in gui/images/.
# Tkinter does not display SVG directly, so the SVG is converted
# once to PNG and the PNG is used by PhotoImage.
ICON_DIR = Path(__file__).resolve().parent / "images"
WARNING_ICON_PNG = ICON_DIR / "warning_icon.png"


# ============================================================
# Main navigation buttons
# ============================================================

NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60


# ============================================================
# Positions
# ============================================================

TITLE_Y = 28

WARNING_TITLE_Y = 240
WARNING_MESSAGE_Y = 310

NAV_BUTTON_Y = 560


class UnscheduledBackupWarningWindow:
    """Warning shown before starting an unscheduled backup."""

    def __init__(
        self,
        root,
        on_exit=None,
        on_back=None,
        on_start=None,
        parent=None,
        scale=None,
    ):
        """Build this screen on the application's shared Canvas."""
        if parent is None:
            raise ValueError(
                "UnscheduledBackupWarningWindow requires parent=shared Canvas."
            )

        self.root = root
        self.on_exit = on_exit
        self.on_back = on_back
        self.on_start = on_start
        self.canvas = parent
        self.scale = scale if scale is not None else MAX_SCALE
        self.warning_icon = None

        self._prepare_warning_icon()
        self._draw_interface()

    # ========================================================
    # SCALE
    # ========================================================

    def _calculate_scale(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        available_width = screen_width - 80
        available_height = screen_height - 120

        return calculate_scale(
            available_width,
            available_height,
            max_scale=MAX_SCALE,
        )

    def sx(self, value):
        return sx(value, self.scale)

    def sy(self, value):
        return sy(value, self.scale)

    def _scaled_font(self, font):
        if len(font) == 2:
            family, size = font
            return (
                family,
                max(1, int(round(size * self.scale))),
            )

        family, size, weight = font
        return (
            family,
            max(1, int(round(size * self.scale))),
            weight,
        )

    # ========================================================
    # WARNING ICON
    # ========================================================

    def _prepare_warning_icon(self):
        """Create a PNG version of warning_icon.svg for Tkinter."""

        svg_path = ICON_DIR / "warning_icon.svg"

        if not WARNING_ICON_PNG.exists() and svg_path.exists():
            try:
                import cairosvg

                cairosvg.svg2png(
                    url=str(svg_path),
                    write_to=str(WARNING_ICON_PNG),
                    output_width=max(
                        1,
                        self.sx(WARNING_ICON_WIDTH),
                    ),
                    output_height=max(
                        1,
                        self.sy(WARNING_ICON_HEIGHT),
                    ),
                )
            except ImportError:
                pass

        if WARNING_ICON_PNG.exists():
            self.warning_icon = tk.PhotoImage(
                file=str(WARNING_ICON_PNG)
            )

    # ========================================================
    # INTERFACE
    # ========================================================

    def _draw_interface(self):
        self.canvas.delete("screen_content")

        width = self.sx(DESIGN_WIDTH)
        height = self.sy(DESIGN_HEIGHT)

        # ----------------------------------------------------
        # Background and window border
        # ----------------------------------------------------

        self.canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=max(
                1,
                self.sx(WINDOW_BORDER_WIDTH),
            ),
            tags=("screen_content",),
        )

        content_x = (
            DESIGN_WIDTH - CONTENT_WIDTH
        ) / 2

        content_y = (
            DESIGN_HEIGHT - CONTENT_HEIGHT
        ) / 2

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

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
            tags=("screen_content",),
        )

        # ----------------------------------------------------
        # Warning title
        # ----------------------------------------------------

        self.canvas.create_text(
            self.sx(content_x),
            self.sy(
                content_y
                + WARNING_TITLE_Y
            ),
            text="Attention: Creating an unscheduled backup",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
            tags=("screen_content",),
        )

        # ----------------------------------------------------
        # Warning icon + warning text
        # ----------------------------------------------------

        icon_x = content_x
        icon_y = (
            content_y
            + WARNING_MESSAGE_Y
            - WARNING_ICON_HEIGHT / 2
        )

        text_x = (
            icon_x
            + WARNING_ICON_WIDTH
            + WARNING_TEXT_GAP
        )

        self.canvas.create_text(
            self.sx(text_x + 16),
            self.sy(
                content_y
                + WARNING_MESSAGE_Y
                - 10
            ),
            text=(
                "Your current backup settings and "
                "schedule will not be changed."
            ),
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
            tags=("screen_content",),
        )

        self.canvas.create_text(
            self.sx(text_x + 16),
            self.sy(
                content_y
                + WARNING_MESSAGE_Y
                + 20
            ),
            text=(
                "This backup will run now in addition "
                "to your scheduled backups."
            ),
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
            tags=("screen_content",),
        )

        if self.warning_icon is not None:
            self.canvas.create_image(
                self.sx(icon_x),
                self.sy(icon_y),
                image=self.warning_icon,
                anchor="nw",
            )

        # ----------------------------------------------------
        # Exit / Back / Start
        # ----------------------------------------------------

        button_y = content_y + NAV_BUTTON_Y

        self._create_main_button(
            x=content_x,
            y=button_y,
            text="Exit",
            command=self._exit,
        )

        self._create_main_button(
            x=content_x + (CONTENT_WIDTH - NAV_BUTTON_WIDTH) / 2,
            y=button_y,
            text="Back",
            command=self._back,
        )

        self._create_main_button(
            x=content_x + CONTENT_WIDTH - NAV_BUTTON_WIDTH,
            y=button_y,
            text="Start",
            command=self._start,
        )

    # ========================================================
    # BUTTON
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

    def _exit(self):
        if self.on_exit is not None:
            self.on_exit()
        else:
            self.root.destroy()

    def _back(self):
        """Return to Window 9 without changing the saved settings."""
        if self.on_back is not None:
            self.on_back()

    def _start(self):
        if self.on_start is not None:
            self.on_start()
        else:
            print("Start backup")

    def destroy(self):
        """Remove this block's canvas items without destroying the shared Canvas."""
        if self.canvas is not None:
            self.canvas.delete("screen_content")
