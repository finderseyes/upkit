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
        args = args_type(config='../test_data/project-a/upkit.yaml', package_folder=None, params={})
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
        args = args_type(config='../test_data/project-b/upkit.yaml', package_folder=None, params={})

        with self.assertRaises(SystemExit):
            command.run(args)

