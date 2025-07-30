from textual.app import App
from textual.containers import Center
from app.widgets.Avatar import Avatar


class MainApp(App):
    """A simple app to display the animation widget."""

    CSS_PATH = "main.css"

    def compose(self):
        with Center():
            yield Avatar()

    # def on_mount(self):
    #     yield Container()
