import urwid

def Lines(selected=-1):
    lines = []
    for i in range(4):
        if i == selected:
            lines.append(
                urwid.Text((i, ">button<"), align='center')
            )
        else:
            lines.append(
                urwid.Text((i, "button"), align='center')
            )

    # lines = [
    #     urwid.Text((0, "button"), align='center'),
    #     urwid.Text((1, "button"), align='center'),
    #     urwid.Text((2, "button"), align='center'),
    #     urwid.Text((3, "button"), align='center'),
    # ]
    return urwid.Pile(lines)

