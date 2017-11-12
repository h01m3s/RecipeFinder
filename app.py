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
    '/drop', 'drop',
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
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'True')
        data = web.data()
        print "data from get {}".format(data)
        return "data"

    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'True')
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
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
        web.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        web.header("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
        data = web.data()
        print "data from options {}".format(data)
        return data


class login:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'True')
        data = json.loads(web.data())
        username = data['username']
        password = data['password']
        with manager() as m:
            result = m.login(username, password)
        return result



class logout:
    def GET(self):
        web.seeother('/')

    def POST(self):
        web.seeother('/')

class drop:
    def GET(self):
        m = manager()
        return m.dropTable()


if __name__ == "__main__":
    app = web.application(urls, globals())
    # web.config.session_parameters['cookie_name'] = 'recipeFinder'
    # web.config.session_parameters['cookie_domain'] = None
    # # 86400 / 24 hrs
    # web.config.session_parameters['timeout'] = 86400
    # web.config.session_parameters['ignore_change_ip'] = True
    # web.config.session_parameters['secret_key'] = 'hwgWKydq4J2H'
    # web.config.session_parameters['expired_message'] = 'Session expired'
    # session = web.session.Session(app, web.session.DiskStore('data/sessions'), initializer={'login': False})
    # def session_hook():
    #     web.ctx.session = session
    # app.add_processor(web.loadhook(session_hook))
    app.run()
