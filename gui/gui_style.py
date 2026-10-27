"""
Shared visual style and rendering helpers for BackupProject_1.2 GUI.

This module contains only shared design-system values and helpers.
Window-specific content, coordinates, dimensions, and application logic
remain in the individual GUI block modules.
"""

from __future__ import annotations

import tkinter as tk
from typing import Callable, Mapping, Optional


# ---------------------------------------------------------------------------
# COLORS
# ---------------------------------------------------------------------------

BACKGROUND_COLOR = "#F0F0F0"
TEXT_COLOR = "#302D4B"
DISABLED_COLOR = "#CECECE"

WINDOW_BORDER_COLOR = "#CECECE"
BUTTON_BORDER_COLOR = "#302D4B"
BUTTON_DISABLED_BORDER_COLOR = "#CECECE"


# ---------------------------------------------------------------------------
# TYPOGRAPHY
# ---------------------------------------------------------------------------

H1_FONT = ("Zen Dots", 34)
H2_FONT = ("Zen Dots", 24)
H3_FONT = ("Zen Kaku Gothic Antique", 16, "bold")
BODY_FONT = ("Zen Kaku Gothic Antique", 14)
SMALL_FONT = ("Zen Kaku Gothic Antique", 10)
BUTTON_FONT = ("Zen Dots", 18)

SECONDARY_BUTTON_FONT = ("Zen Kaku Gothic Antique", 16)


# ---------------------------------------------------------------------------
# WINDOW LAYOUT
# ---------------------------------------------------------------------------

DESIGN_WIDTH = 1200
DESIGN_HEIGHT = 800

CONTENT_WIDTH = 800
CONTENT_HEIGHT = 640

WINDOW_BORDER_WIDTH = 2

MAX_SCALE = 0.75


# ---------------------------------------------------------------------------
# MAIN WINDOW SHADOW
# ---------------------------------------------------------------------------

EFFECT_WINDOW_SHADOW = {
    "type": "drop_shadow",
    "x": 0,
    "y": 0,
    "blur": 30,
    "spread": 0,
    "color": "#000000",
    "opacity": 50,
}


# ---------------------------------------------------------------------------
# BUTTON EFFECTS
# ---------------------------------------------------------------------------

EFFECT_BUTTON_HOVER = {
    "type": "drop_shadow",
    "x": 0,
    "y": 0,
    "blur": 15,
    "spread": 0,
    "color": "#000000",
    "opacity": 30,
}

EFFECT_BUTTON_PRESSED = {
    "type": "drop_shadow",
    "x": 0,
    "y": 3,
    "blur": 15,
    "spread": 0,
    "color": "#000000",
    "opacity": 50,
}


# ---------------------------------------------------------------------------
# BUTTON STYLES
# ---------------------------------------------------------------------------

BUTTON_PRIMARY = {
    "normal": {
        "background": "#F0F0F0",
        "text": "#302D4B",
        "border": "#302D4B",
        "border_width": 2,
        "font": BUTTON_FONT,
        "effect": None,
    },
    "hover": {
        "background": "#F0F0F0",
        "text": "#302D4B",
        "border": "#302D4B",
        "border_width": 2,
        "font": BUTTON_FONT,
        "effect": EFFECT_BUTTON_HOVER,
    },
    "pressed": {
        "background": "#F0F0F0",
        "text": "#302D4B",
        "border": "#302D4B",
        "border_width": 2,
        "font": BUTTON_FONT,
        "effect": EFFECT_BUTTON_PRESSED,
    },
    "disabled": {
        "background": "#F0F0F0",
        "text": "#CECECE",
        "border": "#CECECE",
        "border_width": 2,
        "font": BUTTON_FONT,
        "effect": None,
    },
}


BUTTON_SECONDARY = {
    "normal": {
        "background": "#F0F0F0",
        "text": "#302D4B",
        "border": "#302D4B",
        "border_width": 1,
        "font": SECONDARY_BUTTON_FONT,
        "effect": None,
    },
    "hover": {
        "background": "#F0F0F0",
        "text": "#302D4B",
        "border": "#302D4B",
        "border_width": 1,
        "font": SECONDARY_BUTTON_FONT,
        "effect": EFFECT_BUTTON_HOVER,
    },
    "pressed": {
        "background": "#F0F0F0",
        "text": "#302D4B",
        "border": "#302D4B",
        "border_width": 1,
        "font": SECONDARY_BUTTON_FONT,
        "effect": EFFECT_BUTTON_PRESSED,
    },
    "disabled": {
        "background": "#F0F0F0",
        "text": "#CECECE",
        "border": "#CECECE",
        "border_width": 1,
        "font": SECONDARY_BUTTON_FONT,
        "effect": None,
    },
}


# ---------------------------------------------------------------------------
# SCALING
# ---------------------------------------------------------------------------

def center_window(window, width, height):
    """Center a Tkinter window on the current screen."""
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def calculate_scale(
    window_width: int,
    window_height: int,
    *,
    max_scale: float = MAX_SCALE,
) -> float:
    """Return the design-to-window scale used by the GUI."""
    if window_width <= 0 or window_height <= 0:
        return 1.0

    scale = min(
        window_width / DESIGN_WIDTH,
        window_height / DESIGN_HEIGHT,
    )

    return min(scale, max_scale)


