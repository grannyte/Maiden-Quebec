# -*- coding: utf-8 -*-

import unittest
import os

from src.map.loader import load_from_file


class MapLoaderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        parent = os.path.abspath(os.path.join(cwd, os.pardir))
        parent = os.path.abspath(os.path.join(parent, os.pardir))
        cls.project_dir = os.path.abspath(os.path.join(parent, os.pardir))
        cls.data_dir = os.path.abspath(os.path.join(parent, "data"))

    def test_fail_to_open_file(self):
        self.assertRaises(OSError, load_from_file, "filename_that_should_not_exist")

    def test_load_the_file_content(self):
        filename= os.path.abspath(os.path.join(self.data_dir, "level00.map"))
        actual = load_from_file(filename)
        expect = ("#######\n"
                  "#     #\n"
                  "# H  *#\n"
                  "#  ++$#\n"
                  "#######"
        )
        self.assertEqual(expect, actual)

if __name__ == '__main__':
    unittest.main()
