
import argparse
import sys
from os.path import basename


class ShowDefaultsAction(argparse.Action):
    def __init__(self, option_strings, dest, help=None, **kwargs):
        argparse.Action.__init__(self, option_strings, dest, nargs=0,
                                 help=help)
        self.app = kwargs['app']

    def __call__(self, parser, namespace, values, option_string=None):
        self.app.show_configuration()
        sys.exit()


class Options(object):
    """Command-line options

    Handles building of command-line parser using argparse, including
    uage info. Parses arguments and stores the results.
    """
    def __init__(self, app):
        """Initializer

        Ready the command-line parser and parse the arguments.
        """
        self.app = app
        self.build_parser()
        self.args = self.parser.parse_args()

    def build_parser(self):
        """Build the command line parser

        Construct the command-line parser and usage info.
        """
        self.parser = argparse.ArgumentParser(
            prog=basename(sys.argv[0]),
            description='Stand-alone Certificate Authority',
        )

#        self.parser.add_argument('-c', '--config',
#                                 help='specify a configuration file',
#                                 dest='conf_file')
#
#        self.parser.add_argument('-g', '--loglevel',
#                                 help='log level',
#                                 choices=['error', 'warning', 'info', 'debug'],
#                                 dest='log_level')
#
#        self.parser.add_argument('--show-defaults',
#                                 help='print built-in application defaults',
#                                 action=ShowDefaultsAction, app=self.app)


    def get_args(self):
        """Get parsed command-line arguments

        Returns:
            command line arguments as argparse namespace
        """
        return self.args
