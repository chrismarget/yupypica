import os
import saturnv

from .gpio_kb import keyboard


def is_linux():
    import platform

    if platform.system().lower() == "linux":
        return True
    return False


def is_pi():
    if is_linux():
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    k, v = line.strip().split(":", 1)
                    if k.strip().lower() == "model" & "raspberry pi" in v.lower():
                        return True
        except:
            pass
        return False

class Application(object):
    default_conf = {}
    conf = saturnv.AppConf(defaults=Application.default_conf)

    def __init__(self):
        print("application init")
        if is_pi():
            if os.fork(): # child
                print ("child starts keyboard")
                keyboard()
            else:
                print ("parent continues normally")

    def run(self):
        print("run")

