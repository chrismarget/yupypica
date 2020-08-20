import urwid

def Welcome():
    return urwid.AttrMap(
        urwid.Pile([
            urwid.Text("                              o            ", align='center'),
            urwid.Text(",   . .   . ,---. ,   . ,---. . ,---. ,---.", align='center'),
            urwid.Text("|   | |   | |   | |   | |   | | |     ,---|", align='center'),
            urwid.Text("`---| `---' |---' `---| |---' ` `---' `---^", align='center'),
            urwid.Text("`---'       |     `---' |                  ", align='center'),
            urwid.Text("", align='center'),
            urwid.Text("Stand-alone Certificate Authority", align='center'),
            urwid.Text("v 1.0.7", align='center'),
        ]),
    'logo')
