import tkinter as tk
from pathlib import Path
from gui_style import (BACKGROUND_COLOR, TEXT_COLOR, DESIGN_WIDTH, DESIGN_HEIGHT,
    CONTENT_WIDTH, CONTENT_HEIGHT, H2_FONT, H3_FONT, BODY_FONT, BUTTON_PRIMARY,
    BUTTON_ANCHOR_LEFT, create_button, sx, sy)

PROGRESS_BAR_WIDTH = 800
PROGRESS_BAR_HEIGHT = 30
PROGRESS_BAR_BORDER_WIDTH = 2
STOP_BUTTON_WIDTH = 240
STOP_BUTTON_HEIGHT = 60
TITLE_Y = 28
PROGRESS_TITLE_Y = 190
STATUS_Y = 240
PROGRESS_BAR_Y = 282
FILES_COUNT_Y = 350
STOP_BUTTON_Y = 500

# Reuse the same ten-point animation assets as the other setup screens.
POINT_COUNT = 5
ANIMATION_INTERVAL_MS = 180
POINT_GAP = 3
POINT_SIZE = 10


class BackupInProgressWindow:
    """Backup progress screen integrated into the shared Canvas."""

    def __init__(self, root, parent, scale, files_copied=0, total_files=0,
                 status="Preparing", on_stop=None):
        self.root, self.canvas, self.scale = root, parent, scale
        self.files_copied = max(0, int(files_copied))
        self.total_files = max(0, int(total_files))
        self.status, self.on_stop = status, on_stop
        self._animation_after_id = None
        self._active_point = 0
        self._point_images = []
        self._load_point_images()
        self._draw_interface()
        self._sync_verifying_animation()

    def sx(self, value):
        return sx(value, self.scale)

    def sy(self, value):
        return sy(value, self.scale)

    def _scaled_font(self, font):
        family, size, *weight = font
        return (family, max(1, int(round(size * self.scale))), *weight)

    def _load_point_images(self):
        """Load existing active/passive point icons from gui/images."""
        image_dir = Path(__file__).resolve().parent / "images"
        active_path = image_dir / "active_point.png"
        passive_path = image_dir / "passive_point.png"
        try:
            self._active_point_image = tk.PhotoImage(file=str(active_path))
            self._passive_point_image = tk.PhotoImage(file=str(passive_path))
            self._point_images = [self._active_point_image, self._passive_point_image]
        except (tk.TclError, OSError):
            # Keep the screen usable if the image assets are not present.
            self._active_point_image = None
            self._passive_point_image = None

    def update_progress(self, files_copied=None, total_files=None, status=None):
        if files_copied is not None:
            self.files_copied = max(0, int(files_copied))
        if total_files is not None:
            self.total_files = max(0, int(total_files))
        if status is not None:
            self.status = str(status)
        self._draw_interface()
        self._sync_verifying_animation()

    def _is_animated_status(self):
        status = str(self.status).casefold()
        return (
            "verif" in status
            or "checking free space" in status
            or "checking_space" in status
            or "preparing" in status
        )

    def _sync_verifying_animation(self):
        if self._is_animated_status():
            if self._animation_after_id is None:
                self._animate_verifying()
        else:
            self._stop_verifying_animation()

    def _stop_verifying_animation(self):
        if self._animation_after_id is not None:
            try:
                self.root.after_cancel(self._animation_after_id)
            except tk.TclError:
                pass
            self._animation_after_id = None

    def _animate_verifying(self):
        self._animation_after_id = None
        if not self._is_animated_status():
            return
        self._active_point = (self._active_point + 1) % POINT_COUNT
        self._draw_status_line()
        self._animation_after_id = self.root.after(
            ANIMATION_INTERVAL_MS, self._animate_verifying
        )

    def _draw_status_line(self):
        self.canvas.delete("status_line")
        x0 = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        status_x = x0 + 100
        y = self.sy(((DESIGN_HEIGHT - CONTENT_HEIGHT) / 2) + STATUS_Y)
        self.canvas.create_text(
            self.sx(x0), y, text="Status:", fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT), anchor="w",
            tags=("screen_content", "status_line")
        )
        status_text = str(self.status).strip()
        self.canvas.create_text(
            self.sx(status_x), y, text=status_text, fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT), anchor="w",
            tags=("screen_content", "status_line")
        )
        if self._is_animated_status():
            # Place ten active/inactive point icons on the same line as the current status.
            font_family, font_size, *_ = self._scaled_font(BODY_FONT)
            estimated_text_width = len(status_text) * font_size * 0.62
            points_x = self.sx(status_x) + estimated_text_width + self.sx(10)
            # Slight downward optical correction after reducing the PNG icons.
            points_y = y + self.sy(4)
            point_size = max(1, self.sx(POINT_SIZE))
            gap = max(1, self.sx(POINT_GAP))
            if self._active_point_image and self._passive_point_image:
                for index in range(POINT_COUNT):
                    image = (self._active_point_image if index == self._active_point
                             else self._passive_point_image)
                    self.canvas.create_image(
                        points_x + index * (point_size + gap), points_y,
                        image=image, anchor="w",
                        tags=("screen_content", "status_line")
                    )
            else:
                # Fallback if the image files cannot be loaded.
                dots = " ".join("●" if i == self._active_point else "○"
                                for i in range(POINT_COUNT))
                self.canvas.create_text(
                    points_x, y, text=dots, fill=TEXT_COLOR,
                    font=self._scaled_font(BODY_FONT), anchor="w",
                    tags=("screen_content", "status_line")
                )

    def _draw_interface(self):
        self.canvas.delete("screen_content")
        x0 = (DESIGN_WIDTH - CONTENT_WIDTH) / 2
        y0 = (DESIGN_HEIGHT - CONTENT_HEIGHT) / 2
        tag = ("screen_content",)
        self.canvas.create_text(
            self.sx(x0 + CONTENT_WIDTH / 2), self.sy(y0 + TITLE_Y),
            text="Backup Manager", fill=TEXT_COLOR,
            font=self._scaled_font(H2_FONT), anchor="center", tags=tag
        )
        self.canvas.create_text(
            self.sx(x0), self.sy(y0 + PROGRESS_TITLE_Y),
            text="Backup in progress", fill=TEXT_COLOR,
            font=self._scaled_font(H3_FONT), anchor="w", tags=tag
        )
        self._draw_status_line()

        status_key = str(self.status).casefold()
        is_space_check = "checking free space" in status_key or "checking_space" in status_key
        # Keep the bar at 0% until the destination free-space check succeeds.
        ratio = (0.0 if is_space_check else
                 min(self.files_copied / self.total_files, 1.0) if self.total_files else 0.0)
        left, top = self.sx(x0), self.sy(y0 + PROGRESS_BAR_Y)
        right = self.sx(x0 + PROGRESS_BAR_WIDTH)
        bottom = self.sy(y0 + PROGRESS_BAR_Y + PROGRESS_BAR_HEIGHT)
        self.canvas.create_rectangle(
            left, top, right, bottom, fill=BACKGROUND_COLOR,
            outline=TEXT_COLOR,
            width=max(1, self.sx(PROGRESS_BAR_BORDER_WIDTH)), tags=tag
        )
        if ratio > 0:
            self.canvas.create_rectangle(
                left, top, left + (right - left) * ratio, bottom,
                fill=TEXT_COLOR, outline="", tags=tag
            )
        self.canvas.create_text(
            right + self.sx(14), (top + bottom) / 2,
            text=f"{round(ratio * 100)}%", fill=TEXT_COLOR,
            font=self._scaled_font(BODY_FONT), anchor="w", tags=tag
        )
        self.canvas.create_text(
            self.sx(x0), self.sy(y0 + FILES_COUNT_Y),
            text=f"{self.files_copied} / {self.total_files} files",
            fill=TEXT_COLOR, font=self._scaled_font(BODY_FONT),
            anchor="w", tags=tag
        )
        create_button(
            self.canvas, x=x0 + CONTENT_WIDTH - STOP_BUTTON_WIDTH,
            y=y0 + STOP_BUTTON_Y, width=STOP_BUTTON_WIDTH,
            height=STOP_BUTTON_HEIGHT, text="Stop backup",
            command=self._stop, style=BUTTON_PRIMARY,
            scale=self.scale, anchor=BUTTON_ANCHOR_LEFT
        )

    def _stop(self):
        self._stop_verifying_animation()
        if self.on_stop:
            self.on_stop()

    def destroy(self):
        self._stop_verifying_animation()
        if self.canvas is not None:
            self.canvas.delete("screen_content")


if __name__ == "__main__":
    root = tk.Tk()
    from gui_style import MAX_SCALE
    canvas = tk.Canvas(
        root, width=int(DESIGN_WIDTH * MAX_SCALE),
        height=int(DESIGN_HEIGHT * MAX_SCALE),
        bg=BACKGROUND_COLOR, highlightthickness=0, bd=0
    )
    canvas.pack()
    BackupInProgressWindow(root, canvas, MAX_SCALE, status="Checking free space")
    root.mainloop()
