import saturnv


def is_linux():
    print ('check for linux')
    import platform

    if platform.system().lower() == "linux":
        return True
    return False


def is_pi():
    print ('check for pi')
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


if is_pi():
    print("this is a pi - doing import")
    import uinput
    import RPi.GPIO


class Application(object):
    default_conf = {}

    def __init__(self):
        conf = saturnv.AppConf(defaults=Application.default_conf)

    def run(self):
        print("run")

