import glob
import os
import shutil

import npath
import xmltodict
from jinja2 import Template

from unity_tools import utils


class PackageLinker(object):
    def __init__(self):
        pass

    def link(self, source=None, destination=None, forced=False, name=None, params={}):
        """
        Link a source folder to a sub-folder in destination folder using given name.
        :param source:
        :param destination:
        :param forced:
        :param name:
        :return:
        """
        source = utils.realpath(source)
        destination = utils.realpath(destination)

        # utils.fs_link(source, target)
        package_linkspec = self._read_package_linkspec(source)

        params['__default__'] = destination

        # package name.
        name = package_linkspec.get('name', name)
        if not name:
            raise ValueError('Missing name for package "%s"'.format(source))

        # target
        target_spec = package_linkspec.get('target', None)
        if not target_spec:
            target = os.path.join(destination, name)
        else:
            target = Template(target_spec).render(**params)
        target = os.path.abspath(target)

        # child packages
        child_packages = package_linkspec.get('child_packages', None)
        if not child_packages:
            content = package_linkspec.get('content', None)
            if not content:
                utils.fs_link(source, target, hard_link=True, forced=forced)
            else:
                content_items = [p for item in content for p in glob.glob(os.path.abspath(os.path.join(source, item)))]
                for content_item in content_items:
                    name = ntpath.basename(content_item)
                    item_target = os.path.abspath(os.join(target, name))
                    utils.fs_link(content_item, item_target)
        else:
            for item in child_packages:
                item_source = os.path.abspath(os.path.join(source, item['source']))
                item_target = os.path.abspath(Template(item['target']).render(**params))
                utils.fs_link(item_source, item_target, hard_link=True, forced=forced)

    def _link_one_package(self, name=None, source=None, destination=None, info={}, params={}, forced=False):
        skipped = info.pop('skipped', False)
        name = info.pop('name', name)
        # source =

    def _read_package_linkspec(self, source):
        """
        Reads the linkspec if exist in given source folder.
        :param source: the folder containing linkspec file
        :return: a linkspec dictionary or empty dictionary.
        """
        linkspec = self._read_linkspec_yaml_file(source)
        linkspec = self._read_package_linkspec_file(source) if not linkspec else linkspec
        linkspec = {} if not linkspec else linkspec
        return linkspec

    def _read_linkspec_yaml_file(self, source):
        import yaml

        file = os.path.join(source, 'linkspec.yaml')
        if not os.path.isfile(file):
            file = os.path.join(source, 'linkspec.yml')
            if not os.path.isfile(file):
                return None

        with open(file, 'r') as fh:
            content = fh.read()
            return yaml.load(content)

    def _read_package_linkspec_file(self, source):
        file = os.path.join(source, 'package.linkspec')
        if not os.path.isfile(file):
            return None

        with open(file, 'r') as fh:
            content = fh.read()
            data = xmltodict.parse(content)

            #NOTE: transform to new schema here.
            return data

