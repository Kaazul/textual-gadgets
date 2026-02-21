"""Example app that displays the widgets and screens."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header

from textual_gadgets._utils.utils import get_version
from textual_gadgets.screens import PlaceholderScreen, QuestionScreen


class MainScreen(Screen):
    """Main application menu."""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="menu"):
            yield Button("PlaceHolder Screen", id="placeholder")
            yield Button("Quit", id="quit_button")
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
            QuestionScreen(
                "Do you really want to quit?", yes_variant="error", no_variant="primary"
            ),
            check_quit,
        )


if __name__ == "__main__":
    ExampleApp().run()
