from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Header, Label


class QuestionScreen(ModalScreen[bool]):
    """Screen with a dialog to ask yes/no questions."""

    BUTTON_VARIANTS = ["default", "primary", "success", "warning", "error"]
    CSS = """
    QuestionScreen {
        align: center middle;
        #dialog {
            grid-size: 2;
            grid-gutter: 1 2;
            grid-rows: 1fr 3;
            padding: 0 1;
            width: 60;
            height: 11;
            border: thick $background 80%;
            background: $surface;
        }
        #question {
            column-span: 2;
            height: 1fr;
            width: 1fr;
            content-align: center middle;
        }
    }
"""

    def __init__(
        self,
        question: str = "Are you sure?",
        yes: str = "Confirm",
        yes_variant="success",
        no: str = "Cancel",
        no_variant: str = "error",
    ) -> None:
        """Screen with a dialog to ask yes/no questions.

        Attributes
        ----------
        question
            defines the question that is displayed
        yes
            defines the name displayed on the confirmation button
        yes_variant
            defines the Button.variant (design) of the confirmation button
        no
            the name displayed on the cancel button
        no_variant
            defines the Button.variant (design) of the cancel Button"""
        super().__init__()
        self._question = question
        self._yes = yes
        self._yes_variant = yes_variant if yes_variant in self.BUTTON_VARIANTS else "success"
        self._no = no
        self._no_variant = no_variant if no_variant in self.BUTTON_VARIANTS else "error"

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self._question, id="question"),
            Button(self._yes, variant=self._yes_variant, id="yes"),
            Button(self._no, variant=self._no_variant, id="no"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


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

    def compose(self):
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
