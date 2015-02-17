# -*- coding: utf-8 -*-
from __future__ import print_function

import sqlite3 as lite

class Database():
    """
    """
    def __init__(self):
        self.conn = lite.connect('data/maiden-quebec.db')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def is_user_connected(self, user):
        self.c.execute('SELECT * FROM connections WHERE user=? and date_out=?', (user, None))
        return self.c.fetchone() is None

    def login(self, user, date_in):
        self.c.execute('INSERT INTO connections VALUES (?,?,?)', (user, date_in, None))
        self.conn.commit()

    def logout(self, user, date_out):
        self.c.execute('UPDATE connections SET date_out=? WHERE user=? and date_out=?', (user, date_out))
        self.conn.commit()

    def does_zone_exist(self, zone):
        self.c.execute('SELECT * FROM connections WHERE zone=?', (zone,))
        return self.c.fetchone() is not None

    def fetch_zone(self, zone):
        self.c.execute('SELECT * FROM connections WHERE zone=?', (zone,))


    def query_entities_in(self, zone):
        query = (zone,)
        self.c.execute('SELECT * FROM players WHERE zone=?', (query,))