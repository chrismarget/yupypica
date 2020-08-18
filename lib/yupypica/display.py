from .screen_welcome import Welcome
from .screen_lines import Lines
import asyncio
import random
import datetime
import pytz
import time
import urwid


def now():
    tz = pytz.utc
    return datetime.datetime.now(tz=tz).strftime('%Y-%m-%d-%H:%M:%S%z')


class Display(object):
    palette = []
    button_count = 0
    last = 0

    def __init__(self, event_loop):
        header = self._init_header()
        footer = self._init_footer()

        self.main_box = urwid.Filler(
            Welcome()
        )

        self.frame = urwid.Frame(self.main_box, header, footer)

        self.main_loop = urwid.MainLoop(
            widget=self.frame,
            event_loop=urwid.AsyncioEventLoop(loop=event_loop)
        )

    def add_button(self, button):
        self.palette.append((self.button_count, '', '', '', 'black', button.color))
        self.button_count += 1

    def _init_header(self):
        self.title = urwid.Text("initial title", align='left')
        top_left = urwid.Padding(self.title, left=1)
        top_right = urwid.Padding(urwid.Text('yupypica', align='right'), right=1)
        return urwid.Columns([top_left, top_right])

    def _init_footer(self):
        self.ver_text = urwid.Text("v0.0", align='left')
        bottom_left = urwid.Padding(self.ver_text, left=1)
        self.clock = urwid.Text("", align='right')
        bottom_right = urwid.Padding(self.clock, right=1)
        return urwid.Columns([bottom_left, bottom_right])

    def set_title(self, title):
        self.title.set_text(title)

    def update_clock(self, loop, data):
        self.clock.set_text(now())
        self.main_loop.set_alarm_at(round(time.time()) + 1, self.update_clock)

    def populate_frame(self, loop=None, data=None):
        self.main_box.set_body(Lines(count=self.button_count, selected=self.last % self.button_count))
        self.last += 1

    def start(self):
        self.main_loop.screen.set_terminal_properties(colors=256)
        self.main_loop.screen.register_palette(self.palette)
        self.main_loop.set_alarm_at(int(time.time()) + 2, self.update_clock)
        self.main_loop.set_alarm_in(2, self.populate_frame)
        self.main_loop.run()
