# -*- coding: utf-8 -*-


def load_from_file(filename):
        """Charge un fichier à partir d'un fichier"""
        map_as_string = []
        with open(filename) as f:
            map_as_string = f.readlines()
        return ''.join(map_as_string)