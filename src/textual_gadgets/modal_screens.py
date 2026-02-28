"""ModalScreens."""

from typing import Iterable, Literal

from rich.console import ConsoleRenderable, RichCast
from rich.highlighter import Highlighter
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.suggester import Suggester
from textual.validation import Validator
from textual.widgets import Button, Input, Label


class YesNoScreen(ModalScreen[bool]):
    """Pop-up ModalScreen with a dialog to ask yes/no questions."""

    BUTTON_VARIANTS = ["default", "primary", "success", "warning", "error"]
    CSS = """
    YesNoScreen {
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
        message: str = "Are you sure?",
        yes: str = "Confirm",
        yes_variant: Literal["default", "primary", "success", "warning", "error"] = "success",
        no: str = "Cancel",
        no_variant: Literal["default", "primary", "success", "warning", "error"] = "error",
    ) -> None:
        """Screen with a dialog to ask yes/no questions.

        Attributes
        ----------
        message
            defines the message/question that is displayed
        yes
            defines the name displayed on the confirmation button
        yes_variant
            defines the Button.variant (design) of the confirmation button
        no
            the name displayed on the cancel button
        no_variant
            defines the Button.variant (design) of the cancel Button"""
        super().__init__()
        self._message = message
        self._yes = yes
        self._yes_variant = yes_variant if yes_variant in self.BUTTON_VARIANTS else "success"
        self._no = no
        self._no_variant = no_variant if no_variant in self.BUTTON_VARIANTS else "error"

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self._message, id="question"),
            Button(self._yes, variant=self._yes_variant, id="yes"),
            Button(self._no, variant=self._no_variant, id="no"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class UserInputScreen(ModalScreen[str]):
    """Pop-up ModalScreen to receive input from the user."""

    CSS = """
        UserInputScreen {
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
            #message {
                column-span: 2;
                height: 1fr;
                width: 1fr;
                content-align: center middle;
            }
        }
    """

    def __init__(
        self,
        message: ConsoleRenderable | RichCast | str = "Please input something",
        button_label: str = "Submit",
        button_variant: Literal["default", "primary", "success", "warning", "error"] = "primary",
        input_placeholder: str = "Please input something.",
        input_default: str = "",
        input_highlighter: Highlighter | None = None,
        password: bool = False,
        input_restrict: str | None = None,
        input_type: Literal["integer", "number", "text"] = "text",
        input_max_length: int = 0,
        input_suggester: Suggester | None = None,
        input_validators: Validator | list[Validator] | None = None,
        input_validate_on: Iterable[Literal["blur", "changed", "submitted"]] | None = None,
        input_tooltip: ConsoleRenderable | RichCast | str | None = None,
    ) -> None:
        super().__init__()
        self.label = Label(message, id="message")
        self.submit_button = Button(label=button_label, variant=button_variant, id="submit")
        self.input = Input(
            value=input_default,
            placeholder=input_placeholder,
            highlighter=input_highlighter,
            password=password,
            restrict=input_restrict,
            type=input_type,
            max_length=input_max_length,
            suggester=input_suggester,
            validators=input_validators,
            validate_on=input_validate_on,
            tooltip=input_tooltip,
            id="input",
        )

    def compose(self) -> ComposeResult:
        yield Grid(
            self.label,
            self.input,
            self.submit_button,
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self.dismiss(self.input.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(self.input.value)
