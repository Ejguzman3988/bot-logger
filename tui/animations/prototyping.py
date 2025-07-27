import os
import random
from PIL import Image, ImageDraw

from rich_pixels import Pixels
from textual.app import App, ComposeResult
from textual.widgets import Static, Label

# --- Configuration ---
# Made viewport smaller to easily see both images overlapping
VIEWPORT_WIDTH = 100
VIEWPORT_HEIGHT = 100
MASTER_IMAGE_WIDTH = 1536
MASTER_IMAGE_HEIGHT = 128
CROP_TOP_OFFSET = 32
SCROLL_STEP = 128
IMAGE_PATH = "images/Walking.png"
SCROLL_INTERVAL = 0.1
MIN_INTERVAL = 0.05  # Minimum time in seconds
MAX_INTERVAL = 0.4  # Maximum time in seconds


# This helper function doesn't need to change, but ensure it creates an RGBA image
def create_placeholder_image():
    if os.path.exists(IMAGE_PATH):
        return
    print(f"Creating a placeholder image named '{IMAGE_PATH}'...")
    # ✅ Create an RGBA image to ensure it has a transparency channel
    image = Image.new("RGBA", (MASTER_IMAGE_WIDTH, MASTER_IMAGE_HEIGHT))
    draw = ImageDraw.Draw(image)
    # Make a simple gradient with transparency for easy testing
    for i in range(MASTER_IMAGE_WIDTH):
        alpha = int(255 * (i / MASTER_IMAGE_WIDTH))  # Fades from transparent to red
        draw.line([(i, 0), (i, MASTER_IMAGE_HEIGHT)], fill=(255, 0, 0, alpha))
    image.save(IMAGE_PATH)


class ScrollerData:
    """
    A plain Python class to manage the state of one scrolling image.
    This is NOT a widget.
    """

    def __init__(self, image_path: str, crop_left_offset=0):
        self.master_image = Image.open(image_path).convert("RGBA")
        self.crop_left_offset = crop_left_offset
        self.x_offset = 0

    def scroll(self):
        """Moves the scroller to the next frame."""
        self.x_offset = (self.x_offset + SCROLL_STEP) % self.master_image.width

    def get_slice(self):
        """Crops the master image and returns the Pillow Image slice."""
        left = self.x_offset + self.crop_left_offset
        top = CROP_TOP_OFFSET
        right = left + VIEWPORT_WIDTH
        bottom = top + VIEWPORT_HEIGHT
        right = min(right, self.master_image.width)
        return self.master_image.crop((left, top, right, bottom))


class Scene(Static):
    """
    A single widget that composes two images together before rendering.
    """

    def on_mount(self) -> None:
        # Create our two data sources
        self.p1_data = ScrollerData(IMAGE_PATH)
        self.p2_data = ScrollerData(IMAGE_PATH)
        # Set a timer to uggpdate the animation
        self.set_timer(random.uniform(MIN_INTERVAL, MAX_INTERVAL), self.tick)

    def tick(self) -> None:
        """Animation tick: scroll data sources and refresh the widget."""
        self.p1_data.scroll()
        self.p2_data.scroll()
        self.refresh()  # Trigger a re-render
        self.set_timer(random.uniform(MIN_INTERVAL, MAX_INTERVAL), self.tick)

    def render(self) -> Pixels:
        """
        This is where the magic happens. We composite the images here.
        """
        # 1. Create a blank, transparent canvas for our scene
        canvas = Image.new("RGBA", (VIEWPORT_WIDTH, VIEWPORT_HEIGHT), (0, 0, 0, 0))

        # 2. Get the current image slice from each data source
        p1_slice = self.p1_data.get_slice()
        p2_slice = self.p2_data.get_slice()
        # p2_slice = self.p2_data.get_slice().transpose(Image.FLIP_LEFT_RIGHT)

        # 3. Paste the first image onto the canvas.
        # The offset places it to the left of center.
        canvas.paste(p1_slice, (-36, 0), p1_slice)

        # 4. Create a temporary canvas for the second image to handle its offset.
        p2_canvas = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        p2_canvas.paste(p2_slice, (15, 0), p2_slice)

        # 5. ✅ Use alpha_composite to correctly blend the second image ON TOP of the first.
        # This correctly handles transparency between the images.
        final_image = Image.alpha_composite(canvas, p2_canvas)

        # 6. Return the single, perfectly composited image for rendering.
        return Pixels.from_image(final_image)


class ScrollerApp(App):
    """The main application, now much simpler."""

    CSS = """
    Screen {
        align: center middle;
    }
    Scene {
        width: auto;
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        # We only need to yield our one Scene widget
        create_placeholder_image()
        yield Scene()
        yield Label("Image pre-compositing in action!")
