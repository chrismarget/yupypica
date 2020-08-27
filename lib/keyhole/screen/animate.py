def string_on_string_at_pos_with_transparency(under: str, over: str, transparent="", idx=0) -> str:
    """Overlays one string onto another at a given position.
    Helper function to overlay().

    Parameters
    ----------
    under: str
        The underlay string
    over: str
        The overlay string
    transparent: str, optional
        A set of transparent characters in the overlay string. These characters
        in the overlay do not print, rather the underlay string is visible
        "through" these characters wherever they appear. Defaults to empty set.
    idx: int, optional
        The index of the first position in the underlay string to replace with the
        overlay string. Defaults to 0.
    """

    result = list(under)
    for i in range(len(under)):
        if idx <= i < (idx + len(over)):
            if over[i - idx] not in transparent:
                result[i] = over[i - idx]
    return "".join(result)


def get_overlay_substring(under: str, over: str, idx=0) -> str:
    """Given an overlay string, an underlay string, and an offset, returns the
    overlay substring after trimming off "overhanging" characters from either
    the left or right.

    Parameters
    ----------
    under: str
        The underlay string
    over: str
        The overlay string
    idx: int, optional
        the index of the position in the combined strings length where the
        overlay string begins. Defaults to 0.
     """
    idx += 1
    if idx < len(over):
        over = over[-idx:]
        if len(over) > len(under):
            over = over[:len(under)]
    elif idx > len(under):
        over = over[:(len(under) - idx)]

    return over


def overlay(under: str, over: str, transparent="", pos=0) -> str:
    pos2 = max(0, pos-len(over))
    over = get_overlay_substring(under, over, pos)
    return string_on_string_at_pos_with_transparency(under, over, transparent, pos2)
