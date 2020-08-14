import urwid

class ScreenMain(object):
    def __init__(self):
        self.title = urwid.CENTER(urwid.Text('Main'))
        self.meun = urwid.
    self.version = urwid.Padding(urwid.Text('v0.0', align='right'), right=1)
    self.header = urwid.AttrMap(urwid.Columns([self.app_name, self.version]), 'header')

    choices = u'Chapman Cleese Gilliam Idle Jones Palin'.split()

    def menu(title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

