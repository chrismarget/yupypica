import urwid
from urwid import AttrMap

from .screen import Screen


class MainScreen(Screen):
    def __init__(self, loop, conf, display):
        super().__init__(loop, conf, display)

    def set_contents(self):
        buttons = {
            "f13": 'Sign a Certificate',
            "f14": 'Examine a Certificate',
            "f15": 'Revoke a Certificate',
            "f16": 'Delete a Certificate',
        }

        items = []
        for key in buttons:
            items.append(urwid.Divider(' '))
            items.append(AttrMap(urwid.Button(buttons[key]), key))
        items = urwid.SimpleFocusListWalker(items)
        items = urwid.ListBox(items)
        items = urwid.Padding(items, align='center', width=('relative', 50))

        self.display.set_body(items)

    def set_screen_name(self):
        self.display.set_screen_name("Main Menu")

    def set_status(self):
        self.display.set_status("")

    def set_theme(self):
        self.loop.screen.register_palette(self.display.palette['main'])