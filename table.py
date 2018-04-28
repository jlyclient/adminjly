#-*- coding: utf8 -*-

import time

from sqlalchemy import Column, String, Integer, Date, TIMESTAMP, create_engine
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from conf import conf

mysql_url = 'mysql+mysqlconnector://' + str(conf.mysql_user) + ':%s@%s:'%(conf.mysql_password, conf.mysql_host) + str(conf.mysql_port) + '/' + conf.mysql_db

engine = create_engine(mysql_url, encoding=conf.mysql_encode)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
Base = declarative_base()
###########################################

class JlyAdmin(Base):
    __tablename__ = conf.table_jly_admin
    def __init__(self, id_=0, name='', password='', mobile='',\
                 sex=1, role=1, regist_time='', last_login='',\
                 last_login_ip='', valid_state=0, msg='正常'):
        self.id   = id_
        self.name = name
        self.password = password
        self.mobile = mobile
        self.sex  = sex
        self.role = 1#0=root  1=admin
        self.last_login = last_login
        self.last_login_ip = last_login_ip
        self.valid_state = valid_state
        self.msg  = msg
        t = time.localtime()
        now = time.strftime('%Y-%m-%d %H:%M:%S', t)
        if not regist_time:
            self.regist_time = now
        else:
            self.regist_time = regist_time
        if not last_login:
            self.last_login = now
        else:
            self.last_login = now
    id            = Column(Integer, primary_key=True)
    name          = Column(String(16))
    password      = Column(String(64))
    mobile        = Column(String(16))
    sex           = Column(Integer)
    role          = Column(Integer)
    regist_time   = Column(TIMESTAMP)
    last_login    = Column(TIMESTAMP)
    last_login_ip = Column(String(16))
    valid_state   = Column(Integer)
    msg           = Column(String(128))
    def dic_return(self):
        return {'id': self.id, 'name': self.name, 'password': self.password,
                'mobile': self.mobile, 'sex': self.sex, 'role': self.role,
                'regist_time': str(self.regist_time),
                'last_login': str(self.last_login),
                'last_login_ip':self.last_login_ip,
                'msg': self.msg, 'valid_state':self.valid_state}
###########################################
class User(Base):
    __tablename__ = conf.table_user

    def __init__(self, id_=0, name='', password='', mobile='',
            sex=0, aim=0, age=18,\
            m=0, xz=0, sx=0, blood=0, salary=0, wt=50, ht=160, de=0, \
            na=1, cl1='', cl2='', ori1='', ori2='', st=0,
            t=None, last_t='', last_ip='', openid1='', openid2='', unionid='', v_st=0, msg=''):
        self.id       = id_
        if len(name) == 0 and mobile:
            name = '新用户%s' % self.mobile[-4:]
        self.nick_name= name
        self.password = password
        self.mobile   = mobile
        self.sex      = sex
        self.aim      = aim
        self.age      = age
        self.marriage = m
        self.xingzuo  = xz
        self.shengxiao= sx
        self.blood    = blood
        self.salary   = salary
        self.weight   = wt
        self.height   = ht
        self.degree   = de
        self.nation   = na
        self.curr_loc1= cl1
        self.curr_loc2= cl2
        self.ori_loc1 = ori1
        self.ori_loc2 = ori2
        self.state    = st
        self.last_login_ip = last_ip
        self.openid1  = openid1
        self.openid2  = openid2
        if not t:
            t       = time.localtime()
            now     = time.strftime('%Y-%m-%d %H:%M:%S', t)
            self.regist_time = now
        else:
            self.regist_time = t
        if not last_t:
            t       = time.localtime()
            now     = time.strftime('%Y-%m-%d %H:%M:%S', t)
            self.last_login  = now
        else:
            self.last_login = last_t
        self.unionid     = unionid
        self.valid_state = v_st
        self.msg         = msg

    id                = Column(Integer, primary_key=True)
    nick_name         = Column(String(16))
    password          = Column(String(32))
    mobile            = Column(String(16))
    sex               = Column(Integer)
    aim               = Column(Integer)
    age               = Column(Integer)
    marriage          = Column(Integer) 
    xingzuo           = Column(Integer)
    shengxiao         = Column(Integer)
    blood             = Column(Integer)
    salary            = Column(Integer)
    weight            = Column(Integer)
    height            = Column(Integer)
    degree            = Column(Integer)
    nation            = Column(Integer)
    curr_loc1         = Column(String(8))
    curr_loc2         = Column(String(8))
    ori_loc1          = Column(String(8))
    ori_loc2          = Column(String(8))
    state             = Column(Integer)
    regist_time       = Column(TIMESTAMP)
    last_login        = Column(TIMESTAMP)
    last_login_ip     = Column(String(24))
    openid1           = Column(String(32))
    openid2           = Column(String(32))
    unionid           = Column(String(32))
    valid_state       = Column(Integer)
    msg               = Column(String(32))

    def dic_return(self):
        return { 'id':       self.id,          'nick_name': self.nick_name, 
                 'mobile':    self.mobile,     'last_login': str(self.last_login),
                 'sex':       self.sex,
                 'aim':      self.aim,         'age':       self.age,
                 'marriage': self.marriage,    'xingzuo':   self.xingzuo,
                 'shengxiao':self.shengxiao,   'blood':     self.blood,
                 'salary':   self.salary,
                 'weight':   self.weight,      'height':    self.height,
                 'degree':   self.degree,      'nation':    self.nation,
                 'curr_loc1':self.curr_loc1,   'curr_loc2': self.curr_loc2, 
                 'ori_loc1': self.ori_loc1,    'ori_loc2':  self.ori_loc2,
                 'state':    self.state,       'unionid':self.unionid,
                 'regist_time': str(self.regist_time), 'msg': self.msg,
                 'valid_state': self.valid_state, 'last_login_ip':self.last_login_ip, 
                 'openid1': self.openid1, 'openid2': self.openid2}
    def dic_return2(self):
        return { 'id':       self.id,          'nick_name': self.nick_name,
                 'sex':      self.sex,         'age':       self.age,
                 'height':   self.height,      'degree':    self.degree,
                 'valid_state': self.valid_state, 'msg': self.msg}

