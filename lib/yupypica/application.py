from .button import Button
from .display import Display
import asyncio
import saturnv

button_count = 4


class Application(object):
    default_conf = {
        "button_colors": ["#070", "#44f", "#770", "#700"],
        "button_pins": [17, 22, 23, 27],
        "tz": "utc",
    }

    def __init__(self):
        conf = saturnv.AppConf(defaults=Application.default_conf)

        try:
            check_config(button_count, conf)
        except Exception as e:
            raise (e)

        loop = asyncio.get_event_loop()
        self.display = Display(loop)

        for i in range(button_count):
            pin = conf["button_pins"][i]
            color = conf["button_colors"][i]
            # if i == 0:
            #     b = Button(pin, color, self.__buttoncallback0)
            #     self.display.add_button(b)
            # elif i == 1:
            #     b = Button(pin, color, self.__buttoncallback1)
            #     self.display.add_button(b)
            # elif i == 2:
            #     b = Button(pin, color, self.__buttoncallback2)
            #     self.display.add_button(b)
            # elif i == 3:
            #     b = Button(pin, color, self.__buttoncallback3)
            #     self.display.add_button(b)

            b = Button(pin, color, self.__button_active_callback)
            self.display.add_button(b)

    # def __buttoncallback0(self):
    #     self.display.button_event(data=0)
    #
    # def __buttoncallback1(self):
    #     self.display.button_event(data=1)
    #
    # def __buttoncallback2(self):
    #     self.display.button_event(data=2)
    #
    # def __buttoncallback3(self):
    #     self.display.button_event(data=3)

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
