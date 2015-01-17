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
        expect = ("#######"
                  "#     #"
                  "# H  *#"
                  "#  ++$#"
                  "#######"
        )
        self.assertEqual(expect, actual)

    def test_getNumberOfRows(self):
        filename= os.path.abspath(os.path.join(self.data_dir, "level00.map"))
        map = Map(filename)
        actual = map.getNumberOfRows()
        expect = 5
        self.assertEqual(expect, actual)

    def test_getNumberOfColumns(self):
        filename= os.path.abspath(os.path.join(self.data_dir, "level00.map"))
        map = Map(filename)
        actual = map.getNumberOfColumns()
        expect = 7
        self.assertEqual(expect, actual)

    def test_getElement(self):
        filename= os.path.abspath(os.path.join(self.data_dir, "level00.map"))
        map = Map(filename)
        actual = map.getElement(2,2)
        expect = 'H'
        self.assertEqual(expect, actual)

    def test_getPositionElement(self):
        filename= os.path.abspath(os.path.join(self.data_dir, "level00.map"))
        map = Map(filename)
        actual_row, actual_col = map.getPositionElement('$')
        expect_row = 3
        expect_col = 5
        self.assertEqual(expect_row, actual_row)
        self.assertEqual(expect_col, actual_col)

if __name__ == '__main__':
    unittest.main()