###########################################

class Dating(Base):
    __tablename__ = conf.table_dating
    def __init__(self, id_=0, name='', uid=0, age=18, sex=0, sjt=6, dt=None,\
                 loc1='', loc2='', locd='', obj=2, num=1, fee=0,\
                 bc='', valid_time=1, t_=None, v_st=0, msg=''):
        self.id       = id_
        self.nick_name= name
        self.userid   = uid
        self.age      = age
        self.sex      = sex
        self.subject  = sjt
        self.loc1     = loc1
        self.loc2     = loc2
        self.loc_detail = locd
        self.object1    = obj
        self.numbers    = num
        self.fee        = fee
        self.buchong    = bc
        self.valid_time = valid_time
        self.valid_state= v_st
        self.msg        = msg
        self.scan_count = 0
        if not t_:
            t_    = time.localtime()
            now  = time.strftime('%Y-%m-%d %H:%M:%S', t_)
            self.time_ = now
        else:
            self.time_ = t_
        if not dt:
            t      = time.time() + 3600*3
            t      = time.strftime('%Y-%m-%d %H:%M:%S', t)
            self.dtime = t
        else:
            self.dtime = dt
    id           = Column(Integer, primary_key=True)
    userid       = Column(Integer)
    nick_name    = Column(String(16))
    age          = Column(Integer)
    sex          = Column(Integer)
    subject      = Column(Integer)
    dtime        = Column(TIMESTAMP)
    loc1         = Column(String(8))
    loc2         = Column(String(8))
    loc_detail   = Column(String(64))
    object1      = Column(Integer)
    numbers      = Column(Integer)
    fee          = Column(Integer)
    buchong      = Column(String(160))
    valid_time   = Column(Integer)
    time_        = Column(TIMESTAMP)
    scan_count   = Column(Integer)
    valid_state  = Column(Integer)
    msg          = Column(String(32))
    def dic_return(self):
        t = str(self.time_)
        t = t.replace('-', '/')
        dt = str(self.dtime)
        dt = dt.replace('-', '/')
        return {'id': self.id,   'uid': self.userid, 'age': self.age, 
                'sex': self.sex, 'scan_count': self.scan_count,
                'subject': self.subject, 'dtime': dt,
                'loc1': self.loc1, 'loc2': self.loc2,
                'loc_detail': self.loc_detail, 'object': self.object1,
                'numbers': self.numbers, 'fee': self.fee,
                'buchong': self.buchong, 'valid_time': self.valid_time,
                'valid_state': self.valid_state, 'msg': self.msg,
                'time': t, 'nick_name': self.nick_name}

#################################################################

class Zhenghun(Base):
    __tablename__ = conf.table_zhenghun
    def __init__(self, id_=0, uid=0, name='', age=18, sex=0, loc1='',loc2='',\
                 t=None, v_d=1, title='', cnt='', obj1=0, v_st=0, msg=''):
        self.id       = id_
        self.userid   = uid
        self.nick_name= name
        self.age      = age
        self.sex      = sex
        self.loc1     = loc1
        self.loc2     = loc2
        self.valid_day= v_d
        self.title    = title
        self.content  = cnt
        self.object1  = obj1
        self.scan_count = 0
        self.valid_state = v_st
        self.msg      = msg
        if not t:
            t    = time.localtime()
            now  = time.strftime('%Y-%m-%d %H:%M:%S', t)
            self.time_ = now
        else:
            self.time_ = t
    id            = Column(Integer, primary_key=True)
    userid        = Column(Integer)
    nick_name     = Column(String(16))
    age           = Column(Integer)
    sex           = Column(Integer)
    loc1          = Column(String(8))
    loc2          = Column(String(8))
    time_         = Column(TIMESTAMP)
    valid_day     = Column(Integer)
    title         = Column(String(64))
    content       = Column(String(800))
    object1       = Column(Integer)
    scan_count    = Column(Integer)
    valid_state   = Column(Integer)
    msg           = Column(String(32))
    def dic_return(self):
        return {'id': self.id,      'uid': self.userid,
                'age': self.age,    'sex': self.sex,
                'loc1': self.loc1,  'loc2': self.loc2,
                'valid_day': self.valid_day,  'title': self.title,
                'content': self.content,  'object': self.object1,
                'scan_count': self.scan_count, 
                'valid_state': self.valid_state, 'msg': self.msg,
                'time': str(self.time_), 'nick_name': self.nick_name}

#################################################################
class User_account(Base):
    __tablename__ = conf.table_user_account
    def __init__(self, id_=0, num=0, f=0):
        self.id     = id_
        self.num    = num
        self.free   = f
    id           = Column(Integer, primary_key=True)
    num          = Column(Integer)
    free         = Column(Integer)
    def dic_return(self):
        return {'id': self.id,   'num': self.num, 'free': self.free}
#################################################################

__all__=['DBSession', 'JlyAdmin', 'User', 'Dating', 'User_account', 'Zhenghun']

