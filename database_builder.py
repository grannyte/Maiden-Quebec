# -*- coding: utf-8 -*-
from __future__ import print_function

import sqlite3

from config import database


class DatabaseBuilder():
    """
    Build the table and insert static data in it.  The database itself is use in server/clients thread
    """
    def __init__(self, ):
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()
        if not self.does_exist():
            self.first_time()

    def does_exist(self):
        """
        Determine whether or not the database exists
        :return: True if database exists else False
        """
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='players';")
        return self.c.fetchone() is not None

    def first_time(self):
        self.c.execute('''CREATE TABLE connections
             (user text primary key)''')

        # Create and populate players' table
        self.c.execute('''CREATE TABLE players
             (user text primary key, pass text, race text,
              level int, hp int, max_hp int, zone text,
              x int, y int)''')
        players = [
            ('pl', 'lp', 'spearman', 2, 80, 80, 'temple', 8, 8),
            ('jm', 'mj', 'spearman', 2, 60, 80, 'temple', 8, 8),
            ('dd', 'dd', 'spearman', 2, 40, 80, 'temple', 8, 8),
            ]
        self.c.executemany('INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?)', players)

        # Create and populate monsters' table
        self.c.execute('''CREATE TABLE monsters
             (name text primary key, race text,
              level integer, hp integer, max_hp integer,
              zone text, x integer, y integer,
              weapon text, spells text
             )''')
        monsters = [
            ('spearman', 'human', 2, 24, 24, '', 0, 0, 'spear', ""),
            # ('skeleton-archer', 'skeleton', 2, 16, 16, '', 0, 0, 'bow', ""),
            ('skeleton-spearman', 'skeleton', 2, 24, 24, '', 0, 0, 'spear', ""),
            # ('skeleton-mage', 'skeleton', 4, 12, 12, '', 0, 0, 'hand', ""),
            # ("Makrsh P'tangh", 'skeleton', 256, 65536, 65536, '', 0, 0, 'hand', ""),
            # ('orc-archer', 'orc', 2, 16, 16, '', 0, 0, 'bow', ""),
            ('orc-spearman', 'orc', 2, 24, 24, '', 0, 0, 'spear', ""),
            # ('orc-mage', 'orc', 4, 12, 12, '', 0, 0, 'hand', ""),
            # ('Azog', 'orc', 10, 1024, 1024, '', 0, 0, 'spear', ""),
            ]
        self.c.executemany('INSERT INTO monsters VALUES (?,?,?,?,?,?,?,?,?,?)', monsters)

        # Create and populate weapons' table
        self.c.execute('''CREATE TABLE weapons
             (name text, type text, min, max, spells)''')
        weapons = [
            ('bow', 'aim', 2, 5, ""),
            # ('cupid', 'aim', 1, 2, "charm"), #  Cupid's bow
            ('great-bow', 'aim', 3, 6, ""),
            ('composite-bow', 'aim', 5, 10, ""),
            ('hand', 'cast', 1, 3, ""),
            ('spear', 'thrust', 2, 5, ""),
            ('gungnir', 'thrust', 36768, 36768, ""),  # Odin's spear.
            ('rhongomiant', 'thrust', 16384, 16384, ""),  # King Arthur's spear
            ('wand', 'cast', 2, 5, ""),
            ('phoenix-wand', 'cast', 2, 5, ""),  # Harry Potter's wand
            ]
        self.c.executemany('INSERT INTO weapons VALUES (?,?,?,?,?)', weapons)

        # Create and populate weapons' table
        self.c.execute('''CREATE TABLE spells
             (name text, type text, target, min, max)''')
        spells = [
            ('charm', 'aim', 'single', 2, 5),
            ]
        self.c.executemany('INSERT INTO spells VALUES (?,?,?,?,?)', spells)

    def remove_connected(self, user):
        pass