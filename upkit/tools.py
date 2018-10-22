import argparse
import os
import shutil
import sys
import traceback

from jinja2 import Environment, PackageLoader, select_autoescape, Template

from upkit import utils


class LinkPackageCommand(object):
    help = 'Link packages with given configs'

    def build_argument_parser(self, parser):
        parser.add_argument('-c', '--config', dest='config',
                            help='Path to link configuration file (config.yaml)')

        parser.add_argument('-p', dest='params', action='append',
                            help='Parameters.')

    def run(self, args):
        from upkit.package_linker import PackageLinker

        try:
            params = dict((k, v) for (k, v) in [i.split('=') for i in utils.guaranteed_list(args.params)])

            if args.config:
                args.confg = os.path.abspath(args.config)

            linker = PackageLinker(config_file=args.config, params=params)
            linker.run()
            print('Package link completed.')
        except:
            print('Package link failed with errors.')
            print(traceback.format_exc())
            sys.exit(1)


class CreatePackageCommand(object):
    help = 'Create a package.'

    def __init__(self):
        self.data_folder = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data'))
        self.env = Environment(
            loader=PackageLoader('upkit', 'data/create-package'),
            autoescape=select_autoescape(['html', 'xml', 'nuspec'])
        )

    def build_argument_parser(self, parser):
        parser.add_argument('location', help='Package location')

    def run(self, args):
        try:
            os.mkdir(args.location)
            os.mkdir(os.path.join(args.location, 'assets'))
            os.mkdir(os.path.join(args.location, 'plugins'))
            os.mkdir(os.path.join(args.location, 'settings'))
            os.mkdir(os.path.join(args.location, 'project'))

            # package_config_template_file = os.path.join(self.data_folder, 'create-package', 'package-config.yaml')
            if True:
                template = self.env.get_template('package-config.yaml.j2')
                file_path = os.path.join(args.location, 'package-config.yaml')
                with open(file_path, 'w') as writer:
                    data = template.render()
                    writer.write(data.encode('utf-8'))

            if True:
                template = self.env.get_template('linkspec.yaml.j2')
                file_path = os.path.join(args.location, 'linkspec.yaml')
                with open(file_path, 'w') as writer:
                    data = template.render()
                    writer.write(data.encode('utf-8'))

            if True:
                template = self.env.get_template('git-ignore.j2')
                file_path = os.path.join(args.location, '.gitignore')
                with open(file_path, 'w') as writer:
                    data = template.render()
                    writer.write(data.encode('utf-8'))

            if True:
                template = self.env.get_template('package.nuspec.j2')
                file_path = os.path.join(args.location, 'package.nuspec')
                with open(file_path, 'w') as writer:
                    data = template.render()
                    writer.write(data.encode('utf-8'))

            print('Package created.')
        except:
            print('Creating package failed with errors.')
            print(traceback.format_exc())
            sys.exit(1)


class UnityTools(object):
    def __init__(self):
        self._commands = {
            'link': LinkPackageCommand(),
            'create-package': CreatePackageCommand(),
        }

    def run(self):
        self._parse_args()

    def _parse_args(self):

        from . import __version__

        parser = argparse.ArgumentParser(description='Unity3D project utilities.')
        parser.add_argument('-v', '--version', action='version', version='Unity tools %s' % __version__)
        subparsers = parser.add_subparsers(help='Tool command to execute')

        for k, v in self._commands.items():
            command_parser = subparsers.add_parser(k, help=v.help)
            v.build_argument_parser(command_parser)
            command_parser.set_defaults(func=v.run)

        args = parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()


def execute_from_command_line():
    tools = UnityTools()
    tools.run()


if __name__ == "__main__":
    execute_from_command_line()


