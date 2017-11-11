# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Weijie Lin

import web
import hashlib
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
        i = web.input()
        with manager() as m:
            result = m.getUsers()
        return result


class register:

    def POST(self):
        i = web.input()
        with manager() as m:
            res = m.register(i.username, i.password)
        return res


class login:
    def GET(self):
        return "login get"

    def POST(self):
        i = web.input()
        with manager() as m:
            res = m.login(i.username, i.password)
        return res


class logout:
    def GET(self):
        return "logout get"

    def POST(self):
        return "logout post"

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
