import urwid

from .screen import Screen

class Main(Screen):
    def set_contents(self):
        self.app.display.set_body(urwid.Text(""))

    def set_screen_name(self):
        self.app.display.set_screen_name("Main Menu")

    def set_status(self):
        self.app.display.set_status("Idle")

