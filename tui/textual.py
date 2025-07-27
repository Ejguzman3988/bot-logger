from time import monotonic

from textual import on
from textual.app import App
from textual.containers import HorizontalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Button, Static


class StopWatch(Static):
    """Simple stop watch component to start and stop timers"""

    button_text = reactive("Start")

    @on(Button.Pressed)
    def change_text(self):
        startButton = self.query_one("Button")
        if self.button_text == "Stop":
            self.button_text = "Start"
            startButton.label = self.button_text
            self.query_one(Timer).stop()
        else:
            self.button_text = "Stop"
            startButton.label = self.button_text
            self.query_one(Timer).start()

    def compose(self):
        yield Timer()
        yield StartButton()


class Timer(Static):
    """Display Timer"""

    time_elapsed = reactive(0)
    start_time = 0
    accumalated_time = 0

    def on_mount(self):
        """"""
        self.update_timer = self.set_interval(
            1 / 60,
            self.update_time_elapsed,
            name="update_time_elapsed",
            pause=True,
        )

    def update_time_elapsed(self):
        self.calc_time_elapsed()

    def watch_time_elapsed(self):
        time = self.time_elapsed
        time, seconds = divmod(time, 60)
        hours, minutes = divmod(time, 60)
        time_string = f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
        self.update(time_string)

    def calc_time_elapsed(self):
        if self.start_time == 0:
            self.start_time = monotonic()
        else:
            self.time_elapsed = self.accumalated_time + (monotonic() - self.start_time)

    def start(self):
        """Start keeping track of time elapsed"""
        self.update_timer.resume()
        self.start_time = monotonic()

    def stop(self):
        """Stop Keeping Track of time elapsed"""
        self.update_timer.pause()
        self.accumalated_time = self.time_elapsed


class StartButton(Button):
    """
    Start Button wraps the Button widget
    Adds button_text state: Start | Stop
    @on(Button.Pressed) =>
        Find child button, update label

    NOTE:
    Since this is a wrapper around the button widget
    To see the change I had to get the button child
    Then change the label automatically
    It doesn't automatically do it for you
    """

    # State:

    def watch_button_text(self):
        if self.button_text == "Start":
            self.add_class("started")
        else:
            self.add_class("stoped")


class Layout(Static):
    """Bot Avatar widget"""

    def compose(self):
        x = 0
        while x < 10:
            yield StopWatch(id=f"stopwatch-{x}")
            x += 1


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

    # The on handler
    # @on(Button.Pressed, '#test-button')
    # def print(self):
    #     print(Button.Pressed)

    BINDINGS = [("d", "cycle_colorscheme", "Toggle dark mode")]

    CSS_PATH = "textual.css"

    def compose(self):
        self.theme_index = 0
        """What widgets is the app composed of"""
        yield Header(show_clock=False)
        yield Footer()
        with HorizontalScroll():
            yield Layout()

    def action_cycle_colorscheme(self):
        themes = list(self.available_themes)
        self.theme_index = (self.theme_index + 1) % len(themes)
        self.theme = themes[self.theme_index]
