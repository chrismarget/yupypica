import pytz
import asyncio
import saturnv

from .button import Button
from .display import Display


button_count = 4


class Application(object):
    default_conf = {
        'log_level': 'warning',
        'clock_format': '%Y-%m-%d-%H:%M:%S%z',
        'palette': [
            # (name, foreground, background, mono, foreground_high, background_hi)
            # -or-
            # (name, like_other_name)
            ('background',  '', '', '', 'g15',  'g11'),
            ('header',      '', '', '', '#006', '#fd0'),
            ('footer',      '', '', '', 'g70',  'g23'),
            #('listbox',    '', '', '', '#0d6',  'g23'),
            ('listbox',     '', '', '', 'g58',  'g23'),
            ('listbox2',    '', '', '', '#66f',  'g23'),
            ('listempty',   '', '', '', 'g46',  'g23'),
            ('listtitle',   '', '', '', '#a60',  'g15'),
            ('listitem',    '', '', '', '#0d6',  'g23'),
            ('listbutton',  '', '', '', '#fa0',  '#066'),
        ],

        'button_colors': ['#070', '#44f', '#770', '#700'],
        'button_pins': [17, 22, 23, 27],
        'tz': 'utc',
    }

    def __init__(self):
        self.tz = pytz.utc

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

        self.loop = asyncio.get_event_loop()
        self.display = Display(self)


    def __button_active_callback(self, b):
        self.display.button_event(data=b)

    def run(self):
        self.display.start()


def check_config(count, conf):
    for element_name in ["button_colors", "button_pins"]:
        try:
            check_config_element(element_name, count, conf[element_name])
        except Exception as e:
            raise (e)


def check_config_element(name, count, element):
    # check overall length
    counted = len(element)
    if counted != count:
        raise (RuntimeError("%s has %d elements, expected %d" % (name, counted, count)))

    # count unique items
    d = {}
    for i in element:
        d[i] = None
    counted = len(d)
    if counted != count:
        raise (
            RuntimeError(
                "%s has %d unique elements, expected %d" % (name, counted, count)
            )
        )
