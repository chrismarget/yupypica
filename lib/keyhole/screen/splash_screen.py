import urwid
import time
import random

from .animate import overlay_multiline
from .screen import Screen
from .constellation import Constellation


class SplashScreen(Screen):
    logo = [
        "+====+888888888o8",
        "|####|88888__ /88",
        "|####|8888/  X888",
        "|####|888(  ' )88",
        "|####|88/ \__/888",
        "|####|\/o   /8888",
        "|####|/    +====+",
        "|####/o / /|####|",
        "+===/o / X |####|",
        "888/    /8\|####|",
        "88/\___/888|####|",
        "8(    /8888|####|",
        "88\__/88888|####|",
        "88/ /888888|####|",
        "8/ /8888888+====+",
        "8`/88888888888888",
    ]

    def __init__(self, loop, conf, display):
        self.starfield = Constellation().get_rand()
        self.star_delay = 1
        self.frame_delay = .06
        self.elevation = random.randint(0, len(self.starfield) - len(self.logo))
        super().__init__(loop, conf, display)

    def set_screen_name(self):
        self.display.set_screen_name("Welcome")

    def set_contents(self, loop=None, data=None):
        if data == None:
            self.display.set_body(self.build_logo(self.starfield))
        else:
            lines = overlay_multiline(
                self.starfield,
                self.logo,
                transparent="8",
                idx=data,
                skiplines=self.elevation,
            )
            self.display.set_body(self.build_logo(lines))

    def set_status(self):
        self.display.set_status("Initializing")

    def set_theme(self):
        self.loop.screen.register_palette(self.display.palette["space"])

    def build_logo(self, lines, data=None):
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

    def animate(self):
        frames = len(self.logo[0]) + len(self.starfield[0])
        start = time.time() + self.star_delay
        for i in range(frames):
            alarm = start + (i * self.frame_delay)
            self.loop.set_alarm_at(alarm, self.set_contents, i)

    def activate(self, loop=None, data=None):
        self.display.set_status("")
        self.set_screen_name()
        self.set_contents()
        self.set_status()
        self.set_keys()
        self.set_theme()
        self.animate()
