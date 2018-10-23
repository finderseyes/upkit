import os
import unittest
from collections import namedtuple

from upkit import utils
from upkit.tools import CreatePackageCommand


class CreatePackageCommandTestCase(unittest.TestCase):
    def test_should_create_package_when_location_not_exist(self):
        output = '../temp/output/test-package'
        utils.rmdir(output)

        command = CreatePackageCommand()

        args_type = namedtuple('args', 'location')
        args = args_type(location=output)
        command.run(args)

        self.assertTrue(os.path.isdir(output))
        self.assertTrue(os.path.isfile(os.path.join(output, 'upkit.yaml')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'linkspec.yaml')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'package.nuspec')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project', 'assets')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project', 'assets', 'plugins')))

    def test_should_create_package_when_location_is_empty(self):
        output = '../temp/output/test-package'
        utils.rmdir(output)
        utils.mkdir_p(output)

        command = CreatePackageCommand()

        args_type = namedtuple('args', 'location')
        args = args_type(location=output)
        command.run(args)

        self.assertTrue(os.path.isdir(output))
        self.assertTrue(os.path.isfile(os.path.join(output, 'upkit.yaml')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'linkspec.yaml')))
        self.assertTrue(os.path.isfile(os.path.join(output, 'package.nuspec')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project', 'assets')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project', 'assets', 'plugins')))

    def test_should_not_create_package_when_location_is_not_empty(self):
        output = '../temp/output/test-package'
        utils.rmdir(output)
        utils.mkdir_p(output)
        utils.touch(os.path.join(os.path.abspath(output), 'data.txt'))

        with self.assertRaises(SystemExit):
            command = CreatePackageCommand()
            args_type = namedtuple('args', 'location')
            args = args_type(location=output)
            command.run(args)

        self.assertFalse(os.path.isfile(os.path.join(output, 'upkit.yaml')))
        self.assertFalse(os.path.isfile(os.path.join(output, 'linkspec.yaml')))
        self.assertFalse(os.path.isfile(os.path.join(output, 'package.nuspec')))

