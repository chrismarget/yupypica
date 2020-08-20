import sys
import os
from os.path import basename
import copy
import pytz
import asyncio
import saturnv
import platform

from .button import Button
from .display import Display


button_count = 4


class Application(object):
    default_conf = {
        'log_level': 'warning',
        'clock_format': '%Y-%m-%d %H:%M:%S %Z',
        'palette': [
            # (name, foreground, background, mono, foreground_high, background_hi)
            # -or-
            # (name, like_other_name)
            ('background',  '', '', '', 'white',  'light gray'),

            ('logo',  '', '', '', 'dark blue',  'light gray'),

            ('header',      '', '', '', 'white', 'light blue'),
            ('app_name',    '', '', '', 'white', 'light blue'),
            ('screen_name', '', '', '', 'white',  'dark blue'),

            ('footer',      '', '', '', 'white', 'dark blue'),
            ('clock',    '', '', '', 'white', 'dark blue'),
            ('status', '', '', '', 'white',  'dark blue'),
        ],

        'button_colors': ['#070', '#44f', '#770', '#700'],
        'button_pins': [17, 22, 23, 27],
        'tz': 'utc',
    }

    def __init__(self):
        self.name = basename(sys.argv[0])
        self.tz = pytz.utc
        self.acceptor = self._accept_input

        self.log = saturnv.Logger()
        self.log.set_level(self.default_conf['log_level'])  # from defaults
        self.log.stderr_off() # don't disturb screen layout

        # TODO: Add command line options, uncomment this stanza
        #self.options = Options(self)
        #self.args = self.options.get_args()
        #self.conf = saturnv.AppConf(defaults=Application.default_conf, args=self.args)
        # ...and remove this line:
        self.conf = saturnv.AppConf(defaults=Application.default_conf)

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

        self.palette = copy.deepcopy(self.default_conf['palette'])
        self.asyncio_loop = asyncio.get_event_loop()

        self.display = Display(self)

    def is_linux(self):
        return platform.system() == "Linux"

    def is_pi(self):
        if not self.is_linux():
            return False

        return "Raspberry Pi" in open('/proc/cpuinfo').read()

    def accept_input(self, key):
        self.acceptor(key)

    def set_acceptor(self, acceptor):
        self.acceptor = self._accept_input

    def _accept_input(self, key):
        if key.lower() == 'q':
            raise urwid.ExitMainLoop()

    def __button_active_callback(self, b):
        self.display.button_event(data=b)

    def run(self):
        if not self.is_pi():
            self.log.warning("This isn't a Raspberry Pi")

        # TODO: Use subprocess module for this instead
        #if os.fork(): # child
        #    c = open("/tmp/child", "a")
        #    c.write("child")
        #    c.close()
        #    self.log.info("child starts keyboard")
        #    keyboard()
        #else:
        #    p = open("/tmp/parent", "a")
        #    p.write("parent")
        #    p.close()
        #    self.log.info("parent continues normally")

        self.display.start()


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
