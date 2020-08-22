import uinput
import signal
from time import sleep
from .detect import is_pi

if is_pi():
    import RPi.GPIO

class GPIOKeyBoard:
    def __init__(self, pins, event_names):
        if not is_pi():
            return

        RPi.GPIO.setmode(RPi.GPIO.BCM)
        pin_to_event = dict()
        for i in range(len(pins)):
            pin = pins[i]
            # There should be an event associated with every pin
            try:
                event_name = event_names[i]
            except IndexError:
                raise RuntimeError("no key event associated with pin %d" % pin)

            # get the uinput event variable using the name (a string) passed via configuration
            try:
                event = getattr(uinput, event_name)
            except AttributeError:
                raise RuntimeError("uinput module has no event named '%s'" % event_name)

            # build up the pin_to_event dict
            pin_to_event[pin] = event

        # create the uinput (keyboad) device
        device = uinput.Device(pin_to_event.values())

        self.kh = list()
        for (pin, event) in pin_to_event.items():
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
        RPi.GPIO.add_event_detect(
            self.pin, RPi.GPIO.FALLING, callback=self.debounce_and_click, bouncetime=100
        )

    def debounce_and_click(self, channel):
        sleep(0.05)
        if RPi.GPIO.input(channel) == 0:
            self.device.emit_click(self.event)
