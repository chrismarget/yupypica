import urwid

from .screen import Screen

class MainScreen(Screen):
    def set_contents(self):
        self.display.set_body(urwid.Text(""))

    def set_screen_name(self):
        self.display.set_screen_name("Main Menu")

    def set_status(self):
        self.display.set_status("")

