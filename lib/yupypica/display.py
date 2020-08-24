import datetime
import math
import time
from urwid import ExitMainLoop, AttrMap, Columns, Filler, Frame, Text, Padding



class Display(object):
    palette = []
    button_count = 0
    last = 0

    def __init__(self, app):
        self.app = app
        self.palette = self.theme_to_palette()

        app.loop.screen.set_terminal_properties(colors=88)
        # NOTE: Add extr palette entries here
        app.loop.screen.register_palette(self.palette)

        header = self._init_header()
        footer = self._init_footer()
        self.main_box = Filler(Text(''))
        self.frame = AttrMap(Frame(self.main_box, header, footer), 'background')

    def activate(self):
        self.app.loop.widget = self.frame

    def theme_to_palette(self):
        theme = self.app.conf.get('theme', {})
        palette = []
        for name, colors in theme.items():
            palette.append((name, '', '', '', *colors))
        return palette

    def unhandled_input(self, key):
        raise ExitMainLoop()

    def add_button(self, button):
        self.palette.append((self.button_count, "", "", "", "black", button.color))
        self.button_count += 1

    def _init_header(self):
        self.app_name = Text(self.app.name, align='right')
        self.screen_name = Text("...")
        header = Columns([
            AttrMap(Padding(self.screen_name, align="left", left=1), 'screen_name'),
            AttrMap(self.app_name, 'app_name'),
        ])
        return AttrMap(header, 'header')

    def _init_footer(self):
        self.clock = Text("")
        self.status = Text("Idle", align='right')
        return AttrMap(Columns([
            AttrMap(self.clock, 'clock'),
            AttrMap(self.status, 'status'),
            ]), 'footer')

    def set_screen_name(self, screen_name):
        self.screen_name.set_text(screen_name)

    def set_status(self, status):
        self.status.set_text(status)

    def update_clock(self, loop, data=None):
        now = datetime.datetime.now(tz=self.app.tz)
        self.clock.set_text(now.strftime(self.app.conf['clock_format']))

        next_second = math.ceil(time.time())
        #self.app.main_loop.set_alarm_at(next_second, self.update_clock)
        loop.set_alarm_at(next_second, self.update_clock)

    def set_body(self, body):
        self.main_box.set_body(body)

#    def button_event(self, loop=None, data=None):
#        self.populate_frame(loop=loop, data=data)

