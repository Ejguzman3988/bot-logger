import json
import asyncio
from pathlib import Path

from watchfiles import awatch
from textual.reactive import reactive
from textual.widgets import Static

from app.utils.frame_loader import load_avatar


class Avatar(Static):
    STATE_FILE = Path("state.json")
    AVATAR_NAME = "robo"

    frames = {}
    animation_name = reactive("idle")
    direction = reactive("down")
    current_frame_step = reactive(0)

    def on_mount(self):
        self.timer = self.set_timer(4, lambda: self.set_animation_name("idle"))
        self.interval = self.set_interval(0.15, self.advance_frame)
        self.frames = load_avatar("robo", (16, 16))

        self._watcher_task = asyncio.create_task(self._watch_state_file())

    async def _watch_state_file(self):
        """Run in the background, fire on every change to STATE_FILE"""
        async for changes in awatch(self.STATE_FILE):
            try:
                data = json.loads(self.STATE_FILE.read_text())
            except Exception:
                continue
            if (ani := data.get("ani")) and ani != self.animation_name:
                self.animation_name = ani
            if (dr := data.get("dir")) and dr != self.direction:
                self.direction = dr

    # def on_resize(self) -> None:
    #     """Called when the widget is resized. Load frames here."""
    #     # Get the available space in characters.
    #     # Stop if the widget is too small to draw anything.
    #     # Correct for terminal aspect ratio (characters are ~2x tall).
    #     self.frames = load_avatar("robo", (16, 16))

    def on_unmount(self):
        self._watcher_task.cancel()
        self.interval.stop()
        self.timer.stop()

    def watch_animation_name(self):
        self.interval.pause()
        self.current_frame_step = 0
        # if len(self.get_current_animation_frames()) == 0:
        #     # width = self.size.width // 2
        #     # height = self.size.height
        #     self.frames[self.animation_name][self.direction]

        self.interval.resume()

    def get_current_animation_frames(self):
        try:
            return self.frames[self.animation_name][self.direction]
        except Exception as e:
            print(e)
            return []

    def get_current_frame(self):
        frames = self.get_current_animation_frames()
        if len(frames) == 0:
            return None
        return frames[self.current_frame_step]

    def set_animation_name(self, animation_name):
        self.animation_name = animation_name

    def advance_frame(self):
        if len(self.frames[self.animation_name][self.direction]) == 0:
            raise Exception("No frames loaded. Check file path")
        self.current_frame_step = (self.current_frame_step + 1) % len(
            self.get_current_animation_frames()
        )

    def render(self):
        """Render the current frame of the animation."""
        return self.get_current_frame() or ""
