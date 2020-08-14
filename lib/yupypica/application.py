from .button import Button
from .display import Display
import saturnv

class Application (object):
    default_conf = {}

    def __init__(self):
        self.conf = saturnv.AppConf(defaults=Application.default_conf)
        self.buttons = {
            "A":Button(17,"Green"),
            "B": Button(22, "Blue"),
            "C": Button(23, "Yellow"),
            "D": Button(27, "Red"),
        }
        self.display = Display()

    def run(self):
        self.display.start()

