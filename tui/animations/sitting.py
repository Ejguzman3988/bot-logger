from time import monotonic
from typing import Text
from textual.app import App, ComposeResult
from textual.widgets import Static
from rich_pixels import Pixels


class SpriteAnimation(Static):
    """A widget that displays a dynamically resized animation."""

    def on_mount(self) -> None:
        """Set up the animation timer and initial state."""
        self.frames: list[Pixels] = []
        self.current_frame = 0
        # The timer just advances the frame, it doesn't load data.
        self.set_interval(1 / 12, self._advance_frame)

    def on_resize(self) -> None:
        """Called when the widget is resized. Load frames here."""
        # Get the available space in characters.
        width = self.size.width
        height = self.size.height

        # Stop if the widget is too small to draw anything.
        if not width or not height:
            self.frames = []
            return

        # Correct for terminal aspect ratio (characters are ~2x tall).
        pixel_height = height * 2
        new_frames = []
        file_path = "images/robo-sitting"

        # Load each frame, resizing it to fit the new dimensions.
        for i in range(1, 13):
            try:
                # Use the 'resize' parameter here.
                frame = Pixels.from_image_path(
                    f"{file_path}/robo-{i}.png", resize=(width, pixel_height)
                )
                new_frames.append(frame)
            except Exception as e:
                # Log errors if a frame fails to load.
                self.log.error(f"Failed to load frame {i}: {e}")

        self.frames = new_frames
        self.refresh()  # Request a repaint with the new frame.

    def _advance_frame(self) -> None:
        """Advances the animation to the next frame."""
        if self.frames:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.refresh()

    def render(self) -> Pixels | Text:
        """Render the current animation frame."""
        # Render a frame only if the list isn't empty.
        if self.frames:
            return self.frames[self.current_frame]
        else:
            # Return empty text if there are no frames to show.
            return Text("")


class Animation(Static):
    """A widget to display a simple animation."""

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        # A list of frames for the animation
        self.frames = ["|", "/", "-", "\\"]
        self.current_frame = 0

        # Set a timer to call the _advance_frame method every 1/10th of a second
        self.set_interval(1 / 10, self._advance_frame)

    def _advance_frame(self) -> None:
        """Called by the timer to advance to the next frame."""
        # Cycle through the frames using the modulo operator
        self.current_frame = (self.current_frame + 1) % len(self.frames)

        # Call refresh() to tell Textualize to re-render the widget
        self.refresh()

    def render(self) -> str:
        """Render the current frame of the animation."""
        return self.frames[self.current_frame]


class AnimationApp(App):
    """A simple app to display the animation widget."""

    def compose(self) -> ComposeResult:
        yield SpriteAnimation()
