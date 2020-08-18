import urwid

def Lines(count=0, selected=-1):
    lines = []
    for i in range(count):
        if i == selected:
            lines.append(
                urwid.Text((i, ">button<"), align='center')
            )
        else:
            lines.append(
                urwid.Text((i, "button"), align='center')
            )

    return urwid.Pile(lines)

