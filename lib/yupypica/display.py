import urwid


class Display (object):
    def __init__(self):

        self.page_title = urwid.Text("initial title", align='left')
        self.top_left = urwid.Padding(self.page_title, left=1)

        self.app_name = urwid.Text('pipyca', align='right')
        self.top_right = urwid.Padding(self.app_name, right=1)

        self.header = urwid.Columns([self.top_left, self.top_right])

        self.main_box = urwid.Filler(urwid.Text("text in MainBox", align='center'))

        self.ver_text = urwid.Text("v0.0", align='left')
        self.bottom_left = urwid.Padding(self.ver_text, left=1)

        self.clock = urwid.Text("clock goes here", align='right')
        self.bottom_right = urwid.Padding(self.clock, right=1)

        self.footer = urwid.Columns([self.bottom_left, self.bottom_right])

        self.frame = urwid.Frame(self.main_box, self.header, self.footer)

    def set_title(self, title):
        self.page_title.set_text(title)


    def start(self):
        loop = urwid.MainLoop(self.frame, unhandled_input=self.exit_on_q())
        loop.run()

    def exit_on_q(key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
