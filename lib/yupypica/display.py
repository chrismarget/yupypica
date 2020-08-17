import asyncio
import datetime
import pytz
import time
import urwid


def now():
    return datetime.datetime.now(pytz.utc).strftime('%Y-%m-%d-%H:%M:%S%z')


class Display (object):
    palette = [
        # (name, foreground, background, mono, foreground_high, background_hi)
        # -or-
        # (name, like_other_name)
        ('rev_red', '', '', '', 'black', '#700'),
        ('rev_green', '', '', '', 'black', '#070'),
        ('rev_yellow', '', '', '', 'black', '#770'),
        ('rev_blue', '', '', '', 'black', '#007'),
        # ('rev_green', '', '', '', 'black', 'light_green'),
        # ('rev_yellow', '', '', '', 'black', 'light_yellow'),
        # ('rev_blue', '', '', '', 'black', 'light_blue'),
        ('background', '', '', '', 'g15', 'g11'),
        ('header', '', '', '', '#006', '#fd0'),
        ('footer', '', '', '', 'g70', 'g23'),
        ('listbox', '', '', '', 'g58', 'g23'),
        ('listbox2', '', '', '', '#66f', 'g23'),
        ('listempty', '', '', '', 'g46', 'g23'),
        ('listtitle', '', '', '', '#a60', 'g15'),
        ('listitem', '', '', '', '#0d6', 'g23'),
        ('listbutton', '', '', '', '#fa0', '#066'),
    ]


    def __init__(self, event_loop):

        header = self._init_header()
        footer = self._init_footer()
        # self.main_box = urwid.Filler(urwid.AttrMap(urwid.Text("text in MainBox", align='center'), "lbx2"))
        # self.main_box = urwid.AttrMap(urwid.Filler(urwid.Text("rev_red", "text in MainBox", align='center')),"listbox2")
        self.main_box = urwid.Filler(
            urwid.Text(
                ('rev_blue', "text in MainBox"),
                align='center',
            )
        )
        self.frame = urwid.Frame(self.main_box, header, footer)

        self.main_loop = urwid.MainLoop(
            widget=self.frame,
            palette=self.palette,
            unhandled_input=self.exit_on_q,
            event_loop=urwid.AsyncioEventLoop(loop=event_loop)
        )
        self.main_loop.screen.set_terminal_properties(colors=256)

        self.button_callbacks = []

    def add_button_callback(self, func):
        self.button_callbacks.append(func)

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

    def start(self):
        self.main_loop.set_alarm_at(int(time.time()) + 2, self.update_clock)
        self.main_loop.run()

    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()




