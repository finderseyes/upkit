import os
import unittest
from unity_tools import utils


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.getcwd()

    def test_link_without_linkspecs(self):
        print(self.current_dir)


