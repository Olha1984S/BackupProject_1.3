"""
Backup Manager 1.2
GUI Block 3 / Select the number of copies to keep

Architecture:
    ONE Tk window
        ↓
    ONE shared Canvas
        ↓
    CopiesToKeepWindow

This block does NOT:
    - create Tk()
    - create Toplevel()
    - create its own Canvas
    - set root.geometry()
    - start mainloop()
    - destroy the main application window

The controller owns:
    - the main Tk window
    - the shared Canvas
    - application state
    - navigation between GUI blocks
"""

import tkinter as tk
from pathlib import Path

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    H2_FONT,
    H3_FONT,
    BODY_FONT,
    SMALL_FONT,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT,
    sx,
    sy,
    create_button,
    BUTTON_STATE_NORMAL,
    BUTTON_STATE_DISABLED,
)


# ============================================================
# WINDOW 3 — FIGMA GEOMETRY
# ============================================================

CONTENT_WIDTH = 800
CONTENT_HEIGHT = 640

COPIES_ENTRY_WIDTH = 80
COPIES_ENTRY_HEIGHT = 40
ENTRY_INNER_PADDING = 16

INPUT_HINT_TEXT = "* Use digital format"
INPUT_HINT_GAP = 40

WARNING_ICON_WIDTH = 40
WARNING_ICON_HEIGHT = 35
WARNING_TEXT_GAP = 14

NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60

TITLE_Y = 28
COPIES_LABEL_Y = 200
COPIES_FIELD_Y = 230
WARNING_Y = 370
NAV_BUTTON_Y = 560


# ============================================================
# WARNING ICON
# ============================================================

ICON_DIR = Path(__file__).resolve().parent / "images"
WARNING_ICON_PNG = ICON_DIR / "warning_icon.png"


