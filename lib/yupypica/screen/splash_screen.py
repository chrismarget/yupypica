import urwid

from .screen import Screen

class SplashScreen(Screen):
    logo = [
        "                         o          ",
        ",   ..   .,---.,   .,---..,---.,---.",
        "|   ||   ||   ||   ||   |||    ,---|",
        "`---|`---'|---'`---||---'``---'`---^",
        "`---'     |    `---'|               ",
        "",
        "Stand-alone Certificate Authority",
    ]

    def __init__(self, loop, conf, display):
        super().__init__(loop, conf, display)

    def set_screen_name(self):
        self.display.set_screen_name("Welcome")

    def set_contents(self):
        self.display.set_body(self.build_logo())

    def set_status(self):
        self.display.set_status("Initializing")

    def build_logo(self):
        pile = []
        for line in self.logo:
            pile.append(urwid.Text(line, align='center'))
        pile.append(urwid.Text(self.conf['app_version'], align='center'))

        return urwid.AttrMap(urwid.Pile(pile), 'logo')

