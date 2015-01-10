# -*- coding: utf-8 -*-


import sqlite3


class Database:

    def __init__(self):
        conn = sqlite3.connect(':memory:')
        self.cursor = conn.cursor()
