import urwid


class Screen(object):
    def __init__(self, loop, conf, display):
        self.loop = loop
        self.conf = conf
        self.display = display

    def activate(self, loop=None, data=None):
        self.display.set_status("")

        self.set_screen_name()
        self.set_contents()
        self.set_status()
        self.set_keys()
        self.set_theme()

    def set_screen_name(self):
        pass

    def set_contents(self):
        pass

    def set_status(self):
        pass

    def set_keys(self):
        pass

    def set_theme(self):
        self.loop.screen.register_palette(self.display.palette['main'])