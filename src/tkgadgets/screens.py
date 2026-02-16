from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Label, Button


class QuestionScreen(ModalScreen[bool]):
    """Screen with a dialog to ask yes/no questions."""

    BUTTON_VARIANTS = ["default", "primary", "success", "warning", "error"]

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
        self._yes_variant = (
            yes_variant if yes_variant in self.BUTTON_VARIANTS else "success"
        )
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

    def __init__(self, title: str="Not Implemented",
                 message: str="This functionality is not implemented yet.") -> None:
        super().__init__()
        self.title = title
        self.message = message

    def compose(self):
        with Vertical(id="not-implemented"):
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