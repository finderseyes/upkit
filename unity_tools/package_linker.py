import os
import shutil
import xmltodict

from unity_tools import utils


class PackageLinker(object):
    def __init__(self):
        pass

    def link(self, name=None, source=None, destination=None, params={}, forced=False, ):
        source = utils.realpath(source)
        destination = utils.realpath(destination)
        target = os.path.join(destination, name)

        if not forced and os.path.exists(target):
            raise RuntimeError('Path "%s" exists.'.format(target))

        utils.fs_link(source, target)
        linkspec = self._read_linkspec(source)

    def _link_one_package(self, name=None, source=None, destination=None, info={}, params={}, forced=False):
        skipped = info.pop('skipped', False)
        name = info.pop('name', name)
        source =

    def _read_linkspec(self, source):
        linkspec = self._read_linkspec_yaml(source)
        linkspec = self._read_package_linkspec(source) if not linkspec else linkspec
        linkspec = {} if not linkspec else linkspec

        p = 10

    def _read_linkspec_yaml(self, source):
        import yaml

        file = os.path.join(source, 'linkspec.yaml')
        if not os.path.isfile(file):
            file = os.path.join(source, 'linkspec.yml')
            if not os.path.isfile(file):
                return None

        with open(file, 'r') as fh:
            content = fh.read()
            return yaml.load(content)

    def _read_package_linkspec(self, source):
        file = os.path.join(source, 'package.linkspec')
        if not os.path.isfile(file):
            return None

        with open(file, 'r') as fh:
            content = fh.read()
            data = xmltodict.parse(content)

            #NOTE: transform to new schema here.
            return data

