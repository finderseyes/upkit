import os
import unittest
from collections import namedtuple

from upkit import utils
from upkit.tools import LinkPackageCommand


class LinkPackageCommandTestCase(unittest.TestCase):
    def test_should_link_with_default_unity_project_link_template(self):
        output = '../temp/output/project-a'
        utils.rmdir(output)

        command = LinkPackageCommand()

        args_type = namedtuple('args', ['config', 'package_folder', 'params'])
        args = args_type(config='../test_data/project-a/upkit.yaml', package_folder='../temp/packages', params={})
        command.run(args)

        self.assertTrue(os.path.isdir(output))
        self.assertTrue(os.path.isdir(os.path.join(output, 'Assets/Scripts')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'Assets/Scripts.meta')))
        self.assertFalse(os.path.exists(os.path.join(output, 'Assets/.gitignore')))

    def test_should_not_link_with_default_unity_project_link_template_without_required_project_param(self):
        output = '../temp/output/project-b'
        utils.rmdir(output)

        command = LinkPackageCommand()

        args_type = namedtuple('args', ['config', 'package_folder', 'params'])
        args = args_type(config='../test_data/project-b/upkit.yaml', package_folder='../temp/packages', params={})

        with self.assertRaises(SystemExit):
            command.run(args)

    def test_should_link_with_jinja_config(self):
        output = '../temp/output/project-c-ios'
        utils.rmdir(output)

        command = LinkPackageCommand()

        args_type = namedtuple('args', ['config', 'package_folder', 'params'])
        args = args_type(config='../test_data/project-c/upkit.yaml', package_folder='../temp/packages', params={})
        command.run(args)

        self.assertTrue(os.path.isdir(output))
        self.assertTrue(os.path.isdir(os.path.join(output, 'Assets/ios-asset')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'Assets/ios-asset.meta')))
        self.assertTrue(os.path.isdir(os.path.join(output, 'Assets/Plugins/ios-plugin')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'Assets/Plugins/ios-plugin.meta')))
        self.assertFalse(os.path.exists(os.path.join(output, 'Assets/.gitignore')))

