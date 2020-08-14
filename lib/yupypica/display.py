import urwid

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

class Display (object):
    def __init__(self):

        self.page_title = urwid.Text("initial title")
        self.top_left = urwid.Padding(self.page_title, left=1)
        self.top_right = urwid.Padding(urwid.Text('pipyca'), right=1)
        self.header = urwid.Columns([self.top_left, self.top_right])

        self.page = urwid.Frame(urwid.Text("this is frame"))

        self.bottom_left = urwid.Padding(urwid.Text('v0.0'), left=1)
        self.bottom_right = urwid.Padding(urwid.Text('clock goes here'), right=1)
        self.footer = urwid.Columns([self.bottom_left, self.bottom_right])

        self.whole_screen = urwid.Pile([self.header,self.page,self.footer])

    def set_title(self, title):
        self.page_title.set_text(title)


    def start(self):
        # txt = urwid.Text(u"Hello World")
        # fill = urwid.Filler(txt, 'top')
        # loop = urwid.MainLoop(fill)
        # loop.run()

        loop = urwid.MainLoop(self.whole_screen, unhandled_input=exit_on_q)
        loop.run()

