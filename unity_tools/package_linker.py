import glob
import os

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
        destination = os.path.abspath(destination)

        # utils.fs_link(source, target)
        package_linkspec = self.read_package_linkspec(source)

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
                    content_item_name = os.path.basename(content_item)
                    content_item_target = os.path.abspath(os.path.join(target, content_item_name))
                    utils.fs_link(content_item, content_item_target, hard_link=True, forced=forced)
        else:
            for item in child_packages:
                item_source = os.path.abspath(os.path.join(source, item['source']))
                item_target = os.path.abspath(Template(item['target']).render(**params))

                content = package_linkspec.get('content', None)
                if not content:
                    utils.fs_link(item_source, item_target, hard_link=True, forced=forced)
                else:
                    content_items = [p for item in content for p in
                                     glob.glob(os.path.abspath(os.path.join(item_source, item)))]
                    for content_item in content_items:
                        content_item_name = os.path.basename(content_item)
                        content_item_target = os.path.abspath(os.path.join(item_target, content_item_name))
                        utils.fs_link(content_item, content_item_target, hard_link=True, forced=forced)

        # external packages
        external_packages = package_linkspec.get('external_packages', None)
        if external_packages:
            for item in external_packages:
                item_source = os.path.abspath(Template(item['source']).render(**params))
                item_target = os.path.abspath(os.path.join(source, item['target']))
                utils.fs_link(item_source, item_target, hard_link=True, forced=forced)

                default_content = item.get('default_content', None)
                if default_content:
                    content_items = [
                        p for item in default_content for p in
                        glob.glob(os.path.abspath(os.path.join(source, item)))
                    ]
                    for content_item in content_items:
                        content_item_name = os.path.basename(content_item)
                        content_item_target = os.path.abspath(os.path.join(item_target, content_item_name))
                        if not os.path.exists(content_item_target):
                            utils.copy(content_item, content_item_target)

    def read_package_linkspec(self, source):
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
            transformed_data = {}

            #NOTE: transform to new schema here.
            link = data.get('link', None)
            if not link:
                raise ValueError('Missing <link> root.')

            if '@name' in link:
                transformed_data['name'] = link['@name']

            use_child_package_links = link.get('@useChildPackageLinks', '')
            if use_child_package_links in ['false', 'no', 'False', '']:
                use_child_package_links = False
            else:
                use_child_package_links = True

            if use_child_package_links:
                def _to_child_package(package_link):
                    return {
                        'source': package_link['@package'],
                        'target': '{{__default__}}/%s' % package_link['@package']
                    }

                child_package_links = link.get('childPackageLinks')
                if child_package_links:
                    transformed_data['child_packages'] = [_to_child_package(l) for l in child_package_links['link']]

            external_package_links = link.get('externalPackageLinks', None)
            if external_package_links:
                def _to_external_package(package_link):
                    return {
                        'source': '{{%s}}' % package_link['@package'].strip('ref:'),
                        'target': package_link['@path'],
                    }

                transformed_data['external_packages'] = [_to_external_package(l) for l in external_package_links['link']]

            return transformed_data

