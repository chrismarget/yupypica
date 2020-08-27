import urwid

from .screen import Screen


class MainScreen(Screen):
    def __init__(self, loop, conf, display):
        super().__init__(loop, conf, display)

    def set_contents(self):
        buttons = ["a", "b", "c"]

        items = []
        for button in buttons:
            items.append(urwid.Button(button))
        items = urwid.SimpleFocusListWalker(items)
        items = urwid.ListBox(items)

        self.display.set_body(items)

    def set_screen_name(self):
        self.display.set_screen_name("Main Menu")

    def set_status(self):
        self.display.set_status("")
