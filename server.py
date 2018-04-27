#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import hashlib
import random
import os.path
import json
import time
import datetime
import re
from tornado.web import StaticFileHandler
from tornado.options import define, options

from conf import conf
from db import *

define("port", default=conf.sys_port, help="run on the given port", type=int)

def checkip(ip):  
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')  
    if p.match(ip):  
        return True  
    else:  
        return False 

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        name = self.get_secure_cookie("username")
        uid  = self.get_secure_cookie("userid")
        return name and uid

class IndexHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        coo = self.get_secure_cookie('userid')
        name= self.get_secure_cookie('username')
        if not coo or not name:
            self.render(conf.index_html)
        else:
            try:
                uid = coo.split('_')[1]
                u = query_admin(uid)
                if not u:
                    self.render(conf.index_html)
                else:
                    if u['role'] == 0:
                        self.redirect('/admin')
                    else:
                        self.redirect('/user')
            except:
                self.clear_cookie('userid')
                self.redirect('/')

    def post(self):
        mobile   = self.get_argument('name',     None)
        password = self.get_argument('password', None)
        d = {'code': -1, 'msg': '用户名或密码为空'}
        if not mobile or not password:
            pass
        else:
            d = {'code': -1, 'msg': '用户名或密码错误'}
            r = login_check(mobile, password)
            if r:
                d = {'code': 0, 'msg': 'ok', 'data': r}
                uid = r['id']
                key = 'userid_%s' % str(uid)
                self.set_secure_cookie('userid', key)
                self.set_secure_cookie('username', r['name'])
        d = json.dumps(d)
        self.write(d)


class AdminIndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = self.get_secure_cookie('username')
        D = list_admin()
        self.render(conf.root_index_html, D=D, name=name)

    @tornado.web.authenticated
    def post(self):
        limit = self.get_argument('limit', None)
        page  = self.get_argument('page',  None)
        next_ = self.get_argument('next',  None)
        D = list_admin(limit, page, next_)
        d = {'code': 0, 'msg': 'ok', 'data': D}
        d = json.dumps(d)
        self.write(d)

class CreateAdminHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        name    = self.get_argument('name',   None)
        mobile  = self.get_argument('mobile', None)
        password= self.get_argument('password', None)
        r = create_admin(name, mobile, password)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class DelAdminHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid = self.get_argument('uid', None)
        r = del_admin(uid)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class EditAdminHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid      = self.get_argument('uid', None)
        name     = self.get_argument('name', None)
        password = self.get_argument('password', None)
        mobile   = self.get_argument('mobile', None)
        r = edit_admin(uid, name, password, mobile)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class ForbiddenAdminHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid        = self.get_argument('uid', None)
        r = forbid_admin(uid)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class AllowAdminHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid        = self.get_argument('uid', None)
        r = allow_admin(uid)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = self.get_secure_cookie('username')
        D = list_user()
        self.render(conf.admin_index_html, D=D, name=name)

    @tornado.web.authenticated
    def post(self):
        limit = self.get_argument('limit', None)
        page  = self.get_argument('page',  None)
        next_ = self.get_argument('next',  None)
        D = list_user(limit, page, next_)
        d = {'code': 0, 'msg': 'ok', 'data': D}
        d = json.dumps(d)
        self.write(d)
        
class ForbiddenUserHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid        = self.get_argument('uid', None)
        opt        = self.get_argument('option', None)
        bc         = self.get_argument('msg', None)
        r = forbid_user(uid, opt, bc)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class AllowUserHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid        = self.get_argument('uid', None)
        opt        = self.get_argument('option', None)
        bc         = self.get_argument('msg', None)
        r = allow_user(uid, opt, bc)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class ChongZhiHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid        = self.get_argument('uid', None)
        num        = self.get_argument('num', None)
        r = chongzhi(uid, num)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class SearchAdmin(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid       = self.get_argument('uid', None)
        r = query_admin(uid)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class SearchUser(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        uid       = self.get_argument('uid', None)
        r = search_user(uid)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class SearchZhenghun(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        zid       = self.get_argument('zid', None)
        r = search_zhenghun(zid)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)


class SearchDating(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        did       = self.get_argument('did', None)
        r = search_dating(did)
        d = {'code': -1, 'msg': '参数错误'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class DatingIndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        D = list_dating()
        name = self.get_secure_cookie('username')
        self.render(conf.dating_html, D=D, name=name)

    @tornado.web.authenticated
    def post(self):
        limit = self.get_argument('limit', None)
        page  = self.get_argument('page',  None)
        next_ = self.get_argument('next',  None)
        D = list_dating(limit, page, next_)
        d = {'code': 0, 'msg': 'ok', 'data': D}
        d = json.dumps(d)
        self.write(d)
        
class ForbiddenDatingHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        did  = self.get_argument('did', None)
        opt  = self.get_argument('option', None)
        bc   = self.get_argument('buchong', None)
        r = forbit_dating(did, opt, bc)
        d = {'code': -1, 'msg': '参数不对'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)


class AllowDatingHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        did  = self.get_argument('did', None)
        opt  = self.get_argument('option', None)
        bc   = self.get_argument('buchong', None)
        r = allow_dating(did, opt, bc)
        d = {'code': -1, 'msg': '参数不对'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class DelDatingHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        did = self.get_argument('did', None)
        r = del_dating(did, opt, bc)
        d = {'code': -1, 'msg': '参数不对'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)


class ZhenghunIndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        D = list_zhenghun()
        name = self.get_secure_cookie('username')
        self.render(conf.zhenghun_html, D=D, name=name)

    @tornado.web.authenticated
    def post(self):
        limit = self.get_argument('limit', None)
        page  = self.get_argument('page',  None)
        next_ = self.get_argument('next',  None)
        D = list_zhenghun(limit, page, next_)
        d = {'code': 0, 'msg': 'ok', 'data': D}
        d = json.dumps(d)
        self.write(d)
        
class ForbiddenZhenghunHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        did  = self.get_argument('did', None)
        opt  = self.get_argument('option', None)
        bc   = self.get_argument('buchong', None)
        r = forbit_zhenghun(did, opt, bc)
        d = {'code': -1, 'msg': '参数不对'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)


class AllowZhenghunHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        did  = self.get_argument('did', None)
        opt  = self.get_argument('option', None)
        bc   = self.get_argument('buchong', None)
        r = allow_zhenghun(did, opt, bc)
        d = {'code': -1, 'msg': '参数不对'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class DelZhenghunHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        did = self.get_argument('did', None)
        r = del_zhenghun(did, opt, bc)
        d = {'code': -1, 'msg': '参数不对'}
        if r:
            d = {'code': 0, 'msg': 'ok'}
        d = json.dumps(d)
        self.write(d)

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('userid')
        self.redirect('/')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "adminsWbQLKos6GkHn/TQ9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/",
        "debug":True}
    handler = [
        (r"/static/(.*)", StaticFileHandler, {"path": "static"}),  
        (r"/css/(.*)", StaticFileHandler, {"path": "static/css"}),  
        (r"/js/(.*)", StaticFileHandler, {"path": "static/js"}),  
        (r"/img/(.*)", StaticFileHandler, {"path": "static/img"}), 
        ('/', IndexHandler),
        ('/admin', AdminIndexHandler),
        ('/userlist', UserHandler),
        ('/zhenghun', ZhenghunIndexHandler),
        ('/yuehui', DatingIndexHandler),
        ('/logout', LogoutHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
