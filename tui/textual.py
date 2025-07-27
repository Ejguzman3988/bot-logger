from rich_pixels import Pixels
from textual.app import App, ComposeResult
from textual.widgets import Static


class ImageWidget(Static):
    """A widget to display a rich-pixels image."""

    def __init__(self, image_path):
        super().__init__()

        self.pixels = Pixels.from_image_path(image_path)

    def render(self):
        """The render method returns pixels object."""
        return self.pixels


class AvatarContainer(App):
    """
    This will be where out bot avatar will live.
    Used to minimize the need to animate the avatar.
    Avatar will be animated frame by frame.

    Examples:

    [action] - [bg animation]
    ---

    ** error  - flashing red bg
    * raid   - party mode

    Widgets will be added here.

    """

    CSS_PATH = "textual.css"

    def compose(self):
        yield ImageWidget("images/Walking.png")

    """ Events System """
    """ Async Events """
    """ Animations """
    """ Screens """
    """ Workers """
