import gpiozero


class Button(object):
    def __init__(self, pin, color, when_activated):
        self.color = color
        self.pin = pin
        self.button = gpiozero.Button(pin, bounce_time=.05)
        self.button.when_activated = when_activated
        if self.button.is_active:
            raise (RuntimeError("%s button appears to be stuck" % color))
