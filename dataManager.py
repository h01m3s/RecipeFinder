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

    def register(self, username, password):
        try:
            self.cursor.execute('insert into users (user_name, user_password) values (?, ?)', (username, password))
            self.conn.commit()
        except Exception as e:
            returnJosn = json.dumps({"response": [{'status': False}, {'message': 'Registration Failed.'}]})
            # return "Registration Error: {}".format(e)
            return returnJosn
        returnJosn = json.dumps({"response": [{'status': True}, {'message': 'User Registered.'}]})
        return returnJosn

    def login(self, username, password):
        try:
            self.cursor.execute('select * from users where user_name = ? and user_password = ? ', (username, password))
            res = self.cursor.fetchall()
            if res[0] is None:
                returnJosn = json.dumps({"response": [{'status': False}, {'message': 'Login failed.'}]})
                return returnJosn

            returnJosn = json.dumps({"response": [{'status': True}, {'message': 'Logged in.'}]})
            return returnJosn

        except Exception as e:
            returnJosn = json.dumps({"response": [{'status': False}, {'message': 'Login failed.'}]})
            return returnJosn

    def getUsers(self):
        results = None
        try:
            self.cursor.execute('select * from users')
            results = self.cursor.fetchall()
        except Exception as e:
            return "Fetch User Error {}".format(e)
        return json.dumps({"response": {"users":results}})


    # debug purpose
    def dropTable(self):
        try:
            self.cursor.execute('drop table if exists users')
        except Exception as e:
            return "Error when drop table {}".format(e)
        return "table dropped"
