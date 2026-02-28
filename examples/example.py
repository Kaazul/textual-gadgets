"""Example app that displays the widgets and screens."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static

from textual_gadgets._utils.utils import get_version
from textual_gadgets.modal_screens import UserInputScreen, YesNoScreen
from textual_gadgets.screens import PlaceholderScreen
from textual_gadgets.validators import IPv4Validator


class InputExampleScreen(Screen):
    CSS = """
    InputExampleScreen {
        Static {
            width: 70%;
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Screen for testing UserInput Screen")
        with Horizontal():
            yield Static("UserInputScreen vwith max length=30")
            yield Button("Short Greeting", id="greeting")
        with Horizontal():
            yield Static("Default value and IPv4Validator")
            yield Button("Enter IP", id="ip")
        with Horizontal():
            yield Static("Placeholder")
            yield Button("Enter EMail", id="mail")
        yield Label("Submitted User Result", id="result")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "greeting":
            self.app.push_screen(
                UserInputScreen(
                    message="Enter a short greeting!\nHover over the input field to get help.",
                    input_max_length=30,
                    input_tooltip="A maximum length of 30 characters is allowed.",
                ),
                self.get_user_input,
            )
        elif event.button.id == "ip":
            self.app.push_screen(
                UserInputScreen(
                    message="Enter IP address",
                    input_validators=IPv4Validator(),
                    input_validate_on=["submitted", "blur"],
                ),
                self.get_user_input,
            )
        elif event.button.id == "mail":
            pass

    def get_user_input(self, value: str) -> None:
        label = self.query_one("#result", Label)
        label.content = value


class MainScreen(Screen):
    """Main application menu."""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="menu"):
            yield Button("PlaceHolder Screen", id="placeholder")
            yield Button("User Input Examples", id="user_input")
            yield Button("Quit", id="quit_button", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        """Defines what happens when the screen is mounted/installed."""
        first_button = self.query_one("#placeholder", Button)
        first_button.focus()

    def action_focus_next(self) -> None:
        self.focus_next()

    def action_focus_previous(self) -> None:
        self.focus_previous()

    def action_activate(self) -> None:
        focused = self.focused
        if isinstance(focused, Button):
            focused.press()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "placeholder":
            self.app.push_screen(PlaceholderScreen())
        elif button_id == "quit_button":
            self.app.action_request_quit()
        elif button_id == "user_input":
            self.app.push_screen(InputExampleScreen())
        else:
            self.app.push_screen(PlaceholderScreen(title=event.button.label))


class ExampleApp(App):
    CSS_PATH = "example.tcss"
    BINDINGS = [
        ("q", "request_quit", "Quit"),
        ("escape", "back", "Back"),
        ("enter", "activate", "Activate"),
        Binding("up", "focus_previous", "Focus previous", show=False),
        Binding("down", "focus_next", "Focus next", show=False),
        Binding("ctrl+q", "request_quit", "Quit", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.title = "Example App"
        self.sub_title = get_version()

    async def on_mount(self) -> None:
        await self.push_screen(MainScreen())

    def action_back(self) -> None:
        if len(self.app.screen_stack) > 2:  # Avoid popping Main Screen
            self.app.pop_screen()

    def action_request_quit(self) -> None:
        """Displays the quit screen."""

        def check_quit(is_quit: bool | None) -> None:
            """Called when Quitscreen is dismissed."""
            if is_quit:
                self.exit()

        self.push_screen(
            YesNoScreen("Do you really want to quit?", yes_variant="error", no_variant="primary"),
            check_quit,
        )

    def action_get_user_input(self) -> None:
        """Displays the User input screen"""

        def notify_user_input(value: str) -> None:
            self.notify(value, timeout=5)

        self.push_screen(UserInputScreen(), notify_user_input)


if __name__ == "__main__":
    ExampleApp().run()
