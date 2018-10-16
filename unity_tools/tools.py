import argparse
import sys


class LinkCommand(object):
    def build_argument_parser(self, parser):
        parser.add_argument('-c', '--config', dest='config', required=True,
                            help='Path to the Nuget package .config file')
        parser.add_argument('-p', '--package-dir', dest='packageDir', required=True,
                            help='Path to the directory where Nuget packages are installed')
        parser.add_argument('-l', '--link-dir', dest='linkDir', required=True,
                            help='Path to the directory where links to Nuget packages are created')
        parser.add_argument('-r', '--params', dest='params', required=False, help='Path to XML parameter file')

    def run(self):
        pass


class UnityTools(object):
    def __init__(self):
        self._commands = {
            'link': LinkCommand(),
        }

    def run(self):
        self._parse_args()

    def _parse_args(self):
        parser = argparse.ArgumentParser(description='Unity3D project utilities.')
        subparsers = parser.add_subparsers(help='sub-command help')

        for k, v in self._commands.items():
            command_parser = subparsers.add_parser(k, help='Help for command %s'.format(k))
            v.build_argument_parser(command_parser)

        parser.parse_args()

        command = self._commands[parser.command]
        k = 10

