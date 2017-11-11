# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Weijie Lin

import sqlite3

class manager():

    def __init__(self):
        # initialize database and make sure user table exists
        self.conn = sqlite3.connect('data/user.db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('create table if not exists users (userName unique, password)')
            self.conn.commit()
        except Exception as e:
            return "Initialization Exception: {}".format(e)

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()
        print "db connection closed"

    def __enter__(self):
        return self

    def register(self, userName, password):
        try:
            self.cursor.execute('insert into users (userName, password) values (?, ?)', (userName, password))
            self.conn.commit()
        except Exception as e:
            return "Registration Error: {}".format(e)
        return "User Registered."

    def getUsers(self):
        results = None
        try:
            self.cursor.execute('select * from users')
            results = self.cursor.fetchall()
        except Exception as e:
            return "Fetch User Error {}".format(e)
        return results


    def dropTable(self):
        try:
            self.cursor.execute('drop table if exists users')
            self.conn.commit()
        except Exception as e:
            return "Error when drop table {}".format(e)
        return "table dropped"
