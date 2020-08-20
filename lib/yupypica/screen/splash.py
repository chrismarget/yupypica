import urwid

from .screen import Screen

class Splash(Screen):
    logo = [
        "                              o            ",
        ",   . .   . ,---. ,   . ,---. . ,---. ,---.",
        "|   | |   | |   | |   | |   | | |     ,---|",
        "`---| `---' |---' `---| |---' ` `---' `---^",
        "`---'       |     `---' |                  ",
        "",
        "Stand-alone Certificate Authority",
        "Version 1.0.8",
    ]

    def __init__(self, app):
        super(Splash, self).__init__(app)

    def set_screen_name(self):
        self.app.display.set_screen_name("Welcome")

    def set_contents(self):
        self.app.display.set_body(self.build_logo())

    def set_status(self):
        self.app.display.set_status("Initializing")

    def build_logo(self):
        pile = []
        for line in self.logo:
            pile.append(urwid.Text(line, align='center'))

        return urwid.AttrMap(urwid.Pile(pile), 'logo')

