
import sys
import time
import os
from os.path import basename
import asyncio
import saturnv
import signal
import sys
from dateutil import tz
from urwid import AsyncioEventLoop, MainLoop, ExitMainLoop, Filler, Text

from .display import Display
from .options import Options
from .detect import is_pi
from .screen import Splash, Main


class Application(object):
    default_conf = {
        'log_level': 'warning',
        'clock_format': '%Y-%m-%d %H:%M:%S %Z',
        'clock_timezone': 'utc',
        'theme': {
            # name:         [foreground, background]
            'background':   ['white', 'light gray'],
            'logo':         ['dark blue', 'light gray'],

            'header':       ['white', 'light blue'],
            'app_name':     ['white', 'light blue'],
            'screen_name':  ['white', 'dark blue'],

            'footer':       ['white', 'dark blue'],
            'clock':        ['white', 'dark blue'],
            'status':       ['white', 'dark blue'],
        },

        'gpio_keyboard_info': [
            (17, 'KEY_1', '#070'),
            (22, 'KEY_Q', '#44f'),
            (23, 'KEY_A', '#770'),
            (27, 'KEY_Z', '#700'),
        ],
    }

    def __init__(self):
        self.name = basename(sys.argv[0])

        # Start logger early (use default_conf's value temporarily and update it later)
        self.log = saturnv.Logger()
        self.log.set_level(self.default_conf['log_level'])
        self.log.stderr_off() # don't disturb screen layout

        # Parse command line arguments, and get the app configuration
        self.options = Options(self)
        self.args = self.options.get_args()
        self.conf = saturnv.AppConf(defaults=Application.default_conf, args=self.args)
        self.tz = tz.gettz(self.conf['clock_timezone'])

        # Finalize log level from fully-loaded config
        self.log.set_level(self.conf['log_level'])

        # Build the event loop. Use temp filler and replace it when Display starts rendering
        self.asyncio_loop = asyncio.get_event_loop()
        self.loop = MainLoop(
            widget=Filler(Text('...')),
            event_loop=AsyncioEventLoop(loop=self.asyncio_loop),
            unhandled_input=self.unhandled_input,
        )

        # Prepare button-to-keyboard linkage
        if is_pi() and os.geteuid() == 0:
            from .gpio_kb import GPIOKeyBoard
            self.gpio_keyboard = GPIOKeyBoard(self.conf['gpio_keyboard_info'])

        # Prep Display but don't activate it yet
        self.display = Display(self)

    def run(self):
        # Activate button-to-keyboard linkage
        if self.gpio_keyboard:
            self.gpio_keyboard.run()

        # Activate the display with full layout but no content
        self.display.activate()

        # Switch to splash screen and start the clock
        Splash(self).activate()
        self.display.update_clock(self.loop)

        # Do any remaining start up work here
        # ...

        # Switch to main menu after short time
        self.loop.set_alarm_in(2, Main(self).activate)

        # Start the reactor
        self.loop.run()

        # Leave an extra line to scroll screen
        print()

    def unhandled_input(self, key):
        if key in 'qQ':                 # Q at the top to exit cleanly
            raise ExitMainLoop()
        if key == 'ctrl l':             # Screen refresh (if screen gets overwritten or corrupted)
            self.loop.screen.clear()
            return True
        self.log.warning("Unhandled input: %s" % key)

