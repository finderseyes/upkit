import argparse
import sys
import traceback

from unity_tools import utils


class LinkCommand(object):
    def build_argument_parser(self, parser):
        parser.add_argument('-c', '--config', dest='config',
                            help='Path to link configuration file (config.yaml)')

        parser.add_argument('--packages-config', dest='packages_config',
                            help='Path to Nuget packages.config file')
        parser.add_argument('--packages-folder', dest='packages_folder',
                            help='Path to folder containg Nuget packages')

        parser.add_argument('--params-config', dest='params_config',
                            help='Path to link parameter file (params.yml)')

        parser.add_argument('-d', '--destination', dest='destination', required=True,
                            help='Path to destination folder containing target links.')

        parser.add_argument('-p', '--parameter', dest='params', action='append',
                            help='Parameters.')

        # parser.add_argument('-p', '--package-dir', dest='packageDir', required=True,
        #                     help='Path to the directory where Nuget packages are installed')
        # parser.add_argument('-l', '--link-dir', dest='linkDir', required=True,
        #                     help='Path to the directory where links to Nuget packages are created')
        # parser.add_argument('-r', '--params', dest='params', required=False, help='Path to XML parameter file')

    def run(self, args):
        from unity_tools.package_linker import PackageLinker

        try:
            params = dict((k, v) for (k, v) in [i.split('=') for i in utils.guaranteed_list(args.params)])

            linker = PackageLinker(
                config=args.config,
                packages_config=args.packages_config,
                packages_folder=args.packages_folder,
                params_config=args.params_config,
                destination=args.destination,
                params=params
            )
            linker.run()
            print('Package link completed.')
        except:
            print('Package link failed with errors.')
            print(traceback.format_exc())
            sys.exit(1)


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
            command_parser.set_defaults(func=lambda a: v.run(a))

        args = parser.parse_args()
        args.func(args)

