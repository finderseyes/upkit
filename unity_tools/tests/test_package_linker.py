import os
import unittest
from unity_tools.package_linker import PackageLinker


class PackageLinkerTestCase(unittest.TestCase):
    def setUp(self):
        self._linker = PackageLinker()

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
        self.assertFalse(os.path.isfile('../../temp/lib-a-selective/data0.txt'))
