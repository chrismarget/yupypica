from gpiozero import Button as gzbutton

class Button(object):
    def __init__(self, pin, color):
        self.color = color
        self.button = gzbutton(pin)
        if self._is_pressed():
            RuntimeError("%s button appears to be stuck" % color)

    def _is_pressed(self):
        # todo: this should return true sometimes
        return False