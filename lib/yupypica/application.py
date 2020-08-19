import os
import platform
import saturnv

from .gpio_kb import keyboard


def is_linux():
    return platform.system() == "Linux"

def is_pi():
    if not is_linux():
        return False

    return "Raspberry Pi" in open('/proc/cpuinfo').read()


class Application(object):
    default_conf = {}

    def __init__(self):
        conf = saturnv.AppConf(defaults=Application.default_conf)

        print("Application init")
        if not is_pi():
            print("This isn't a Raspberry Pi")

        # TODO: Use subprocess module for this instead
        if os.fork(): # child
            c = open("/tmp/child", "a")
            c.write("child")
            c.close()
            print("child starts keyboard")
            keyboard()
        else:
            p = open("/tmp/parent", "a")
            p.write("parent")
            p.close()
            print("parent continues normally")

    def run(self):
        print("run")

