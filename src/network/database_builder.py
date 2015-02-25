# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sqlite3 as lite

from config import database, database_schema


class DatabaseBuilder():
    """
    Build the table and insert static data in it.  The database itself is use in server/clients thread
    """
    # TODO: try catch around database
    def __init__(self):
        """
        Initialized the database schema and static info
        :return:
        """
        if os.path.isfile(database):
            os.remove(database)
        self.conn = lite.connect(database)
        self.c = self.conn.cursor()
        with open(database_schema, 'r') as f:
            query = ""
            for line in f.readlines():
                query += line
                if lite.complete_statement(query):
                    try:
                        query = query.strip()
                        self.c.execute(query)
                    except lite.OperationalError as e:
                        if str(e.args[0]).strip() == "cannot commit - no transaction is active":
                            print("commit anyway")
                            self.conn.commit()
                    except lite.IntegrityError as e:
                        if str(e.args[0]).strip().startswith("UNIQUE constraint failed"):
                            print(e.args[0])
                    query = ""
            self.conn.commit()

    def first_time(self):
        """
        Initialized the database schema and static info
        :return:
        """
        with open(database_schema, 'r') as f:
            query = ""
            for line in f.readlines():
                query += line
                if lite.complete_statement(query):
                    try:
                        query = query.strip()
                        self.c.execute(query)
                    except lite.OperationalError as e:
                        if str(e.args[0]).strip() == "cannot commit - no transaction is active":
                            print("commit anyway")
                            self.conn.commit()
                    except lite.IntegrityError as e:
                        if str(e.args[0]).strip().startswith("UNIQUE constraint failed"):
                            print(e.args[0])
                    query = ""
            self.conn.commit()