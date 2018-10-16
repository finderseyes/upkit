import os
import unittest
from unity_tools.package_linker import PackageLinker


class PackageLinkerTestCase(unittest.TestCase):
    def setUp(self):
        self._linker = PackageLinker()

    def test_link_without_linkspecs(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.0/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-a/data.txt'))

    def test_link_with_child_packages(self):
        self._linker.link(name='lib-a',
                          source='../../tests/lib-a1.0.1/content',
                          destination='../../temp',
                          forced=True)

        self.assertTrue(os.path.isfile('../../temp/lib-a/data.txt'))

