"""
Backup Manager 1.2
GUI Block 2 / Choice of Paths

New architecture:

    ONE Tk window
        ↓
    ONE main Canvas
        ↓
    ChoiceOfPathsScreen

This screen does NOT:
    - create Tk()
    - create Toplevel()
    - set root.geometry()
    - start mainloop()
    - destroy the main window

The controller owns application state and navigation.
"""

import tkinter as tk
from tkinter import filedialog
from pathlib import Path

from gui.gui_style import (
    BACKGROUND_COLOR,
    TEXT_COLOR,
    H2_FONT,
    H3_FONT,
    BODY_FONT,
    DESIGN_WIDTH,
    DESIGN_HEIGHT,
    BUTTON_PRIMARY,
    BUTTON_SECONDARY,
    BUTTON_ANCHOR_LEFT,
    scale_value,
    sx,
    sy,
    create_button,
)


# ============================================================================
# WINDOW 2 — FIGMA GEOMETRY
# ============================================================================

CONTENT_WIDTH = 800
CONTENT_HEIGHT = 640

ENTRY_WIDTH = 600
ENTRY_HEIGHT = 60
ENTRY_INNER_PADDING = 16

PATH_BUTTON_GAP = 40

BROWSE_WIDTH = 160
BROWSE_HEIGHT = 60

NAV_BUTTON_WIDTH = 160
NAV_BUTTON_HEIGHT = 60

TITLE_Y = 28

SOURCE_LABEL_Y = 180
SOURCE_FIELD_Y = 210

BACKUP_LABEL_Y = 330
BACKUP_FIELD_Y = 360

NAV_BUTTON_Y = 560


