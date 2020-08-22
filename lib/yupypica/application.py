
import sys
import os
from os.path import basename
import asyncio
import saturnv
import sys
from dateutil import tz
from urwid import AsyncioEventLoop, MainLoop, ExitMainLoop, Filler, Text

from .button import Button
from .display import Display
from .gpio_kb import GPIOKeyBoard
from .options import Options
from .detect import is_pi, is_linux
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

        'button_colors': ['#070', '#44f', '#770', '#700'],
        'button_pins': [17, 22, 23, 27],
        'button_keys': ['KEY_1', 'KEY_Q', 'KEY_A', 'KEY_Z'],
    }

    def __init__(self):
        self.name = basename(sys.argv[0])
        self.acceptor = self._accept_input

        self.log = saturnv.Logger()
        self.log.set_level(self.default_conf['log_level'])  # from defaults
        self.log.stderr_off() # don't disturb screen layout

        # Parse command line arguments, and get the app configuration
        self.options = Options(self)
        self.args = self.options.get_args()
        self.conf = saturnv.AppConf(defaults=Application.default_conf, args=self.args)
        self.tz = tz.gettz(self.conf['clock_timezone'])

        self.log.set_level(self.conf['log_level'])  # from final config

#        try:
#            check_config(button_count, self.conf)
#        except Exception as e:
#            raise (e)
#
#        for i in range(button_count):
#            pin = conf["button_pins"][i]
#            color = conf["button_colors"][i]
#            b = Button(pin, color, self.__button_active_callback)
#            self.display.add_button(b)

        self.asyncio_loop = asyncio.get_event_loop()
        self.loop = MainLoop(
            widget=Filler(Text('...')),
            event_loop=AsyncioEventLoop(loop=self.asyncio_loop),
            unhandled_input=self.unhandled_input,
        )

        self.display = Display(self)

    def run(self):
        # TODO: Use subprocess module for this instead?
        if is_pi():
            if os.fork(): # child
                GPIOKeyBoard(self.conf['button_pins'], self.conf['button_keys']).run()

        self.display.activate()

        # Switch to splash screen and start clock
        Splash(self).activate()
        self.display.update_clock(self.loop)

        # Do any remaining start up work here

        # Switch to main menu after short time
        self.loop.set_alarm_in(2, Main(self).activate)

        # Start the reactor
        self.loop.run()

    def accept_input(self, key):
        self.acceptor(key)

    def set_acceptor(self, acceptor):
        self.acceptor = self._accept_input

    def _accept_input(self, key):
        if key.lower() == 'q':
            raise ExitMainLoop()

    def __button_active_callback(self, b):
        self.display.button_event(data=b)

    def unhandled_input(self, key):
        if key in 'qQ':
            raise ExitMainLoop()


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
