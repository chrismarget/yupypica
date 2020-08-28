def string_on_string_at_idx_with_transparency(under: str, over: str, transparent="", idx=0) -> str:
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


def overlay(under: str, over: str, transparent="", idx=0) -> str:
    """Overlays one string onto another, accounting for overhang at either end.
    With idx = 10 -> "......A"

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
        the index of the position in the combined strings length where the
        overlay string begins. Defaults to 0. Sensible values are:
            range(len(under) + len(over) - 1)

    Example
    -------
    over = "ABCDE"
    under = "......."
    transparent = "C"

    With idx = 0  -> "E......"
    With idx = 1  -> "DE....."
    With idx = 2  -> ".DE...."
    With idx = 3  -> "B.DE..."
    With idx = 4  -> "AB.DE.."
    With idx = 5  -> ".AB.DE."
    With idx = 6  -> "..AB.DE"
    With idx = 7  -> "...AB.D"
    With idx = 8  -> "....AB."
    With idx = 9  -> ".....AB"
    With idx = 10 -> "......A"
    """

    idx2 = max(0, idx-len(over) + 1)
    over = get_overlay_substring(under, over, idx)
    return string_on_string_at_idx_with_transparency(under, over, transparent, idx2)

def overlay_multiline(under: [], over:[], transparent="", idx=0, skiplines=0) -> []:
    """multiline version of overlay()

    Parameters
    ----------
    under: []
        A list of underlay strings
    over: []
        A list of overlay strings
    idx: int, optional
        offset, same as in overlay()
    skiplines:
        vertical offset, shift overlay down by this many lines

    Example
    -------
    u = [ "1__________",
          "2__________",
          "3__________",
          "4__________",
          "5__________" ]
    o = [ "A   ",
          " B  ",
          "  C ",
          "   D" ]
    t = " "
    skiplines = 1
    idx = 9

    result = [ "1__________",
               "2_____A____",
               "3______B___",
               "4_______C__",
               "5________D_" ]
    """

    out = []

    # copy skiplines from underlay without overlay
    for i in range(min(skiplines, len(under))):
        out.append(under[i])

    # copy overlaid lines to output
    for i in range(skiplines, min(len(under), skiplines + len(over))):
        out.append(overlay(under[i], over[i - skiplines], transparent, idx))

    # copy remaining underlay lines to output without overlay
    for i in range(min(len(under), skiplines + len(over)), len(under)):
        out.append(under[i])

    return out