class ChoiceOfPathsScreen:
    """
    GUI Block 2.

    The screen uses the shared Canvas supplied by the controller.

    Application state is stored in the controller:
        state["source_path"]
        state["backup_path"]
    """

    def __init__(
        self,
        parent,
        controller,
        scale: float,
    ):
        self.parent = parent
        self.controller = controller
        self.scale = scale

        self.source_entry = None
        self.backup_entry = None

        self.next_button = None

        self._build_screen()

        # Restore values previously stored by the controller.
        self._restore_state()

        # Next must initially be disabled unless both fields contain values.
        self._update_next_state()

        self.source_entry.focus_set()

    # =========================================================================
    # SCREEN SETUP
    # =========================================================================

    def _build_screen(self):
        """Create the Entry widgets and draw the Canvas interface."""

        self.source_entry = self._create_entry()
        self.backup_entry = self._create_entry()

        self._draw_interface()

    # =========================================================================
    # ENTRIES
    # =========================================================================

    def _create_entry(self):
        """
        Create a transparent-style Entry.

        The Entry itself is placed over the white Figma field area.
        """

        entry = tk.Entry(
            self.parent,
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=self._scaled_font(BODY_FONT),
        )

        entry.bind(
            "<KeyRelease>",
            self._on_entry_changed,
        )

        return entry

    def _scaled_font(self, font_spec):
        """Return a font scaled according to the current screen scale."""

        family = font_spec[0]
        size = int(font_spec[1])
        rest = tuple(font_spec[2:])

        return (
            family,
            max(1, self.sx(size)),
            *rest,
        )

    # =========================================================================
    # DRAWING
    # =========================================================================

    def _draw_interface(self):
        """
        Draw only Window 2 content.

        The common application background and outer border belong to the
        controller and are deliberately not drawn here.
        """

        # Content area is centered in the shared 1400 × 804 design space.
        content_x = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        content_y = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2

        # ---------------------------------------------------------------------
        # TITLE
        # ---------------------------------------------------------------------

        self.parent.create_text(
            self.sx(content_x + CONTENT_WIDTH / 2),
            self.sy(content_y + TITLE_Y),
            text="Backup Manager",
            fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT),
            anchor="center",
            tags=("screen_content", "paths_screen"),
        )

        # ---------------------------------------------------------------------
        # SOURCE FOLDER
        # ---------------------------------------------------------------------

        self.parent.create_text(
            self.sx(content_x),
            self.sy(content_y + SOURCE_LABEL_Y),
            text="Select source folder:",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
            tags=("screen_content", "paths_screen"),
        )

        self._draw_entry_field(
            content_x,
            content_y + SOURCE_FIELD_Y,
        )

        self._place_entry(
            self.source_entry,
            content_x,
            content_y + SOURCE_FIELD_Y,
        )

        self._create_figma_button(
            x=content_x + ENTRY_WIDTH + PATH_BUTTON_GAP,
            y=content_y + SOURCE_FIELD_Y,
            width=BROWSE_WIDTH,
            height=BROWSE_HEIGHT,
            text="Browse",
            command=self._browse_source,
            tag="paths_screen_browse_source",
        )

        # ---------------------------------------------------------------------
        # BACKUP LOCATION
        # ---------------------------------------------------------------------

        self.parent.create_text(
            self.sx(content_x),
            self.sy(content_y + BACKUP_LABEL_Y),
            text="Select backup location:",
            fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT),
            anchor="w",
            tags=("screen_content", "paths_screen"),
        )

        self._draw_entry_field(
            content_x,
            content_y + BACKUP_FIELD_Y,
        )

        self._place_entry(
            self.backup_entry,
            content_x,
            content_y + BACKUP_FIELD_Y,
        )

        self._create_figma_button(
            x=content_x + ENTRY_WIDTH + PATH_BUTTON_GAP,
            y=content_y + BACKUP_FIELD_Y,
            width=BROWSE_WIDTH,
            height=BROWSE_HEIGHT,
            text="Browse",
            command=self._browse_backup,
            tag="paths_screen_browse_backup",
        )

        # ---------------------------------------------------------------------
        # BACK
        # ---------------------------------------------------------------------

        self._create_main_button(
            x=content_x,
            y=content_y + NAV_BUTTON_Y,
            text="Back",
            command=self._back,
            tag="paths_screen_back",
        )

        # ---------------------------------------------------------------------
        # NEXT
        # ---------------------------------------------------------------------

        self.next_button = self._create_main_button(
            x=content_x + CONTENT_WIDTH - NAV_BUTTON_WIDTH,
            y=content_y + NAV_BUTTON_Y,
            text="Next",
            command=self._next,
            tag="paths_screen_next",
        )

    def _draw_entry_field(self, x, y):
        """
        Draw the white field area behind an Entry.

        The rectangle belongs to the screen, while the main window
        background remains owned by the controller.
        """

        self.parent.create_rectangle(
            self.sx(x),
            self.sy(y),
            self.sx(x + ENTRY_WIDTH),
            self.sy(y + ENTRY_HEIGHT),
            fill=BACKGROUND_COLOR,
            outline="",
            tags=("screen_content", "paths_screen"),
        )

        # Figma-style bottom line of the input field.
        self.parent.create_line(
            self.sx(x),
            self.sy(y + ENTRY_HEIGHT),
            self.sx(x + ENTRY_WIDTH),
            self.sy(y + ENTRY_HEIGHT),
            fill=TEXT_COLOR,
            width=max(1, self.sx(1)),
            tags=("screen_content", "paths_screen"),
        )

    # =========================================================================
    # ENTRY PLACEMENT
    # =========================================================================

    def _place_entry(self, entry, x, y):
        """Place a Tk Entry over its corresponding Figma field."""

        entry.place(
            x=self.sx(x + ENTRY_INNER_PADDING),
            y=self.sy(y + 20),
            width=self.sx(
                ENTRY_WIDTH - 2 * ENTRY_INNER_PADDING
            ),
            height=self.sy(
                ENTRY_HEIGHT - 20
            ),
        )

    # =========================================================================
    # BUTTONS
    # =========================================================================

    def _create_figma_button(
        self,
        x,
        y,
        width,
        height,
        text,
        command,
        tag,
    ):
        """Create a Browse-style secondary button."""

        return create_button(
            self.parent,
            x,
            y,
            width,
            height,
            text,
            command,
            style=BUTTON_SECONDARY,
            scale=self.scale,
            anchor=BUTTON_ANCHOR_LEFT,
            tag=tag,
        )

    def _create_main_button(
        self,
        x,
        y,
        text,
        command,
        tag,
    ):
        """Create a primary navigation button."""

        return create_button(
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
            tag=tag,
            state="normal",
        )

    # =========================================================================
    # STATE
    # =========================================================================

    def _restore_state(self):
        """Restore previously entered paths from the controller state."""

        state = getattr(self.controller, "state", {})

        source_path = state.get("source_path") or ""
        backup_path = state.get("backup_path") or ""

        if source_path:
            self.source_entry.insert(0, source_path)

        if backup_path:
            self.backup_entry.insert(0, backup_path)

    def _save_state(self):
        """Save the current field values to the controller state."""

        if not hasattr(self.controller, "state"):
            return

        self.controller.state["source_path"] = (
            self.source_entry.get().strip()
        )

        self.controller.state["backup_path"] = (
            self.backup_entry.get().strip()
        )

    # =========================================================================
    # NEXT BUTTON STATE
    # =========================================================================

    def _on_entry_changed(self, _event=None):
        """React to typing in either path field."""

        self._save_state()
        self._update_next_state()

    def _update_next_state(self):
        """
        Enable Next only when both fields contain text.

        Path existence is checked only after Next is pressed.
        """

        source_filled = bool(
            self.source_entry.get().strip()
        )

        backup_filled = bool(
            self.backup_entry.get().strip()
        )

        enabled = source_filled and backup_filled

        # The current gui_style Canvas button implementation does not yet
        # expose a direct disabled-button object API. Therefore the button
        # state is represented by its visual state here; command validation
        # remains protected in _next().
        if self.next_button is None:
            return

        rectangle_id, text_id = self.next_button

        from gui.gui_style import set_button_state

        set_button_state(
            self.parent,
            rectangle_id,
            text_id,
            BUTTON_PRIMARY,
            "normal" if enabled else "disabled",
            self.scale,
        )

        # Store the logical state on the screen.
        self._next_enabled = enabled

    # =========================================================================
    # BROWSE
    # =========================================================================

    def _browse_source(self):
        """Open the source-folder selection dialog."""

        path = filedialog.askdirectory(
            title="Select source folder"
        )

        if path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, path)
            self._save_state()
            self._update_next_state()

    def _browse_backup(self):
        """Open the backup-location selection dialog."""

        path = filedialog.askdirectory(
            title="Select backup location"
        )

        if path:
            self.backup_entry.delete(0, tk.END)
            self.backup_entry.insert(0, path)
            self._save_state()
            self._update_next_state()

    # =========================================================================
    # NAVIGATION
    # =========================================================================

    def _back(self):
        """Return to Block 1 through the controller."""

        self._save_state()

        if hasattr(self.controller, "show_screen"):
            self.controller.show_screen("start")

    def _next(self):
        """
        Validate that both fields are filled and ask the controller
        to validate the actual paths.

        Actual filesystem validation belongs to the application/controller
        layer and will be connected with the existing backend.
        """

        self._save_state()

        if not getattr(self, "_next_enabled", False):
            return

        source = self.source_entry.get().strip()
        backup = self.backup_entry.get().strip()

        source_valid = Path(source).is_dir()
        backup_valid = Path(backup).is_dir()

        if not source_valid or not backup_valid:
            invalid_fields = []

            if not source_valid:
                invalid_fields.append("source")

            if not backup_valid:
                invalid_fields.append("backup")

            self._show_path_error(invalid_fields)
            return

        # Block 3 will be connected later.
        if hasattr(self.controller, "show_screen"):
            self.controller.show_screen("copies")

    def _show_path_error(self, invalid_fields):
        """Show Window 2.1 and clear/focus the invalid path fields after OK."""
        from importlib import import_module

        ErrorPathWindow = import_module("2_1_backup_manager_error_path").ErrorPathWindow

        if invalid_fields == ["source"]:
            title = "Invalid source folder"
            message = "The selected source folder does not exist."
        elif invalid_fields == ["backup"]:
            title = "Invalid backup location"
            message = "The selected backup location does not exist."
        else:
            title = "Invalid paths"
            message = "The selected source folder and backup location do not exist."

        ErrorPathWindow(
            self.parent.winfo_toplevel(),
            title=title,
            message=message,
            on_ok=lambda: self._handle_path_error_closed(invalid_fields),
        )

    def _handle_path_error_closed(self, invalid_fields):
        """Clear invalid fields and place the cursor according to the rules."""
        if "source" in invalid_fields:
            self.source_entry.delete(0, tk.END)

        if "backup" in invalid_fields:
            self.backup_entry.delete(0, tk.END)

        self._save_state()
        self._update_next_state()

        if "source" in invalid_fields:
            self.source_entry.focus_set()
            self.source_entry.icursor(tk.END)
        elif "backup" in invalid_fields:
            self.backup_entry.focus_set()
            self.backup_entry.icursor(tk.END)

    # =========================================================================
    # DESTROY
    # =========================================================================

    def destroy(self):
        """
        Remove Window 2 widgets and Canvas content.

        The controller owns the main Tk window and Canvas.
        This block only removes the widgets and drawings it created.
        """

        for entry in (self.source_entry, self.backup_entry):
            if entry is not None:
                try:
                    entry.destroy()
                except tk.TclError:
                    pass

        self.source_entry = None
        self.backup_entry = None
        self.next_button = None

        self.parent.delete("screen_content")
        self.parent.delete("paths_screen")
        self.parent.delete("paths_screen_back")
        self.parent.delete("paths_screen_next")
        self.parent.delete("paths_screen_browse_source")
        self.parent.delete("paths_screen_browse_backup")


    # =========================================================================
    # SCALE HELPERS
    # =========================================================================

    def sx(self, value):
        return sx(value, self.scale)

    def sy(self, value):
        return sy(value, self.scale)
