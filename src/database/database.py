# -*- coding: utf-8 -*-


import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.conn.close()

    def populate(self):
        """Inscrit des éléments à l'intérieur de la base de données"""
        self.cursor.execute('CREATE TABLE weapons (name, damage)')
        weapons = [('excalibur', 10),
                   ('Ragnarok', 5),
                   ('dague rouillé', 1),
                   ]
        self.cursor.executemany('INSERT INTO weapons VALUES (?,?)', weapons)