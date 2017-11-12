# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Weijie Lin

import web
import hashlib
import json
from dataManager import *

urls = (
    '/', 'index',
    '/register', 'register',
    '/login', 'login',
    '/logout', 'logout',
    '/updatebookmark', 'updateBookmark',
    '/getbookmark', 'getBookmark',
    '/reset', 'reset'
    )

web.config.debug = False


class index:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'True')
        i = web.input()
        with manager() as m:
            result = m.getUsers()
        return result


class register:
    def GET(self):
        return "post method only"

    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'True')
        # web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
        data = json.loads(web.data())
        username = data['username']
        password = data['password']
        with manager() as m:
            result = m.register(username, password)
        return result

    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'True')
        # web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
        data = web.data()
        print "data from options {}".format(data)
        return data


class login:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'True')
        # data = json.loads(web.data())
        # username = data['username']
        # password = data['password']
        try:
            i = web.input()
            username = i.username
            password = i.password
            with manager() as m:
                result = m.login(username, password)
        except Exception as e:
            return "Wrong parameter: {}".format(e)
        return result

    def POST(self):
        return "get method only"


class updateBookmark:
    def GET(self):
        return "post method only"

    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'True')
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
        data = json.loads(web.data())
        username = data['username']
        uri = data['uri']
        with manager() as m:
            result = m.addBookmark(username, uri)
        return result

    # def OPTIONS(self):
    #     web.header('Access-Control-Allow-Origin', '*')
    #     web.header('Access-Control-Allow-Credentials', 'True')
    #     web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
    #     web.header("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
    #     data = web.data()
    #     print "data from options {}".format(data)
    #     return data


class getBookmark:
    def GET(self):
        i = web.input()
        username = i.username
        with manager() as m:
            result = m.getBookmark(username)
        return result

    def POST(self):
        return "post method only"

class logout:
    def GET(self):
        web.seeother('/')

    def POST(self):
        web.seeother('/')

class drop:
    def GET(self):
        with manager() as m:
            results = m.dropTable
        return results


class reset:
    def GET(self):
        with manager() as m:
            m.dropTable()
            m.__init__()
        return "reset"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
