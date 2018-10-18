import glob
import os
import yaml
import xmltodict
from jinja2 import Template, Environment, meta

from unity_tools import utils


class PackageLinker(object):
    def __init__(self, config=None,
                 packages_config=None,
                 packages_folder=None,
                 params_config=None,
                 destination=None,
                 params={}):
        """

        :param config: the config file, will override packages_config and params_config
        :param packages_config: Nuget packages.config file
        :param params_config: yaml file containing parameter definitions
        :param destination: the default link destination folder
        :param params: command-line parameters.
        """
        if not destination:
            raise ValueError('Missing required parameter "destination"')

        destination = os.path.abspath(destination)

        self._jinja_environment = Environment()
        self._destination = destination
        self._params = {
            '__default__': destination,
            '__cwd__': os.path.abspath(os.getcwd()),
        }

        if config:
            self._params['__dir__'] = os.path.abspath(os.path.dirname(config))

            with open(config, 'r') as fh:
                content = fh.read()

                config_data = yaml.load(content)

                # parameters
                params_data = config_data.get('params', {})
                self._expand_params(params_data)

                # override params
                self._params.update(params)

                # links
                links_data = config_data.get('links', {})

                def _to_link(i, dest):
                    name = i.get('name')
                    source = os.path.abspath(self._render_template(i.get('source'), self._params))
                    destination_spec = i.get('destination', dest)
                    dest = os.path.abspath(self._render_template(destination_spec, self._params))

                    return {
                        'name': name,
                        'source': source,
                        'destination': dest
                    }

                self._links = [_to_link(item, destination) for item in links_data]
        else:
            if params_config:
                self._params['__dir__'] = os.path.abspath(os.path.dirname(params_config))
                with open(params_config, 'r') as fh:
                    content = fh.read()
                    params_data = yaml.load(content)
                    self._expand_params(params_data)

            # override params
            self._params.update(params)

            # packages
            if packages_config:
                if not packages_folder:
                    raise ValueError('Missing parameter "packages_folder".')

                self._params['__dir__'] = os.path.abspath(os.path.dirname(packages_config))
                with open(packages_config, 'r') as fh:
                    content = fh.read()
                    packages_data = xmltodict.parse(content)

                    def _to_link(i, pkg_folder, dest):
                        name = '%s%s' % (i.get('@id'), i.get('@version'))
                        source = os.path.abspath(os.path.join(pkg_folder, name, 'content'))

                        return {
                            'name': name,
                            'source': source,
                            'destination': dest
                        }

                    self._links = [_to_link(item, packages_folder, os.path.abspath(destination))
                                   for item in utils.guaranteed_list(packages_data['packages']['package'])]

    def _expand_params(self, params_data):
        for k, item in params_data.items():
            self._params[k] = os.path.abspath(self._render_template(item, self._params))

    def _render_template(self, template, params={}):
        ast = self._jinja_environment.parse(template)
        variables = meta.find_undeclared_variables(ast)
        for v in variables:
            if v not in params:
                raise ValueError('Unknown parameter "%s"' % v)
        return Template(template).render(**params)

    def run(self):
        for link in self._links:
            self.link(source=link['source'], destination=link['destination'], name=link['name'], forced=True,
                      params=self._params)

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
            target = self._render_template(target_spec, params)
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
                item_target = os.path.abspath(self._render_template(item['target'], params))

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
                item_source = os.path.abspath(self._render_template(item['source'], params))
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
                    transformed_data['child_packages'] = [
                        _to_child_package(l) for l in utils.guaranteed_list(child_package_links['link'])]

            external_package_links = link.get('externalPackageLinks', None)
            if external_package_links:
                def _to_external_package(package_link):
                    return {
                        'source': '{{%s}}' % package_link['@package'].replace('ref:', '').replace('.', '_'),
                        'target': package_link['@path'],
                    }

                transformed_data['external_packages'] = [
                    _to_external_package(l) for l in utils.guaranteed_list(external_package_links['link'])]

            return transformed_data

