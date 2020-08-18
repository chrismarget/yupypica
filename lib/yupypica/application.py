from .button import Button
from .display import Display
import asyncio
import saturnv


class Application(object):
    default_conf = {
        "button_colors": ["#070", "#44f", "#770", "#700"],
        "button_pins": [17, 22, 23, 27],
        "tz": "utc"
    }

    def __init__(self):
        conf = saturnv.AppConf(defaults=Application.default_conf)
        button_count = 4

        # Sanity check button color count
        bcc = len(conf["button_colors"])
        if bcc != button_count:
            raise (RuntimeError("configured with %d button_colors, expect %d" % (bcc, button_count)))

        # Sanity check button pin count
        bpc = len(conf["button_pins"])
        if bpc != button_count:
            raise (RuntimeError("configured with %d button_pins, expect %d" % (bpc, button_count)))

        loop = asyncio.get_event_loop()
        self.display = Display(loop)

        for i in range(button_count):
            pin = conf["button_pins"][i]
            color = conf["button_colors"][i]
            b = Button(pin, color, self.__buttonactivecallback)
            self.display.add_button(b)

    def __buttonactivecallback(self, b):
        self.display.populate_frame()

    def run(self):
        self.display.start()
