# -*- coding: utf-8 -*-


def load_from_file(self, filename):
        """Charge un fichier à partir d'un fichier"""
        map_as_string = []
        with open(filename) as f:
            map_as_string = f.readlines()
        return map_as_string