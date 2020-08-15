import datetime
import pytz
import urwid


def now():
    return datetime.datetime.now(pytz.utc).strftime('%Y-%m-%d-%H:%M:%S%z')

class Display (object):
    def __init__(self):

        self.title = urwid.Text("initial title", align='left')
        top_left = urwid.Padding(self.title, left=1)

        top_right = urwid.Padding(urwid.Text('yupypica', align='right'), right=1)

        header = urwid.Columns([top_left, top_right])

        self.main_box = urwid.Filler(urwid.Text("text in MainBox", align='center'))

        self.ver_text = urwid.Text("v0.0", align='left')
        bottom_left = urwid.Padding(self.ver_text, left=1)

        self.clock = urwid.Text(now(), align='right')
        bottom_right = urwid.Padding(self.clock, right=1)

        footer = urwid.Columns([bottom_left, bottom_right])

        self.frame = urwid.Frame(self.main_box, header, footer)

        self.loop = urwid.MainLoop(self.frame, unhandled_input=self.exit_on_q())

    def set_title(self, title):
        self.title.set_text(title)

    def update_clock(self, loop, data):
        self.clock.set_text(now())
        loop.set_alarm_in(1, self.update_clock)

    def start(self):
        self.loop.set_alarm_in(1, self.update_clock)
        self.loop.run()

    def exit_on_q(key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
