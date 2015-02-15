# -*- coding: utf-8 -*-
from __future__ import print_function

import sqlite3

class Database():
    """

    """
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()

        # Create table
        self.c.execute('''CREATE TABLE connections
             (user text primary key)''')

        # Create and populate players' table
        self.c.execute('''CREATE TABLE players
             (user text primary key, pass text, skin text,
              level int, hp int, max_hp int, zone text,
              x int, y int)''')
        players = [
            ('pl', 'lp', 'rogue', 2, 80, 80, 'temple', 8, 8),
            ('jm', 'mj', 'mage', 2, 60, 80, 'temple', 8, 8),
            ('dd', 'dd', 'warrior', 2, 40, 80, 'temple', 8, 8),
            ]
        self.c.executemany('INSERT INTO players VALUES (?,?,?,?,?,?,?)', players)

        # Create and populate monsters' table
        self.c.execute('''CREATE TABLE monsters
             (name text primary key, type text,
              level integer, hp integer, max_hp integer,
              zone text, x integer, y integer,
              weapon text, spells text
             )''')
        monsters = [
            ('skeleton-archer', 'skeleton', 2, 16, 16, '', 0, 0, 'bow', ""),
            ('skeleton-warrior', 'skeleton', 2, 24, 24, '', 0, 0, 'spear', ""),
            ('skeleton-mage', 'skeleton', 4, 12, 12, '', 0, 0, 'hand', ""),
            ("Makrsh P'tangh", 'skeleton', 256, 65536, 65536, '', 0, 0, 'hand', ""),
            ('skeleton-archer', 'skeleton', 2, 16, 16, '', 0, 0, 'bow', ""),
            ('skeleton-warrior', 'skeleton', 2, 24, 24, '', 0, 0, 'spear', ""),
            ('skeleton-mage', 'skeleton', 4, 12, 12, '', 0, 0, 'hand', ""),
            ('Azog', 'orc', 10, 1024, 1024, '', 0, 0, 'spear', ""),
            ]
        self.c.executemany('INSERT INTO monsters VALUES (?,?,?,?,?,?,?)', monsters)

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
            ('wand', 'cast', 2, 5),
            ('phoenix-wand', 'cast', 2, 5),  # Harry Potter's wand
            ]
        self.c.executemany('INSERT INTO weapons VALUES (?,?,?,?,?,?,?)', weapons)

        # Create and populate weapons' table
        self.c.execute('''CREATE TABLE spells
             (name text, type text, target, min, max)''')
        spells = [
            ('charm', 'aim', 'single', 2, 5),
            ]
        self.c.executemany('INSERT INTO spells VALUES (?,?,?,?,?,?,?)', spells)
