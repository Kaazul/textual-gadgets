"""Screens."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label


class PlaceholderScreen(Screen):
    """Simple Placeholder Screen for not yet implemented functionalities."""

    CSS = """
    #placeholder {
        width: 60;
        padding: 2;
        border: round $accent;
        background: $panel;
        align: center middle;
    }
    #message {
        content-align: center middle;
        margin-bottom: 2;
    }
"""

    def __init__(
        self,
        title: str = "Placeholder",
        message: str = "This functionality is not implemented yet.",
        show_header: bool = True,
        show_footer: bool = True,
    ) -> None:
        super().__init__()
        self.title = title
        self.message = message
        self.show_header = show_header
        self.show_footer = show_footer

    def compose(self) -> ComposeResult:
        if self.show_header:
            yield Header()
        if self.show_footer:
            yield Footer()
        with Vertical(id="placeholder"):
            yield Label(
                f"{self.title}\n\n {self.message}",
                id="message",
            )
            yield Button("Back", id="back")

    def on_mount(self) -> None:
        self.query_one("#back", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
