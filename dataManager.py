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

            self.cursor.execute('create table if not exists bookmark \
            (saved text not NULL, \
            userid integer not NULL, \
            FOREIGN KEY(userid) REFERENCES users(id))')
            self.conn.commit()
        except Exception as e:
            print "Initialization Exception: {}".format(e)

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def register(self, username, password):
        try:
            self.cursor.execute('insert into users (user_name, user_password) values (?, ?)', (username, password))
            self.conn.commit()
        except Exception as e:
            # returnJosn = json.dumps({"response": [{'status': False}, {'message': 'Registration Failed.'}]})
            # return returnJosn
            return None
        # returnJosn = json.dumps({"response": [{'status': True}, {'message': 'User Registered.'}]})
        # return returnJosn
        return username

    def login(self, username, password):
        try:
            self.cursor.execute('select * from users where user_name = ? and user_password = ? ', (username, password))
            res = self.cursor.fetchall()
            # if res[0] is None:
            #     returnJosn = json.dumps({"response": [{'status': False}, {'message': 'Login failed.'}]})
            #     return returnJosn
            #
            # returnJosn = json.dumps({"response": [{'status': True}, {'message': 'Logged in.'}]})
            # return returnJosn
            return None if res[0] is None else username

        except Exception as e:
            # returnJosn = json.dumps({"response": [{'status': False}, {'message': 'Login failed.'}]})
            # return returnJosn
            return None

    def addBookmark(self, userid, uri):
        # Need front end to filter uri
        try:
            self.cursor.execute('insert into bookmark (userid, saved) values (?, ?)', (userid, uri))
            self.conn.commit()
        except Exception as e:
            # returnJosn = json.dumps({"response": [{'status': False}, {'message': 'bookmark save failed.'}]})
            # return returnJosn
            return None
        # returnJosn = json.dumps({"response": [{'status': True}, {'message': 'bookmark saved.'}]})
        # return returnJosn
        return True

    def getBookmark(self, userid):
        try:
            self.cursor.execute('select saved from bookmark where userid = ?', (userid))
            res = self.cursor.fetchall()
        except Exception as e:
            # returnJosn = json.dumps({"response": [{'status': False}, {'message': 'get bookmark failed.'}]})
            # return returnJosn
            return None
        # returnJosn = json.dumps({"response": [{'status': True}, {'bookmarks': res}]})
        # return returnJosn
        return res

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
