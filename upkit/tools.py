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
        parser.add_argument(dest='config', default='upkit.yaml', nargs='?',
                            help='Path to link configuration file (config.yaml)')

        parser.add_argument('-w', '--package-folder', dest='package_folder', default=None,
                            help='Path to a folder where dependency packages will be resolved to.')

        parser.add_argument('-p', dest='params', action='append',
                            help='Parameters.')

    def run(self, args):
        from upkit.package_linker import PackageLinker, UnityProjectLinkTemplate

        try:
            params = dict((k, v) for (k, v) in [i.split('=') for i in utils.guaranteed_list(args.params)])

            if not args.package_folder:
                args.package_folder = os.path.join(os.path.dirname(args.config), '.packages')

            link_template = UnityProjectLinkTemplate()

            linker = PackageLinker(config_file=args.config, package_folder=args.package_folder,
                                   link_template=link_template, params=params)
            linker.run()
            print('Package link completed.')
        except:
            print('Package link failed with errors.')
            print(traceback.format_exc())
            sys.exit(1)


class CreatePackageCommand(object):
    help = 'Create a package.'

    def __init__(self):
        # self.data_folder = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data'))
        self.env = Environment(
            loader=PackageLoader('upkit', 'data/create-package'),
            autoescape=select_autoescape(['html', 'xml', 'nuspec'])
        )

    def build_argument_parser(self, parser):
        parser.add_argument('location', help='Package location')
        parser.add_argument('--link', action='store_const', const=True,
                            help='Link and create package Unity project after created')

    def run(self, args):
        try:
            if os.path.exists(args.location):
                if os.path.isfile(args.location) or os.listdir(args.location):
                    raise RuntimeError('"%s" must be an empty folder.' % args.location)
            else:
                os.mkdir(args.location)

            os.mkdir(os.path.join(args.location, 'assets'))
            os.mkdir(os.path.join(args.location, 'plugins'))
            os.mkdir(os.path.join(args.location, 'settings'))
            os.mkdir(os.path.join(args.location, 'packages'))
            os.mkdir(os.path.join(args.location, 'project'))

            # package_config_template_file = os.path.join(self.data_folder, 'create-package', 'package-config.yaml')
            if True:
                template = self.env.get_template('upkit.yaml.j2')
                file_path = os.path.join(args.location, 'upkit.yaml')
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

            if hasattr(args, 'link') and args.link:
                from upkit.package_linker import PackageLinker
                linker = PackageLinker(config_file=os.path.abspath(os.path.join(args.location, 'upkit.yaml')))
                linker.run()
                print('Package link completed.')

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


