import os
import unittest

import yaml

from upkit import utils
from upkit.package_linker import PackageLinker


class PackageLinkerTestCase(unittest.TestCase):
    def test_link_without_linkspec(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.0/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data.txt' % output))

    def test_link_with_empty_linkspec(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.1/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data.txt' % output))

    def test_link_with_one_child_link_in_linkspec(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.2/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/lib-a-child0/data.txt' % output))

    def test_link_with_empty_child_links_in_linkspec(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.3/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data.txt' % output))

    def test_link_with_two_child_links_in_linkspec(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.4/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/lib-a-child0/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/a/b/lib-a-child1/data.txt' % output))

    def test_link_with_content_selection_in_linkspec(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.5/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data0.txt' % output))
        self.assertTrue(os.path.isfile('%s/data1.txt' % output))
        self.assertTrue(os.path.isfile('%s/data2.txt' % output))
        self.assertFalse(os.path.isfile('%s/data.txt' % output))

    def test_link_with_content_selection_in_child_links_in_linkspec(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.6/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/child/data0.txt' % output))
        self.assertTrue(os.path.isfile('%s/child/data1.txt' % output))
        self.assertTrue(os.path.isfile('%s/child/data2.txt' % output))
        self.assertFalse(os.path.isfile('%s/child/data.txt' % output))

    def test_link_with_external_links_in_linkspec(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.7/content', target=output, forced=True,
                    params=dict(resources_package='../../tests/resources'))

        self.assertTrue(os.path.isfile('%s/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/resources/data.txt' % output))

    def test_link_with_external_links_default_content_in_linkspec(self):
        if os.path.exists('../../tests/empty_resources/default-data.txt'):
            os.remove('../../tests/empty_resources/default-data.txt')

        if os.path.exists('../../tests/empty_resources/a'):
            utils.rmdir('../../tests/empty_resources/a')

        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.8/content', target=output, forced=True,
                    params=dict(resources_package='../../tests/empty_resources'))

        self.assertTrue(os.path.isfile('%s/child/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/child/resources/default-data.txt' % output))
        self.assertTrue(os.path.isfile('%s/child/resources/a/data.txt' % output))

    def test_overwrite_linkspec(self):
        import os

        content = """
links:
- source: '{{__dir__}}/aaa'
  target: '{{__target__}}/aaa'
external_links:
- source: '{{resources_package}}'
  target: '{{__dir__}}/aaa/resources'
  default_content: ['{{__dir__}}/_resources/*']
"""
        package_linkspec = yaml.load(content)

        if os.path.exists('../../tests/empty_resources/default-data.txt'):
            os.remove('../../tests/empty_resources/default-data.txt')

        if os.path.exists('../../tests/empty_resources/a'):
            utils.rmdir('../../tests/empty_resources/a')

        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.8/content', target=output, forced=True,
                    package_linkspec=package_linkspec,
                    params=dict(resources_package='../../tests/empty_resources'))

        self.assertTrue(os.path.isfile('%s/aaa/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/aaa/resources/default-data.txt' % output))
        self.assertTrue(os.path.isfile('%s/aaa/resources/a/data.txt' % output))

    def test_link_with_no_target_if_linkspec_has_links(self):
        output = '../../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../../tests/lib-a.1.0.9/content', forced=True,
                    params={'output': output})

        self.assertTrue(os.path.isfile('%s/child/data.txt' % output))

    def test_run_from_config(self):
        output = '../../temp/output/run-config'
        utils.rmdir(output)

        linker = PackageLinker(config='../../tests/config.yaml', params={
            'output': output
        })
        linker.run()

        self.assertTrue(os.path.isfile('%s/lib-a/child/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/lib-a/child/resources/default-data.txt' % output))
        self.assertTrue(os.path.isfile('%s/lib-a/child/resources/a/data.txt' % output))

        self.assertTrue(os.path.isfile('%s/lib-c/c-data.txt' % output))

    def test_run_from_config_and_overwrite_linkspec(self):
        output = '../../temp/output/run-config-overwrite'
        utils.rmdir(output)

        linker = PackageLinker(config='../../tests/config-overwrite.yaml', params={
            'output': output
        })
        linker.run()

        self.assertTrue(os.path.isfile('%s/lib-a/aaa/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/lib-a/aaa/resources/default-data.txt' % output))
        self.assertTrue(os.path.isfile('%s/lib-a/aaa/resources/a/data.txt' % output))

        self.assertTrue(os.path.isfile('%s/lib-c/c-data.txt' % output))

    def test_run_from_config_and_overwrite_params(self):
        output = '../../temp/output/run-config-params-overwrite'
        utils.rmdir(output)

        linker = PackageLinker(
            config='../../tests/config-params-overwrite.yaml',
            params={'output': output}
        )
        linker.run()

        self.assertTrue(os.path.isfile('%s/project-ios/assets/images/fake-image.txt' % output))
        self.assertTrue(os.path.isfile('%s/project-ios/assets/plugins/lib-c/c-data.txt' % output))

        linker = PackageLinker(
            config='../../tests/config-params-overwrite.yaml',
            params={'output': output, 'platform': 'android'}
        )
        linker.run()

        self.assertTrue(os.path.isfile('%s/project-android/assets/images/fake-image.txt' % output))
        self.assertTrue(os.path.isfile('%s/project-android/assets/plugins/lib-c/c-data.txt' % output))

    def test_run_from_config_with_no_link_targets(self):
        output = '../../temp/output/run-config-no-link-targets'
        utils.rmdir(output)

        linker = PackageLinker(config='../../tests/config-no-link-targets.yaml', params={
            'output': output
        })
        linker.run()

        self.assertTrue(os.path.isfile('%s/child/data.txt' % output))