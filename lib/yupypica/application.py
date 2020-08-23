
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

from .button import Button
from .display import Display
from .options import Options
from .detect import is_pi, is_linux
from .screen import Splash
from .screen import Main

if is_pi():
    from .gpio_kb import GPIOKeyBoard

button_count = 4


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

        # todo: discussion - I'm not completely convinced about the map
        #  below. It seems to me that all three "clicky" attributes (color,
        #  keystroke and GPIO pin) equally need to be mapped together.
        #  keeping them in three lists allows us to do that. In that case,
        #  index zero of all three lists (green/17/Key_1) allows us to keep
        #  track of them that way.
        #  .
        #  Alternatively, we could make two maps: a gpio_to_color map and
        #  a gpio_to_keystroke map.
        #  .
        #  I'm not sure which makes more sense yet.
        #  .
        #  Additional complications:
        #  - we might choose to map multiple keystrokes to the same action
        #  - we might choose to associate actions to keys not associated with
        #    a gpio pin. "q" for quit, for example.
        'button_colors': ['#070', '#44f', '#770', '#700'],
        'gpio_keyboard_map': {
            # pin: key
            17: 'KEY_1',
            22: 'KEY_Q',
            23: 'KEY_A',
            27: 'KEY_Z',
        },
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

        # Prep Display but don't activate it yet
        self.display = Display(self)

    def run(self):
        # On RPis, start the GPIO Keyboard process
        if is_pi():
            signal.signal(signal.SIGCHLD, signal.SIG_IGN) # ignore SIGCHLD to prevent a zombie
            if not os.fork(): # in child process
                self.gkbd = GPIOKeyBoard(self.conf['gpio_keyboard_map'], self.log)
                self.gkbd.run()
        # Continue in single or parent process

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

    def unhandled_input(self, key):
        if key in 'qQ':                 # Q at the top to exit cleanly
            raise ExitMainLoop()
        if key == 'ctrl l':             # Screen refresh (if screen gets overwritten or corrupted)
            self.loop.screen.clear()
            return True

        self.log.warning("Unhandled input: %s" % key)

    def __button_active_callback(self, b):
        self.display.button_event(data=b)


def check_config(count, conf):
    for element_name in ["button_colors", "button_pins"]:
        check_config_element(element_name, count, conf[element_name])

def check_config_element(name, count, element):
    # check overall length
    counted = len(element)
    if count != counted:
        raise (RuntimeError("%s has %d elements, expected %d" % (name, counted, count)))

    # count unique items
    counted = len(set(element))
    if count != counted:
        raise (
            RuntimeError(
                "%s has %d unique elements, expected %d" % (name, counted, count)
            )
        )
