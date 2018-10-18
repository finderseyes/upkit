import os
import unittest

import yaml

from unity_tools.package_linker import PackageLinker


class PackageLinkerTestCase(unittest.TestCase):
    def setUp(self):
        self._linker = PackageLinker(destination='../../temp',)

    def test_link_without_linkspec(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.0/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-a/data.txt'))

    def test_link_with_empty_linkspec(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.1/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-a/data.txt'))

    def test_link_with_name_in_linkspec(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.2/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-abc/data.txt'))

    def test_link_with_target_in_linkspec(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.3/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-abcdef/data.txt'))

    def test_link_with_child_packages_in_linkspec(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.4/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-a-child0/data.txt'))
        self.assertTrue(os.path.isfile('../../temp/a/b/lib-a-child1/data.txt'))

    def test_link_with_content_selection_in_linkspec(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.5/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-a-selective/data0.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-selective/data1.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-selective/data2.txt'))
        self.assertFalse(os.path.isfile('../../temp/lib-a-selective/data.txt'))

    def test_link_with_content_selection_in_sub_packages_in_linkspec(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.6/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-a-child-content/data0.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-child-content/data1.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-child-content/data2.txt'))
        self.assertFalse(os.path.isfile('../../temp/lib-a-child-content/data.txt'))

    def test_link_with_external_packages_in_linkspec(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.7/content',
                          destination='../../temp',
                          forced=True,
                          params=dict(resources_package='../../tests/resources'))

        self.assertTrue(os.path.isfile('../../temp/lib-a-with-external-packages/data.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-with-external-packages/resources/data.txt'))

    def test_link_with_external_packages_default_content_in_linkspec(self):
        import os

        if os.path.exists('../../tests/empty_resources/default-data.txt'):
            os.remove('../../tests/empty_resources/default-data.txt')

        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.8/content',
                          destination='../../temp',
                          forced=True,
                          params=dict(resources_package='../../tests/empty_resources'))

        self.assertTrue(os.path.isfile('../../temp/lib-a-external-child/data.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-external-child/resources/default-data.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-external-child/resources/a/data.txt'))

    def test_overwrite_linkspec(self):
        import os

        content = """
child_packages:
- source: aaa
  target: '{{__default__}}/lib-a-external-aaa'
external_packages:
- source: '{{resources_package}}'
  target: aaa/resources
  default_content: ['_resources/*']
"""
        package_linkspec = yaml.load(content)

        if os.path.exists('../../tests/empty_resources/default-data.txt'):
            os.remove('../../tests/empty_resources/default-data.txt')

        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.8/content',
                          destination='../../temp',
                          forced=True,
                          package_linkspec=package_linkspec,
                          params=dict(resources_package='../../tests/empty_resources'))

        self.assertTrue(os.path.isfile('../../temp/lib-a-external-aaa/data.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-external-aaa/resources/default-data.txt'))
        self.assertTrue(os.path.isfile('../../temp/lib-a-external-aaa/resources/a/data.txt'))

    def test_load_package_linkspec_file(self):
        package_linkspec = self._linker.read_package_linkspec(source='../../tests/lib-b1.0.0/content')

        self.assertEqual({
            'name': 'a-package-name',
            'child_packages': [
                {'source': 'aaa', 'target': '{{__default__}}/aaa'},
                {'source': 'bbb', 'target': '{{__default__}}/bbb'},
            ],
            'external_packages': [
                {'source': '{{var_a}}', 'target': 'aaa/Resources'},
                {'source': '{{var_b}}', 'target': 'bbb/Resources'},
                {'source': '{{c_d_e}}', 'target': 'ccc/Resources'},
            ],
        }, package_linkspec)

    def test_load_package_linkspec_file_not_using_child_packages(self):
        package_linkspec = self._linker.read_package_linkspec(source='../../tests/lib-b1.0.1/content')

        self.assertEqual({
            'name': 'a-package-name',
            'external_packages': [
                {'source': '{{var_a}}', 'target': 'aaa/Resources'},
                {'source': '{{var_b}}', 'target': 'bbb/Resources'},
                {'source': '{{c_d_e}}', 'target': 'ccc/Resources'},
            ],
        }, package_linkspec)

    def test_run_from_config(self):
        linker = PackageLinker(config='../../tests/config.yaml', destination='../../temp/from-config')
        linker.run()

        self.assertTrue(os.path.isfile('../../temp/from-config/lib-a-external-child/data.txt'))
        self.assertTrue(os.path.isfile('../../temp/from-config/lib-a-external-child/resources/default-data.txt'))
        self.assertTrue(os.path.isfile('../../temp/from-config/lib-a-external-child/resources/a/data.txt'))

    def test_run_from_packages_config(self):
        linker = PackageLinker(
            packages_config='../../tests/packages.config',
            packages_folder='../../tests',
            destination='../../temp/from-packages-config',
            params=dict(resources_package='../../tests/empty_resources')
        )
        linker.run()

        self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/data.txt'))
        self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/resources/default-data.txt'))
        self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/resources/a/data.txt'))

    def test_run_from_packages_config_and_params_config(self):
        linker = PackageLinker(
            packages_config='../../tests/packages.config',
            packages_folder='../../tests',
            destination='../../temp/from-packages-config',
            params_config='../../tests/params.yaml',
        )
        linker.run()

        self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/data.txt'))
        self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/resources/default-data.txt'))
        self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/resources/a/data.txt'))

    # def test_not_run_if_missing_parameters(self):
    #     linker = PackageLinker(
    #         packages_config='../../tests/packages.config',
    #         packages_folder='../../tests',
    #         destination='../../temp/from-packages-config')
    #     linker.run()
    #
    #     self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/data.txt'))
    #     self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/resources/default-data.txt'))
    #     self.assertTrue(os.path.isfile('../../temp/from-packages-config/lib-a-external-child/resources/a/data.txt'))