class CopiesToKeepWindow:
    """
    GUI Block 3.

    Uses the shared Canvas supplied by app_controller_3.py.

    Controller state:
        state["copies_to_keep"]
    """

    def __init__(self, parent, controller, scale):
        self.parent = parent
        self.controller = controller
        self.scale = scale

        self.copies_entry = None
        self.warning_icon = None

        self.next_button_ids = None
        self.next_button_enabled = False

        # Coordinate helpers MUST exist before any drawing/font creation.
        self.sx = lambda value: sx(value, self.scale)
        self.sy = lambda value: sy(value, self.scale)

        self._prepare_warning_icon()
        self._build_screen()

        self._restore_state()
        self._update_next_button_state()

        self.copies_entry.focus_set()

    # ========================================================
    # WARNING ICON
    # ========================================================

    def _prepare_warning_icon(self):
        """Prepare the warning icon for Tkinter."""

        svg_path = ICON_DIR / "warning_icon.svg"

        if not WARNING_ICON_PNG.exists() and svg_path.exists():
            try:
                import cairosvg

                cairosvg.svg2png(
                    url=str(svg_path),
                    write_to=str(WARNING_ICON_PNG),
                    output_width=WARNING_ICON_WIDTH,
                    output_height=WARNING_ICON_HEIGHT,
                )
            except ImportError:
                pass

        if WARNING_ICON_PNG.exists():
            try:
                self.warning_icon = tk.PhotoImage(
                    file=str(WARNING_ICON_PNG)
                )
            except tk.TclError:
                self.warning_icon = None

    # ========================================================
    # SCREEN SETUP
    # ========================================================

    def _build_screen(self):
        """Create the Entry and draw the screen on the shared Canvas."""

        self.copies_entry = self._create_entry()

        self._draw_interface()

        self._place_entry(
            self.copies_entry,
            (DESIGN_WIDTH - CONTENT_WIDTH) / 2,
            (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2 + COPIES_FIELD_Y,
        )

    # ========================================================
    # ENTRY
    # ========================================================

    def _create_entry(self):
        """Create the number-of-copies Entry."""

        validate_command = self.parent.register(
            self._validate_digits
        )

        entry = tk.Entry(
            self.parent,
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=self._scaled_font(BODY_FONT),
            justify="left",
            validate="key",
            validatecommand=(validate_command, "%P"),
        )

        entry.bind(
            "<KeyRelease>",
            self._on_copies_changed,
        )

        return entry

    def _validate_digits(self, value):
        """Allow only digits while typing."""

        return value == "" or value.isdigit()

    # ========================================================
    # FONT SCALING
    # ========================================================

    def _scaled_font(self, font_spec):
        """Return a font scaled to the current GUI scale."""

        family = font_spec[0]
        size = int(font_spec[1])
        rest = tuple(font_spec[2:])

        return (
            family,
            max(1, self.sx(size)),
            *rest,
        )

    # ========================================================
    # DRAWING
    # ========================================================

    def _draw_interface(self):
        """
        Draw Window 3 content only.

        The controller owns the common background and outer frame.
        """

        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.parent.create_text(
            self.sx(content_x + CONTENT_WIDTH / 2),
            self.sy(content_y + TITLE_Y),
            text="Backup Manager",
            fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT),
            anchor="center",
            tags=("screen_content", "copies_screen"),
        )

        # ----------------------------------------------------
        # LABEL
        # ----------------------------------------------------

        self.parent.create_text(
            self.sx(content_x),
            self.sy(content_y + COPIES_LABEL_Y),
            text="Select the number of copies to keep",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
            tags=("screen_content", "copies_screen"),
        )

        # ----------------------------------------------------
        # INPUT UNDERLINE
        # ----------------------------------------------------

        line_y = self.sy(
            content_y
            + COPIES_FIELD_Y
            + COPIES_ENTRY_HEIGHT
        )

        self.parent.create_rectangle(
            self.sx(content_x),
            line_y,
            self.sx(content_x + COPIES_ENTRY_WIDTH),
            line_y + max(1, self.sx(1)),
            fill=TEXT_COLOR,
            outline="",
            tags=("screen_content", "copies_screen"),
        )

        # ----------------------------------------------------
        # INPUT HINT
        # ----------------------------------------------------

        self.parent.create_text(
            self.sx(
                content_x
                + COPIES_ENTRY_WIDTH
                + INPUT_HINT_GAP
            ),
            self.sy(
                content_y
                + COPIES_FIELD_Y
                + COPIES_ENTRY_HEIGHT / 2
                + 4
            ),
            text=INPUT_HINT_TEXT,
            fill=TEXT_COLOR,
            font=self._scaled_font(SMALL_FONT),
            anchor="w",
            tags=("screen_content", "copies_screen"),
        )

        # ----------------------------------------------------
        # WARNING
        # ----------------------------------------------------

        icon_x = content_x

        icon_y = (
            content_y
            + WARNING_Y
            - WARNING_ICON_HEIGHT / 2
        )

        text_x = (
            icon_x
            + WARNING_ICON_WIDTH
            + WARNING_TEXT_GAP
        )

        self.parent.create_text(
            self.sx(text_x + 16),
            self.sy(content_y + WARNING_Y - 10),
            text=(
                "When the maximum number of copies is reached, "
                "the oldest backup will be "
            ),
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
            tags=("screen_content", "copies_screen"),
        )

        self.parent.create_text(
            self.sx(text_x + 16),
            self.sy(content_y + WARNING_Y + 20),
            text="automatically deleted.",
            fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT),
            anchor="w",
            tags=("screen_content", "copies_screen"),
        )

        if self.warning_icon is not None:
            self.parent.create_image(
                self.sx(icon_x),
                self.sy(icon_y),
                image=self.warning_icon,
                anchor="nw",
                tags=("screen_content", "copies_screen"),
            )

        # ----------------------------------------------------
        # BACK
        # ----------------------------------------------------

        self._create_main_button(
            x=content_x,
            y=content_y + NAV_BUTTON_Y,
            text="Back",
            command=self._back,
        )

        # ----------------------------------------------------
        # NEXT
        # ----------------------------------------------------

        self._create_main_button(
            x=content_x + CONTENT_WIDTH - NAV_BUTTON_WIDTH,
            y=content_y + NAV_BUTTON_Y,
            text="Next",
            command=self._next,
        )

    # ========================================================
    # ENTRY PLACEMENT
    # ========================================================

    def _place_entry(self, entry, x, y):
        """Place the Entry over the Figma input area."""

        entry.place(
            x=self.sx(x + ENTRY_INNER_PADDING),
            y=self.sy(y + 3),
            width=self.sx(
                COPIES_ENTRY_WIDTH - 2 * ENTRY_INNER_PADDING
            ),
            height=self.sy(
                COPIES_ENTRY_HEIGHT - 6
            ),
        )

    # ========================================================
    # BUTTONS
    # ========================================================

    def _create_main_button(
        self,
        x,
        y,
        text,
        command,
    ):
        """Create a primary navigation button."""

        if text == "Back":
            state = BUTTON_STATE_NORMAL
        else:
            state = (
                BUTTON_STATE_NORMAL
                if self.next_button_enabled
                else BUTTON_STATE_DISABLED
            )

        ids = create_button(
            self.parent,
            x,
            y,
            NAV_BUTTON_WIDTH,
            NAV_BUTTON_HEIGHT,
            text,
            command,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            state=state,
            tag=f"window3_nav_{text}",
        )

        if text == "Next":
            self.next_button_ids = ids

        return ids

    # ========================================================
    # NEXT BUTTON STATE
    # ========================================================

    def _on_copies_changed(self, _event=None):
        """Update Next button when the user changes the value."""

        self._save_state()
        self._update_next_button_state()

    def _update_next_button_state(self):
        """Enable Next only for a positive integer."""

        if self.copies_entry is None:
            return

        value = self.copies_entry.get().strip()

        enabled = (
            bool(value)
            and value.isdigit()
            and int(value) > 0
        )

        if enabled == self.next_button_enabled:
            return

        if self.next_button_ids is not None:
            old_rectangle, old_text = self.next_button_ids

            self.parent.delete(old_rectangle)
            self.parent.delete(old_text)

        state = (
            BUTTON_STATE_NORMAL
            if enabled
            else BUTTON_STATE_DISABLED
        )

        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        self.next_button_ids = create_button(
            self.parent,
            content_x + CONTENT_WIDTH - NAV_BUTTON_WIDTH,
            content_y + NAV_BUTTON_Y,
            NAV_BUTTON_WIDTH,
            NAV_BUTTON_HEIGHT,
            "Next",
            self._next,
            style=BUTTON_PRIMARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            state=state,
            tag="window3_nav_Next",
        )

        self.next_button_enabled = enabled

    # ========================================================
    # STATE
    # ========================================================

    def _restore_state(self):
        """Restore the previously entered number of copies."""

        state = getattr(self.controller, "state", {})

        copies = state.get("copies_to_keep")

        if copies not in (None, ""):
            self.copies_entry.insert(0, str(copies))

    def _save_state(self):
        """Save the current value to the controller."""

        if not hasattr(self.controller, "state"):
            return

        self.controller.state["copies_to_keep"] = (
            self.copies_entry.get().strip()
        )

    # ========================================================
    # NAVIGATION
    # ========================================================

    def _back(self):
        """Return to Window 2 through the controller."""

        self._save_state()

        if hasattr(self.controller, "show_screen"):
            self.controller.show_screen("paths")

    def _next(self):
        """Validate and pass the selected number to the controller."""

        if not self.next_button_enabled:
            return

        copies = self.copies_entry.get().strip()

        if not copies.isdigit() or int(copies) <= 0:
            self.copies_entry.focus_set()
            return

        copies = int(copies)

        self.controller.state["copies_to_keep"] = copies

        if hasattr(self.controller, "_next_from_window_3"):
            self.controller._next_from_window_3(copies)

    # ========================================================
    # DESTROY
    # ========================================================

    def destroy(self):
        """
        Destroy only widgets belonging to this block.

        The shared Canvas itself belongs to the controller and
        MUST NOT be destroyed here.
        """

        if self.copies_entry is not None:
            try:
                self.copies_entry.destroy()
            except tk.TclError:
                pass

        self.copies_entry = None
        self.warning_icon = None
        self.next_button_ids = None


# This file is intended to be loaded by app_controller_3.py.
# It intentionally has no standalone mainloop.
