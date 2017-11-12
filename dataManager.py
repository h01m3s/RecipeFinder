# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Weijie Lin

import sqlite3
import json
import web

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
            user_name VARCHAR(20) NOT NULL UNIQUE, \
            user_password VARCHAR(40) NOT NULL)')

            self.cursor.execute('create table if not exists bookmark \
            (saved text not NULL, \
            user_name VARCHAR(20) not NULL, \
            FOREIGN KEY(user_name) REFERENCES users(user_name))')
            self.conn.commit()
        except Exception as e:
            print "Initialization Exception: {}".format(e)

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def register(self, username, password):
        returnJosnFailed = json.dumps({'username': "none", \
                                'message': 'registration Failed.'})
        returnJosnSuccess = json.dumps({'username': username, \
                                'message': 'registration success.'})
        try:
            self.cursor.execute('insert into users (user_name, user_password) values (?, ?)', (username, password))
            self.conn.commit()
            return returnJosnSuccess
        except sqlite3.Error as se:
            # print "A database error has occured: {}".format(se.args[0])
            if se.args[0] == "UNIQUE constraint failed: users.user_name":
                msg = "User already exist."
            return web.HTTPError("400 Bad Request", {"Content-type": "application/json"}, msg)
        except Exception as e:
            return web.HTTPError("400 Bad Request", {"Content-type": "application/json"}, returnJosnFailed)

    def login(self, username, password):
        returnJosnFailed = json.dumps({'username': "none", \
                                'message': 'login Failed.'})
        returnJosnSuccess = json.dumps({'username': username, \
                                'message': 'login success.'})
        try:
            self.cursor.execute('select * from users where user_name = ? and user_password = ? ', (username, password))
            res = self.cursor.fetchall()

            if res[0] is None:
                return web.HTTPError("400 Bad Request", {"Content-type": "application/json"}, returnJosnFailed)

            return returnJosnSuccess

        except Exception as e:
            return web.HTTPError("400 Bad Request", {"Content-type": "application/json"}, returnJosnFailed)

    def addBookmark(self, username, uri):
        # NEED TO CHECK IF USERNAME EXISTS IN USER TABLE AND RESTRICT URI(UNIQUE)
        returnJosnFailed = json.dumps({'username': "none", \
                                'message': 'Error when add bookmark.'})
        returnJosnSuccess = json.dumps({'username': username, \
                                'message': 'bookmark added'})
        # Need front end to filter uri
        try:
            self.cursor.execute('insert into bookmark (user_name, saved) values (?, ?)', (username, uri))
            self.conn.commit()
            return returnJosnSuccess
        except Exception as e:
            return web.HTTPError("400 Bad Request", {"Content-type": "application/json"}, returnJosnFailed)

    def getBookmark(self, username):
        try:
            self.cursor.execute('select saved from bookmark where user_name = ?', (username,))
            res = self.cursor.fetchall()
            returnJsonSuccess = json.dumps({"bookmark": res, "message":"get bookmark success"})
            return returnJsonSuccess
        except Exception as e:
            print "error when fetch bookmarks: {}".format(e)
            returnJosnFailed = json.dumps({"bookmark": "none", "message":"get bookmark failed"})
            return web.HTTPError("400 Bad Request", {"Content-type": "application/json"}, returnJosnFailed)

    # debug purpose
    def getUsers(self):
        try:
            self.cursor.execute('select * from users')
            users = self.cursor.fetchall()
            self.cursor.execute('select * from bookmark')
            bookmarks = self.cursor.fetchall()
            if users and bookmarks is not None:
                return json.dumps({"users": users, "bookmarks": bookmarks})
        except Exception as e:
            return "Fetch User Error {}".format(e)

    # debug purpose
    def dropTable(self):
        try:
            self.cursor.execute('drop table if exists users')
            self.cursor.execute('drop table if exists bookmark')
        except Exception as e:
            return "Error when drop table {}".format(e)
        return "table dropped"
