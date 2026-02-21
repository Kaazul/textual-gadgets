# textual-gadgets
Widgets, functions and more for the python package textual

## Screens

    from textual_gadgets.screens import *

### QuestionScreen

QuestionScreen is a pop-up screen that displays a question and displays two buttons of
choice. It inherits from ModalScreen and depending on the button pressed returns True or
False if it is dismissed. The left button has the label "Success" per default, dismisses
the Screen and returns True. The right button has the label "Cancel" per default,
dismisses the Screen and returns True. Furthermore, the Button variants can be given.

### PlaceholderScreen

PlaceholderScreen is a small and simple screen to be used as a placeholder or
to signal that a functionality is not yet implemented. In the example app
PlaceholderScreen is also used in the case the on_button_pressed(message) method receives
an unknown message.

PlaceholderScreen has a default title and message. By default, a Footer and a Header is
also yielded in its compose method.
