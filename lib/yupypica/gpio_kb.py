import uinput
import signal
import sys
import saturnv
from time import sleep
from .detect import is_pi
import RPi.GPIO


class GPIOKeyBoard:
    def __init__(self, event_map):
        self.event_map = event_map

        RPi.GPIO.setmode(RPi.GPIO.BCM) # Use Broadcom pin numbers rather than header pins

        # create the uinput (keyboard) device and keyhandlers
        self.device = uinput.Device([getattr(uinput, k[1]) for k in event_map])
        self.keyhandlers = []
        for event in event_map:
            key = getattr(uinput, event[1])
            pin = event[0]
            self.keyhandlers.append(KeyHandler(self.device, key, pin))

    def run(self):
        for keyhandler in self.keyhandlers:
            keyhandler.start()


class KeyHandler:
    def __init__(self, device, event, pin):
        self.device = device
        self.event = event
        self.pin = pin

    def start(self):
        RPi.GPIO.setup(self.pin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        RPi.GPIO.add_event_detect(self.pin, RPi.GPIO.FALLING,
            callback=self.keystroke, bouncetime=200)

    def keystroke(self, channel):
        self.device.emit_click(self.event)

