
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
from .screen import Splash
from .screen import Main


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

        'gpio_keyboard_info': {
            # pin: (color, key)
            17: ('#070', 'KEY_1'),
            22: ('#44f', 'KEY_Q'),
            23: ('#770', 'KEY_A'),
            27: ('#700', 'KEY_Z'),
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
        if is_pi() and os.geteuid() == 0:
            import uinput
            from .gpio_kb import GPIOKeyBoard
            signal.signal(signal.SIGCHLD, signal.SIG_IGN) # ignore SIGCHLD to prevent a zombie
            child_pid = os.fork()
            if not child_pid: # in child process
                pin_to_event = {
                    i[0]: getattr(uinput,i[1][1]) for i in self.conf['gpio_keyboard_info'].items()
                }
                self.gkbd = GPIOKeyBoard(pin_to_event, self.log).run()
                sys.exit() # the child process must exit here.

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

        # Kill the GPIO keyboard (if we managed to create one)
        if child_pid:
            os.kill(child_pid, signal.SIGTERM)

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
