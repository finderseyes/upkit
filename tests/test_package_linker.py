import os
import unittest

import yaml

from upkit import utils
from upkit.package_linker import PackageLinker


class PackageLinkerTestCase(unittest.TestCase):
    def test_link_without_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.0/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data.txt' % output))

    def test_link_with_empty_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.1/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data.txt' % output))

    def test_link_with_one_child_link_in_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.2/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/lib-a-child0/data.txt' % output))

    def test_link_with_empty_child_links_in_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.3/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data.txt' % output))

    def test_link_with_two_child_links_in_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.4/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/lib-a-child0/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/a/b/lib-a-child1/data.txt' % output))

    def test_link_with_content_selection_in_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.5/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data0.txt' % output))
        self.assertTrue(os.path.isfile('%s/data1.txt' % output))
        self.assertTrue(os.path.isfile('%s/data2.txt' % output))
        self.assertFalse(os.path.isfile('%s/data.txt' % output))

    def test_link_with_content_selection_in_child_links_in_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.6/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/child/data0.txt' % output))
        self.assertTrue(os.path.isfile('%s/child/data1.txt' % output))
        self.assertTrue(os.path.isfile('%s/child/data2.txt' % output))
        self.assertFalse(os.path.isfile('%s/child/data.txt' % output))

    def test_link_with_external_links_in_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.7/content', target=output, forced=True,
                    params=dict(resources_package='../test_data/resources'))

        self.assertTrue(os.path.isfile('%s/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/resources/data.txt' % output))

    def test_link_with_external_links_default_content_in_linkspec(self):
        if os.path.exists('../test_data/empty_resources/default-data.txt'):
            os.remove('../test_data/empty_resources/default-data.txt')

        if os.path.exists('../test_data/empty_resources/a'):
            utils.rmdir('../test_data/empty_resources/a')

        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.8/content', target=output, forced=True,
                    params=dict(resources_package='../test_data/empty_resources'))

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

        if os.path.exists('../test_data/empty_resources/default-data.txt'):
            os.remove('../test_data/empty_resources/default-data.txt')

        if os.path.exists('../test_data/empty_resources/a'):
            utils.rmdir('../test_data/empty_resources/a')

        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.8/content', target=output, forced=True,
                    params=dict(resources_package='../test_data/empty_resources'), **package_linkspec)

        self.assertTrue(os.path.isfile('%s/aaa/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/aaa/resources/default-data.txt' % output))
        self.assertTrue(os.path.isfile('%s/aaa/resources/a/data.txt' % output))

    def test_link_with_no_target_if_linkspec_has_links(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.9/content', forced=True,
                    params={'output': output})

        self.assertTrue(os.path.isfile('%s/child/data.txt' % output))

    def test_run_from_config(self):
        output = '../temp/output/run-config'
        utils.rmdir(output)

        linker = PackageLinker(config_file='../test_data/config.yaml', params={
            'output': output
        })
        linker.run()

        self.assertTrue(os.path.isfile('%s/lib-a/child/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/lib-a/child/resources/default-data.txt' % output))
        self.assertTrue(os.path.isfile('%s/lib-a/child/resources/a/data.txt' % output))

        self.assertTrue(os.path.isfile('%s/lib-c/c-data.txt' % output))

    def test_run_from_config_and_overwrite_linkspec(self):
        output = '../temp/output/run-config-overwrite'
        utils.rmdir(output)

        linker = PackageLinker(config_file='../test_data/config-overwrite.yaml', params={
            'output': output
        })
        linker.run()

        self.assertTrue(os.path.isfile('%s/lib-a/aaa/data.txt' % output))
        self.assertTrue(os.path.isfile('%s/lib-a/aaa/resources/default-data.txt' % output))
        self.assertTrue(os.path.isfile('%s/lib-a/aaa/resources/a/data.txt' % output))

        self.assertTrue(os.path.isfile('%s/lib-c/c-data.txt' % output))

    def test_run_from_config_and_overwrite_params(self):
        output = '../temp/output/run-config-params-overwrite'
        utils.rmdir(output)

        linker = PackageLinker(
            config_file='../test_data/config-params-overwrite.yaml',
            params={'output': output}
        )
        linker.run()

        self.assertTrue(os.path.isfile('%s/project-ios/assets/images/fake-image.txt' % output))
        self.assertTrue(os.path.isfile('%s/project-ios/assets/plugins/lib-c/c-data.txt' % output))

        linker = PackageLinker(
            config_file='../test_data/config-params-overwrite.yaml',
            params={'output': output, 'platform': 'android'}
        )
        linker.run()

        self.assertTrue(os.path.isfile('%s/project-android/assets/images/fake-image.txt' % output))
        self.assertTrue(os.path.isfile('%s/project-android/assets/plugins/lib-c/c-data.txt' % output))

    def test_run_from_config_with_no_link_targets(self):
        output = '../temp/output/run-config-no-link-targets'
        utils.rmdir(output)

        linker = PackageLinker(config_file='../test_data/config-no-link-targets.yaml', params={
            'output': output
        })
        linker.run()

        self.assertTrue(os.path.isfile('%s/child/data.txt' % output))

    def test_link_with_content_selection_and_exclude_in_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.5.1/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/data0.txt' % output))
        self.assertTrue(os.path.isfile('%s/data2.txt' % output))
        self.assertFalse(os.path.isfile('%s/data1.txt' % output))
        self.assertFalse(os.path.isfile('%s/data.txt' % output))

    def test_link_with_content_selection_and_exclude_child_package_in_linkspec(self):
        output = '../temp/output/lib-a'
        utils.rmdir(output)

        linker = PackageLinker()
        linker.link(source='../test_data/lib-a.1.0.6.1/content', target=output, forced=True)

        self.assertTrue(os.path.isfile('%s/child/data0.txt' % output))
        self.assertTrue(os.path.isfile('%s/child/data2.txt' % output))
        self.assertFalse(os.path.isfile('%s/child/data1.txt' % output))
        self.assertFalse(os.path.isfile('%s/child/data.txt' % output))

    def test_support_nuget_source(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='nuget:NuGet.Core@2.14.0', target=output, forced=True)
        # linker.link(source='git:http://NuGet.Core@2.14.0', target=output, forced=True)

        self.assertTrue(os.path.isdir(os.path.join(package_folder, 'Nuget.Core.2.14.0')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'Nuget.Core.2.14.0.nupkg')))

    def test_support_nuget_source_with_path(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='nuget:NuGet.Core@2.14.0#lib', target=output, forced=True)
        # linker.link(source='git:http://NuGet.Core@2.14.0', target=output, forced=True)

        self.assertTrue(os.path.isdir(os.path.join(package_folder, 'Nuget.Core.2.14.0')))
        self.assertTrue(os.path.isdir(os.path.join(output, 'net40-Client')))

    def test_support_nuget_source_with_deep_path(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='nuget:NuGet.Core@2.14.0#lib/net40-Client', target=output, forced=True)
        # linker.link(source='git:http://NuGet.Core@2.14.0', target=output, forced=True)

        self.assertTrue(os.path.isdir(os.path.join(package_folder, 'Nuget.Core.2.14.0')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'NuGet.Core.Dll')))

    def test_support_git_source(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git',
                    target=output, forced=True)
        # linker.link(source='git:http://NuGet.Core@2.14.0', target=output, forced=True)

        # self.assertTrue(os.path.isfile(os.path.join(package_folder, 'README.md')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'README.md')))

    def test_support_git_source_using_ssh(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:git@bitbucket.org:tuongvu/upkit-test-package.git',
                    target=output, forced=True)
        # linker.link(source='git:http://NuGet.Core@2.14.0', target=output, forced=True)

        # self.assertTrue(os.path.isfile(os.path.join(package_folder, 'README.md')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'README.md')))

    def test_support_git_source_and_path(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git#aaa',
                    target=output, forced=True)
        # linker.link(source='git:http://NuGet.Core@2.14.0', target=output, forced=True)

        # self.assertTrue(os.path.isfile(os.path.join(package_folder, 'README.md')))
        self.assertTrue(os.path.isfile(os.path.join(output, '111.txt')))

    def test_support_git_source_with_branch(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git@feature/ccc',
                    target=output, forced=True)

        self.assertTrue(os.path.isdir(os.path.join(output, 'ccc')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'README.md')))

    def test_support_git_source_with_branch_via_ssh(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:git@bitbucket.org:tuongvu/upkit-test-package.git@feature/ccc',
                    target=output, forced=True)

        self.assertTrue(os.path.isdir(os.path.join(output, 'ccc')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'README.md')))

    def test_support_git_source_with_branch_and_path(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git@feature/ccc#ccc',
                    target=output, forced=True)

        self.assertTrue(os.path.isfile(os.path.join(output, '333.txt')))

    def test_support_git_source_with_tag(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git@tag-1',
                    target=output, forced=True)
        # linker.link(source='git:http://NuGet.Core@2.14.0', target=output, forced=True)

        self.assertTrue(os.path.isdir(os.path.join(output, 'ccc')))
        self.assertFalse(os.path.isdir(os.path.join(output, 'eee')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'README.md')))

    def test_support_git_source_if_already_cloned(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git',
                    target=output, forced=True)

        # link again, with existing package folder
        utils.rmdir(output)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git',
                    target=output, forced=True)

        self.assertTrue(os.path.isfile(os.path.join(output, 'README.md')))

    def test_support_git_source_with_branch_if_already_cloned(self):
        output = '../temp/output/lib-a'
        package_folder = '../temp/output/packages'

        utils.rmdir(output)
        utils.rmdir(package_folder)

        linker = PackageLinker(package_folder=package_folder)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git@feature/ccc',
                    target=output, forced=True)

        # link again, with existing package folder
        utils.rmdir(output)
        linker.link(source='git:https://bitbucket.org/tuongvu/upkit-test-package.git@feature/ccc',
                    target=output, forced=True)

        self.assertTrue(os.path.isdir(os.path.join(output, 'ccc')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'README.md')))


