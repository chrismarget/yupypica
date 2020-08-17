from .button import Button
from .display import Display
import asyncio
import saturnv

class Application (object):
    default_conf = {
        "button_colors": ["Green", "Blue", "Yellow", "Red"],
        "button_pins": [17,22,23,27],
    }

    def __init__(self):
        conf = saturnv.AppConf(defaults=Application.default_conf)
        loop = asyncio.get_event_loop()
        self.display = Display(loop)

        buttons = [
            Button(conf["button_pins"][0],conf["button_colors"][0]),
            Button(conf["button_pins"][1],conf["button_colors"][1]),
            Button(conf["button_pins"][2],conf["button_colors"][2]),
            Button(conf["button_pins"][3],conf["button_colors"][3]),
        ]

        for b in buttons:
            print ("press the %s button" % b.color)
            b.button.wait_for_active()
            print(b.color)

        # print ("press each button:")
        # buttons["A"].button.wait_for_active()
        # print("A")
        # buttons["B"].button.wait_for_active()
        # print("B")
        # buttons["C"].button.wait_for_active()
        # print("C")
        # buttons["D"].button.wait_for_active()
        # print("D")

        # def button_callback(channel):
        #     print("Button was pushed!")
        #
        #
        # button_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(button_loop)

        # self.display = Display(button_loop)



    def run(self):
        self.display.start()
