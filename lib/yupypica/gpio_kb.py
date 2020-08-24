import RPi.GPIO

class GPIOKeyBoard:
    def __init__(self, loop, key_map):
        self.loop = loop
        self.key_map = key_map

        # Create the key handlers
        self.keyhandlers = []
        for this_key in key_map:
            pin = this_key[0]
            key = this_key[1]
            self.keyhandlers.append(KeyHandler(loop, pin, key))

    def run(self):
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        for keyhandler in self.keyhandlers:
            keyhandler.start()


class KeyHandler:
    def __init__(self, loop, pin, key):
        self.loop = loop
        self.pin = pin
        self.key = key

    def start(self):
        RPi.GPIO.setup(self.pin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        RPi.GPIO.add_event_detect(self.pin, RPi.GPIO.FALLING,
            callback=self.keystroke, bouncetime=200)

    def keystroke(self, pin):
        self.loop.process_input(self.key)

