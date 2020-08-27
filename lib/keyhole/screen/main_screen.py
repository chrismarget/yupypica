import urwid
from urwid import AttrMap

from .screen import Screen

class MainScreen(Screen):
    def __init__(self, loop, conf, display):
        super().__init__(loop, conf, display)

    def set_contents(self):
        buttons = [
            'Sign a Certificate',
            'Examine a Certificate',
            'Revoke a Certificate',
            'Delete a Certificate',
        ]

        items = []
        for button in buttons:
            items.append(urwid.Divider(' '))
            items.append(AttrMap(urwid.Button(button), 'button'))
        items = urwid.SimpleFocusListWalker(items)
        items = urwid.ListBox(items)
        items = urwid.Padding(items, align='center', width=('relative', 50))

        self.display.set_body(items)

    def set_screen_name(self):
        self.display.set_screen_name("Main Menu")

    def set_status(self):
        self.display.set_status("")

