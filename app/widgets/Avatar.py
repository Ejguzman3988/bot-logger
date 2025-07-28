from textual.reactive import reactive
from textual.widgets import Static

from app.utils.frame_loader import load_frames


class Avatar(Static):
    AVATAR_NAME = "robo"
    IDLE_PATH = f"images/{AVATAR_NAME}/idle"

    frames = {
        "loading": ["|", "/", "-", "\\"],
        "idle": {
            "frames": [],
            "path": IDLE_PATH,
        },
    }
    animation_name = reactive("loading")
    current_frame_step = reactive(0)

    def on_mount(self):
        self.timer = self.set_timer(4, lambda: self.set_animation_name("idle"))
        self.interval = self.set_interval(2 / 12, self.advance_frame)

    def on_resize(self) -> None:
        """Called when the widget is resized. Load frames here."""
        # Get the available space in characters.
        width = self.size.width // 2
        height = self.size.height

        # Stop if the widget is too small to draw anything.

        # Correct for terminal aspect ratio (characters are ~2x tall).
        self.idle_frames = load_frames(self.IDLE_PATH, (width, height))

    def on_unmount(self):
        self.interval.stop()
        self.timer.stop()

    def watch_animation_name(self):
        self.interval.pause()
        self.current_frame_step = 0
        if len(self.get_current_animation_frames()) == 0:
            width = self.size.width // 2
            height = self.size.height
            path = self.frames[self.animation_name]["path"]
            self.frames[self.animation_name]["frames"] = load_frames(
                path, (width, height)
            )

        self.interval.resume()

    def get_current_animation_frames(self):
        if self.animation_name == "loading":
            return self.frames[self.animation_name]
        return self.frames[self.animation_name]["frames"]

    def get_current_frame(self):
        return self.get_current_animation_frames()[self.current_frame_step]

    def set_animation_name(self, animation_name):
        if animation_name not in self.frames:
            self.animation_name = "loading"
            return

        self.animation_name = animation_name

    def advance_frame(self):
        if len(self.idle_frames) == 0:
            raise Exception("No frames loaded. Check file path")
        self.current_frame_step = (self.current_frame_step + 1) % len(
            self.get_current_animation_frames()
        )

    def render(self):
        """Render the current frame of the animation."""
        return self.get_current_frame() or ""
