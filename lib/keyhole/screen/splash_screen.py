import urwid

from .screen import Screen


class SplashScreen(Screen):
    logo = [
        "+====+         o ",
        "|####|     __ /  ",
        "|####|    /  X   ",
        "|####|   (  ' )  ",
        "|####|  / \__/   ",
        "|####|\/o   /    ",
        "|####|/    +====+",
        "|####/o / /|####|",
        "+===/o / X |####|",
        "   /    / \|####|",
        "  /\___/   |####|",
        " (    /    |####|",
        "  \__/     |####|",
        "  / /      |####|",
        " / /       +====+",
        " `/              ",
    ]

    constellation = [
        "                                        ",
        "                                        ",
        "                                        ",
        "                                        ",
        "                                        ",
        "                                        ",
        "                                        ",
        "      o                                 ",
        "            *                           ",
        "                                        ",
        "                                        ",
        "                .                       ",
        "                                        ",
        "                                        ",
        "                    *                   ",
        "                                        ",
        "                                        ",
        "                             o          ",
        "                    o                   ",
        "                                        ",
        "                          .             ",
        "                                        ",
        "                                        ",
    ]

    def __init__(self, loop, conf, display):
        super().__init__(loop, conf, display)

    def set_screen_name(self):
        self.display.set_screen_name("Welcome")

    def set_contents(self):
        self.display.set_body(self.build_logo(self.constellation))

    def set_status(self):
        self.display.set_status("Initializing")

    def set_theme(self):
        self.loop.screen.register_palette(self.display.palette["space"])

    def build_logo(self, lines):
        pile = []
        for line in lines:
            pile.append(urwid.Text(line, align="center"))
        pile.append(urwid.Text("", align="center"))
        pile.append(urwid.Text("", align="center"))
        pile.append(urwid.Text(self.conf["title"], align="center"))
        pile.append(urwid.Text(self.conf["subtitle"], align="center"))
        pile.append(urwid.Text("", align="center"))
        pile.append(urwid.Text(self.conf["app_version"], align="center"))
        pile = urwid.Pile(pile)
        pile = urwid.Filler(pile)
        return urwid.AttrMap(pile, "logo")
