import os
import unittest
from collections import namedtuple

from upkit import utils
from upkit.tools import CreatePackageCommand


class CreatePackageCommandTestCase(unittest.TestCase):
    def test_should_create_package_when_location_is_empty(self):
        output = '../temp/output/test-package'
        utils.rmdir(output)

        command = CreatePackageCommand()

        args_type = namedtuple('args', 'location')
        args = args_type(location=output)
        command.run(args)

        self.assertTrue(os.path.isdir(output))
        self.assertTrue(os.path.isfile(os.path.join(output, 'package-config.yaml')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project', 'assets')))
        # self.assertTrue(os.path.isdir(os.path.join(output, 'project', 'assets', 'plugins')))

