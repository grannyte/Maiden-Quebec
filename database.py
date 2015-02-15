# -*- coding: utf-8 -*-
from __future__ import print_function

import sqlite3

class Database():
    """

    """
    def __init__(self):
        self.conn = sqlite3.connect('data/maiden-quebec.db')
        self.c = self.conn.cursor()

    def query_connected(self, user):
        query = (user,)
        self.c.execute('SELECT * FROM connections WHERE user=?', query)
        print(self.c.fetchone())
        print(self.c.fetchone())
        return self.c.fetchone() is not None

    def add_connected(self, user):
        query = (user,)
        self.c.execute('INSERT INTO connections VALUES (?)', query)

    def remove_connected(self, user):
        query = (user,)
        self.c.execute('DELETE FROM connections WHERE user=(?)', query)
        pass