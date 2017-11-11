# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Weijie Lin

import sqlite3
import json

class manager():

    def __init__(self):
        # initialize database and make sure user table exists
        self.conn = sqlite3.connect('data/user.db')
        # Access row value by column name like a dictionary
        # self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('create table if not exists users ( \
            id integer PRIMARY KEY AUTOINCREMENT, \
            user_name varchar(20) NOT NULL UNIQUE, \
            user_password varchar(40) NOT NULL)')
            self.conn.commit()
        except Exception as e:
            print "Initialization Exception: {}".format(e)

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()
        print "db connection closed"

    def __enter__(self):
        return self

    def register(self, userName, password):
        try:
            self.cursor.execute('insert into users (user_name, user_password) values (?, ?)', (userName, password))
            self.conn.commit()
        except Exception as e:
            return "Registration Error: {}".format(e)
        return "User Registered."

    def login(self, userName, password):
        try:
            self.cursor.execute('select * from users where user_name = ? and user_password = ? ', (userName, password))
            res = self.cursor.fetchall()
            if res[0] is None:
                return False
            return True

        except Exception as e:
            print "Error when check user identity {}".format(e)
            return False

    def getUsers(self):
        results = None
        try:
            self.cursor.execute('select * from users')
            # userNames = [row['user_name'] for row in results]
            results = self.cursor.fetchall()
        except Exception as e:
            return "Fetch User Error {}".format(e)
        return results


    def dropTable(self):
        try:
            self.cursor.execute('drop table if exists users')
        except Exception as e:
            return "Error when drop table {}".format(e)
        return "table dropped"
