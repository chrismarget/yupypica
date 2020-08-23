import uinput
import signal
from time import sleep
from .detect import is_pi

if is_pi():
    import RPi.GPIO

class GPIOKeyBoard:
    def __init__(self, event_map, log):
        self.event_map = event_map
        self.log = log

        if not is_pi():
            return

        RPi.GPIO.setmode(RPi.GPIO.BCM) # Use Broadcom pin numbers rather than header pins

        # create the uinput (keyboard) device
        device = uinput.Device(event_map.values())
        self.kh = []
        for pin, event in event_map.items():
            self.kh.append(KeyHandler(device, event, pin))

    def run(self):
        if not is_pi():
            return

        for keyhandler in self.kh:
            keyhandler.start()

        signal.pause()


class KeyHandler:
    def __init__(self, device, event, pin):
        self.device = device
        self.event = event
        self.pin = pin

        RPi.GPIO.setup(pin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

    def start(self):
        RPi.GPIO.add_event_detect(self.pin, RPi.GPIO.FALLING,
                callback=self.debounce_and_click, bouncetime=100)

    def debounce_and_click(self, channel):
        sleep(0.05)
        if RPi.GPIO.input(channel) == 0:
            self.device.emit_click(self.event)
