import glob
import copy
import os
import yaml
import yamlordereddictloader
import xmltodict
from jinja2 import Template, Environment, meta, TemplateSyntaxError

from upkit import utils


class PackageLinker(object):
    def __init__(self, config=None,
                 params={},
                 # packages_config=None,
                 # packages_folder=None,
                 # params_config=None,
                 ):
        """

        :param config: the config file, will override packages_config and params_config
        :param packages_config: Nuget packages.config file
        :param params_config: yaml file containing parameter definitions
        :param destination: the default link destination folder
        :param params: command-line parameters.
        """

        self._jinja_environment = Environment()
        self._params = {
            '__cwd__': os.path.abspath(os.getcwd()),
        }

        if config:
            with open(config, 'r') as fh:
                content = fh.read()

                config_data = yaml.load(content, Loader=yamlordereddictloader.Loader)

                # parameters
                params_data = config_data.get('params', {})
                params.update({
                    '__cwd__': os.path.abspath(os.getcwd()),
                    '__dir__': os.path.abspath(os.path.dirname(config)),
                })

                self._params = copy.deepcopy(params)
                self._expand_params(params_data, exclude=params)

                # links
                links_data = config_data.get('links', {})

                def _to_link(i):
                    source = os.path.abspath(self._render_template(i.get('source'), self._params))
                    target_spec = i.get('target', None)
                    target = os.path.abspath(self._render_template(target_spec, self._params)) if target_spec else None
                    package_linkspec = i.get('linkspec', None)

                    return {
                        'source': source,
                        'target': target,
                        'linkspec': package_linkspec,
                    }

                self._links = [_to_link(item) for item in links_data]
        else:
            self._links = []
            # if params_config:
            #     self._params['__dir__'] = os.path.abspath(os.path.dirname(params_config))
            #     with open(params_config, 'r') as fh:
            #         content = fh.read()
            #         params_data = yaml.load(content, Loader=yamlordereddictloader.Loader)
            #         self._expand_params(params_data)
            #
            # # override params
            # self._params.update(params)
            #
            # # packages
            # if packages_config:
            #     if not packages_folder:
            #         raise ValueError('Missing parameter "packages_folder".')
            #
            #     self._params['__dir__'] = os.path.abspath(os.path.dirname(packages_config))
            #     with open(packages_config, 'r') as fh:
            #         content = fh.read()
            #         packages_data = xmltodict.parse(content)
            #
            #         def _to_link(i, pkg_folder, dest):
            #             name = '%s.%s' % (i.get('@id'), i.get('@version'))
            #             source = os.path.abspath(os.path.join(pkg_folder, name, 'content'))
            #
            #             return {
            #                 'name': name,
            #                 'source': source,
            #                 'destination': dest,
            #                 'linkspec': None,
            #             }
            #
            #         self._links = [_to_link(item, packages_folder, os.path.abspath(destination))
            #                        for item in utils.guaranteed_list(packages_data['packages']['package'])]

    def _expand_params(self, params_data, exclude={}):
        for k, item in params_data.items():
            if k not in exclude:
                self._params[k] = self._render_template(item, self._params)

    def _render_template(self, template, params={}):
        try:
            ast = self._jinja_environment.parse(template)
            variables = meta.find_undeclared_variables(ast)
            for v in variables:
                if v not in params:
                    raise ValueError('Unknown parameter "%s"' % v)
            return Template(template).render(**params)
        except TypeError as err:
            raise ValueError('Syntax error at "%s", error: %s' % (template, str(err)))
        except TemplateSyntaxError as err:
            raise ValueError('Syntax error at "%s", error: %s' % (template, str(err)))

    def run(self):
        for link in self._links:
            self.link(source=link['source'],
                      target=link['target'],
                      package_linkspec=link['linkspec'],
                      forced=True,
                      set_dir=('__dir__' in self._params),
                      params=self._params)

    def link(self, source=None, target=None, forced=False, package_linkspec=None, set_dir=True, params={}):
        """
        Link a source folder to a sub-folder in destination folder using given name.
        :param source:
        :param target:
        :param forced:
        :param package_linkspec:
        :param set_dir:
        :param params:
        :return:
        """
        if not source:
            raise ValueError('Missing required "source" parameter.')

        source = utils.realpath(source)

        # utils.fs_link(source, target)
        if not package_linkspec:
            package_linkspec = self.read_package_linkspec(source)

        # make a copy of the dict
        params = copy.deepcopy(params)
        if source:
            params['__source__'] = source
            if set_dir:
                params['__dir__'] = source

        if target:
            target = os.path.abspath(target)
            params['__target__'] = target

        # child packages
        child_packages = package_linkspec.get('links', None)
        if not child_packages:
            if not target:
                raise ValueError('Missing parameter "target" but no links can be found in the linkspec.')

            content = package_linkspec.get('content', None)
            if not content:
                utils.fs_link(source, target, hard_link=True, forced=forced)
            else:
                content_items = [
                    p for item in content
                    for p in glob.glob(os.path.abspath(self._render_template(item, params)))
                ]
                for content_item in content_items:
                    content_item_name = os.path.basename(content_item)
                    content_item_target = os.path.abspath(os.path.join(target, content_item_name))
                    utils.fs_link(content_item, content_item_target, hard_link=True, forced=forced)
        else:
            for item in child_packages:
                item_target = os.path.abspath(self._render_template(item['target'], params))

                content = item.get('content', None)

                # content will overwrite the source
                if not content:
                    item_source = os.path.abspath(self._render_template(item['source'], params))
                    utils.fs_link(item_source, item_target, hard_link=True, forced=forced)
                else:
                    content_items = [p for item in content for p in
                                     glob.glob(os.path.abspath(self._render_template(item, params)))]
                    for content_item in content_items:
                        content_item_name = os.path.basename(content_item)
                        content_item_target = os.path.abspath(os.path.join(item_target, content_item_name))
                        utils.fs_link(content_item, content_item_target, hard_link=True, forced=forced)

        # external packages
        external_packages = package_linkspec.get('external_links', None)
        if external_packages:
            for item in external_packages:
                item_source = os.path.abspath(self._render_template(item['source'], params))
                item_target = os.path.abspath(self._render_template(item['target'], params))
                utils.fs_link(item_source, item_target, hard_link=True, forced=forced)

                default_content = item.get('default_content', None)
                if default_content:
                    content_items = [
                        p for item in default_content for p in
                        glob.glob(os.path.abspath(self._render_template(item, params)))
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
            return yaml.load(content, Loader=yamlordereddictloader.Loader)

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

