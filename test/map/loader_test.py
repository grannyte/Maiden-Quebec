# -*- coding: utf-8 -*-

import unittest
import os

from src.map.loader import Map


class MapLoaderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        parent = os.path.abspath(os.path.join(cwd, os.pardir))
        parent = os.path.abspath(os.path.join(parent, os.pardir))
        cls.project_dir = os.path.abspath(os.path.join(parent, os.pardir))
        cls.data_dir = os.path.abspath(os.path.join(parent, "data"))

    def test_constructeur_avec_fichier_inexistant(self):
        filename= os.path.abspath(os.path.join(self.data_dir, "levelXX.map"))
        with self.assertRaises(FileNotFoundError):
            map = Map(filename)

    def test_constructeur_avec_fichier_existant_level00(self):
        filename= os.path.abspath(os.path.join(self.data_dir, "level00.map"))
        try:
            map = Map(filename)
        except FileNotFoundError:
            self.fail()

    def test_repr(self):
        filename= os.path.abspath(os.path.join(self.data_dir, "level00.map"))
        actual = str(Map(filename))
        expect = ("#######\n"
                  "#     #\n"
                  "# H  *#\n"
                  "#  ++$#\n"
                  "#######"
        )
        self.assertEqual(expect, actual)

if __name__ == '__main__':
    unittest.main()
