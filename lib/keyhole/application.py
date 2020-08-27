import sys
import time
import os
from os.path import basename
import asyncio
import saturnv
import sys
from urwid import AsyncioEventLoop, MainLoop, ExitMainLoop, Filler, Text

from .display import Display
from .options import Options
from .detect import is_pi
from .screen import SplashScreen, MainScreen
from .version import get_version


class Application(object):
    default_conf = {
        "log_level": "warning",
        "clock_format": "%Y-%m-%d %H:%M:%S %Z",
        "clock_timezone": "utc",
        "theme": {
            # name:         [foreground, background]
            "background": ["white", "light gray"],
            "logo": ["dark blue", "light gray"],
            "header": ["white", "light blue"],
            "app_name": ["white", "light blue"],
            "screen_name": ["white", "dark blue"],
            "footer": ["white", "dark blue"],
            "clock": ["white", "dark blue"],
            "status": ["white", "dark blue"],
        },
        "pin_color_map": {17: "#070", 22: "#44f", 23: "#770", 27: "#700",},
    }

    def __init__(self):

        # Start logger early (use default_conf's value temporarily and update it later)
        self.log = saturnv.Logger()
        self.log.set_level(self.default_conf["log_level"])
        self.log.stderr_off()  # don't disturb screen layout

        # Parse command line arguments, and get the app configuration
        self.options = Options(self)
        self.args = self.options.get_args()
        self.conf = saturnv.AppConf(defaults=Application.default_conf, args=self.args)
        self.conf["app_version"] = get_version()

        # Finalize log level from fully-loaded config
        self.log.set_level(self.conf["log_level"])

        # Build the event loop. Use temp filler and replace it when Display starts rendering
        self.asyncio_loop = asyncio.get_event_loop()
        self.loop = MainLoop(
            widget=Filler(Text("...")),
            event_loop=AsyncioEventLoop(loop=self.asyncio_loop),
            unhandled_input=self.unhandled_input,
        )

        # Prepare button-to-keyboard linkage
        if is_pi() and os.geteuid() == 0:
            from .buttons import Buttons

            self.buttons = Buttons(self.loop, list(self.conf["pin_color_map"]))

        # Prep Display but don't activate it yet. Prep starting screens.
        self.display = Display(self.loop, self.conf)
        self.splash_screen = SplashScreen(self.loop, self.conf, self.display)
        self.main_screen = MainScreen(self.loop, self.conf, self.display)

    def run(self):
        # Activate button-to-keyboard linkage (if we have one)
        try:
            self.buttons.activate()
        except AttributeError:
            pass

        # Activate the display with full layout but no content
        self.display.activate()

        # Switch to splash screen and start the clock
        self.splash_screen.activate()
        self.display.update_clock(self.loop)

        # Do any remaining start up work here
        # ...

        # Switch to main menu after short time
        self.loop.set_alarm_in(1, self.main_screen.activate)

        # Start the reactor
        self.loop.run()

        # Leave an extra line to scroll screen
        print()

    def unhandled_input(self, key):
        # Out-of-band controls
        if key == "esc":  # Exit the program
            raise ExitMainLoop()
        if key == "ctrl l":  # Refresh overwritten/corrupted screen
            self.loop.screen.clear()
            return True

        # TODO: These should be ignored here
        self.display.set_status("Got key %s" % key)
        return True

        self.log.warning("Unhandled input: %s" % key)