def scale_value(value: float, scale: float) -> int:
    """Scale a design-space value and return a Tkinter-friendly integer."""
    return int(round(value * scale))


def sx(value: float, scale: float) -> int:
    """Scale an X coordinate or width."""
    return scale_value(value, scale)


def sy(value: float, scale: float) -> int:
    """Scale a Y coordinate or height."""
    return scale_value(value, scale)


# ---------------------------------------------------------------------------
# BUTTON RENDERING
# ---------------------------------------------------------------------------

BUTTON_STATE_NORMAL = "normal"
BUTTON_STATE_HOVER = "hover"
BUTTON_STATE_PRESSED = "pressed"
BUTTON_STATE_DISABLED = "disabled"

BUTTON_ANCHOR_LEFT = "left"
BUTTON_ANCHOR_RIGHT = "right"
BUTTON_ANCHOR_CENTER = "center"


def _button_left_x(
    x: float,
    width: float,
    *,
    anchor: str,
) -> float:
    if anchor == BUTTON_ANCHOR_LEFT:
        return x
    if anchor == BUTTON_ANCHOR_RIGHT:
        return x - width
    if anchor == BUTTON_ANCHOR_CENTER:
        return x - width / 2
    raise ValueError(f"Unsupported button anchor: {anchor!r}")


def create_button(
    canvas: tk.Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
    command: Optional[Callable[[], None]],
    *,
    style: Mapping[str, Mapping[str, object]] = BUTTON_PRIMARY,
    scale: float = 1.0,
    anchor: str = BUTTON_ANCHOR_LEFT,
    state: str = BUTTON_STATE_NORMAL,
    tag: Optional[str] = None,
):
    """
    Create a Canvas-based button using a shared button style.

    Returns:
        (rectangle_id, text_id)
    """
    if state not in style:
        raise ValueError(f"Unsupported initial button state: {state!r}")

    item_tag = tag or f"button_{id(canvas)}_{text}_{x}_{y}"

    left = _button_left_x(x, width, anchor=anchor)
    top = y
    right = left + width
    bottom = top + height

    visual = style[state]

    rectangle_id = canvas.create_rectangle(
        sx(left, scale),
        sy(top, scale),
        sx(right, scale),
        sy(bottom, scale),
        fill=str(visual["background"]),
        outline=str(visual["border"]),
        width=max(1, sx(float(visual["border_width"]), scale)),
        tags=(item_tag,),
    )

    text_id = canvas.create_text(
        sx((left + right) / 2, scale),
        sy((top + bottom) / 2, scale),
        text=text,
        fill=str(visual["text"]),
        font=_scaled_font(visual["font"], scale),
        tags=(item_tag,),
    )

    if state != BUTTON_STATE_DISABLED:
        canvas.tag_bind(
            item_tag,
            "<Enter>",
            lambda _event: set_button_state(
                canvas, rectangle_id, text_id, style,
                BUTTON_STATE_HOVER, scale
            ),
        )

        canvas.tag_bind(
            item_tag,
            "<Leave>",
            lambda _event: set_button_state(
                canvas, rectangle_id, text_id, style,
                BUTTON_STATE_NORMAL, scale
            ),
        )

        canvas.tag_bind(
            item_tag,
            "<ButtonPress-1>",
            lambda _event: set_button_state(
                canvas, rectangle_id, text_id, style,
                BUTTON_STATE_PRESSED, scale
            ),
        )

        canvas.tag_bind(
            item_tag,
            "<ButtonRelease-1>",
            lambda _event: _release_button(
                canvas, rectangle_id, text_id, style, scale, command
            ),
        )

    return rectangle_id, text_id


def _release_button(
    canvas: tk.Canvas,
    rectangle_id: int,
    text_id: int,
    style: Mapping[str, Mapping[str, object]],
    scale: float,
    command: Optional[Callable[[], None]],
) -> None:
    set_button_state(
        canvas,
        rectangle_id,
        text_id,
        style,
        BUTTON_STATE_HOVER,
        scale,
    )

    if command is not None:
        canvas.after_idle(command)


def set_button_state(
    canvas: tk.Canvas,
    rectangle_id: int,
    text_id: int,
    style: Mapping[str, Mapping[str, object]],
    state: str,
    scale: float = 1.0,
) -> None:
    """Apply one visual state to an existing Canvas button."""
    if state not in style:
        raise ValueError(f"Unsupported button state: {state!r}")

    visual = style[state]

    canvas.itemconfigure(
        rectangle_id,
        fill=str(visual["background"]),
        outline=str(visual["border"]),
        width=max(1, sx(float(visual["border_width"]), scale)),
    )

    canvas.itemconfigure(
        text_id,
        fill=str(visual["text"]),
        font=_scaled_font(visual["font"], scale),
    )


def _scaled_font(font_spec, scale: float):
    """Scale a Tkinter font tuple while preserving family/style attributes."""
    family = font_spec[0]
    size = int(font_spec[1])
    rest = tuple(font_spec[2:])

    scaled_size = max(1, int(round(size * scale)))
    return (family, scaled_size, *rest)
