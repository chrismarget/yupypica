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
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if line.strip():
                        k, v = line.split(":", 1)
                        if k.strip().lower() == "model" and "raspberry pi" in v.lower():
                            return True
        except:
            pass
    return False

class Application(object):
    default_conf = {}

    def __init__(self):
        conf = saturnv.AppConf(defaults=Application.default_conf)

        print("Application init")
        if is_pi():
            print("this is a pi")
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
        else:
            print("this is not a pi")

    def run(self):
        print("run")

