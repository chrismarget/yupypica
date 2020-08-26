import RPi.GPIO


class Buttons:
    def __init__(self, loop, pins):
        self.loop = loop

        # Create the button handlers
        self.buttons = []
        for i in range(min(len(pins), 12)):  # only 12 Fn keys
            self.buttons.append(Button(loop, pins[i], "f" + str(i+1)))

    def activate(self):
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        for button in self.buttons:
            button.start()


class Button:
    def __init__(self, loop, pin, key):
        self.loop = loop
        self.pin = pin
        self.key = key

    def start(self):
        RPi.GPIO.setup(self.pin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        RPi.GPIO.add_event_detect(
            self.pin, RPi.GPIO.FALLING, callback=self.push, bouncetime=200
        )

    def push(self, pin):
        self.loop.process_input([self.key])
