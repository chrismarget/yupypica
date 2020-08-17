from .button import Button
from .display import Display
import asyncio
import saturnv
import time

class Application (object):
    default_conf = {
        "button_colors": ["#070", "#44f", "#770", "#700"],
        "button_pins": [17,22,23,27],
        "tz":"utc"
    }

    def __init__(self):
        conf = saturnv.AppConf(defaults=Application.default_conf)
        button_count = 4

        # Sanity check button color count and button pin count
        bcc = len(conf["button_colors"])
        if bcc != button_count:
            raise(RuntimeError("configured with %d button_colors, expect %d" % (bcc, button_count)))
        bpc = len(conf["button_pins"])
        if bpc != button_count:
            raise(RuntimeError("configured with %d button_pins, expect %d" % (bpc, button_count)))

        loop = asyncio.get_event_loop()
        self.display = Display(loop)

        for i in range(button_count):
            b = Button(conf["button_pins"][i],conf["button_colors"][i])
            self.display.add_to_palette(i, b.color)
            # self.display.add_button_callback(b.callback)

        # for b in buttons:
            # print ("press the %s button" % b.color)
            # b.button.wait_for_active()
            # print(b.color)
            # self.display.add_button_callback()

        # self.display.add_button_callback(Button(conf["button_pins"][0],conf["button_colors"][0]))

        # def button_callback(channel):
        #     print("Button was pushed!")
        #
        #
        # button_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(button_loop)

        # self.display = Display(button_loop)



    def run(self):
        self.display.start()

    def RedButton(self):
        self.display.set_title("red")

