import platform

def is_linux():
    return platform.system() == "Linux"

def is_pi():
    if not is_linux():
        return False

    return "Raspberry Pi" in open('/proc/cpuinfo').read()

