#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import hashlib
import json
import urllib
import urllib2

from conf import conf
from table import *
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import desc

def sendemail(uid=None, msg=None):
    if not uid or not msg:
        return None

    url = conf.email_url
    body_value = {"cuid": conf.admin_id,
                  "uid": uid,
                  "content": msg, 'kind': 1 }
    body_value  = urllib.urlencode(body_value)
    request = urllib2.Request(url=url, data=body_value)
    result = urllib2.urlopen(request)

def digest(word):
    m2 = hashlib.md5()
    line = '%s%s' % (word, conf.digest_salt)
    m2.update(line)
    token = m2.hexdigest()
    return token

def login_check(mobile=None, password=None, ip=None):
    if not mobile or not password:
        return None
    s = DBSession()
    tok = digest(password)
    c = and_(JlyAdmin.mobile == mobile, JlyAdmin.password==tok)
    r = s.query(JlyAdmin).filter(c).first()
    if r:
        r.last_login_ip = ip if ip else ''
        d = r.dic_return()
        s.commit()
        s.close()
        return d
    s.close()
    return None

def update_password(uid, old, new):
    tok_old = digest(old)
    s = DBSession()
    r = s.query(JlyAdmin).filter(JlyAdmin.id == uid).first()
    if not r:
        s.close()
        return False
    if r.password == tok_old:
        tok_new = digest(new)
        r.password = tok_new
        s.commit()
        s.close()
        return True
    s.close()
    return False

def get_role(cuid=None):
    if not cuid:
        return -1
    s = DBSession()
    r = s.query(JlyAdmin).filter(JlyAdmin.id == cuid).first()
    if r:
        s.close()
        return r.role
    s.close()
    return -1
def query_admin(cuid=None, uid=None):
    if not cuid or not uid:
        return None
    uid = int(uid)
    s = DBSession()
    if cuid != uid:
        ru = s.query(JlyAdmin).filter(JlyAdmin.id == cuid).first()
        if not ru:
            s.close()
            return None
    r = s.query(JlyAdmin).filter(JlyAdmin.id == uid).first()
    if not r:
        s.close()
        return None
    if ru.role <= r.role:
        s.close()
        D = r.dic_return()
        return D
    s.close()
    return None


def create_admin(uid=None, name=None, mobile=None, password=None):
    if not uid or not name or not mobile or not password:
        return None
    s = DBSession()
    ru = s.query(JlyAdmin).filter(JlyAdmin.id == uid).first()
    if not ru:
        s.close()
        return None
    if ru.role != 0:
        s.close()
        return None
    r = s.query(JlyAdmin).filter(JlyAdmin.mobile == mobile).first()
    if r:
        s.close()
        return None
    tok = digest(password)
    u = JlyAdmin(name=name, mobile=mobile, password=tok)
    s.add(u)
    s.commit()
    s.close()
    return True

def del_admin(cuid=None, uid=None):
    if not cuid or not uid:
        return None
    s = DBSession()
    rc = s.query(JlyAdmin).filter(JlyAdmin.id == cuid).first()
    if not rc or rc.role != 0:
        s.close()
        return None
    r = s.query(JlyAdmin).filter(JlyAdmin.id == uid).delete(synchronize_session=False)
    s.commit()
    s.close()
    return True
'''
cuid:  主动发起编辑者id
uid:   要被编辑的id
'''
def edit_admin(cuid=None, uid=None, name=None, password=None, mobile=None, state=None, msg=None, s=None):
    if not cuid or not uid or cuid==uid:
        return None
    f = True
    cuid, uid = int(cuid), int(uid)
    D = {}
    if name:
        D[JlyAdmin.name] = name
    if password:
        tok = digest(password)
        D[JlyAdmin.password] = tok
    if mobile:
        D[JlyAdmin.mobile] = mobile
    if not state and state != 0 and state != '':
        pass
    else:
        state = int(state)
        if state in [0, 1, 2, 3]:
            D[JlyAdmin.valid_state] = state
            D[JlyAdmin.msg] = msg if msg else ''
    if D:
        f = s
        if not f:
            s = DBSession()
        rc = s.query(JlyAdmin).filter(JlyAdmin.id == cuid).first()
        if not rc or rc.role != 0:
            if not f:
                s.close()
            return None

        s.query(JlyAdmin).filter(JlyAdmin.id == uid).update(D)
        s.commit()
    if not f:
        s.close()
    return True

def forbid_admin(cuid=None, uid=None, msg=None):
    if not cuid or not uid:
        return None
    cuid, uid = int(cuid), int(uid)
    msg = '禁止' if not msg else msg
    r = edit_admin(cuid=cuid, uid=uid, state=1, msg=msg)
    return r

def allow_admin(cuid=None, uid=None, msg=None):
    if not cuid or not uid:
        return None
    cuid, uid = int(cuid), int(uid)
    msg = '审核通过' if not msg else msg
    r = edit_admin(cuid=cuid, uid=uid, state=3, msg=msg)
    return r

def list_admin(limit=None, page=None, next_=None, kind=None):
    limit = int(limit) if limit else conf.admin_limit
    page  = int(page) if page else conf.admin_page
    next_ = int(next_) if next_ else 0
  
    if not kind:
        kind = 0
    elif int(kind) not in [0,1,2,3]:
        kind = 0
    else:
        kind = int(kind)
    s = DBSession()
    c = and_(True, JlyAdmin.role != 0)
    r = s.query(JlyAdmin).filter(c).filter(JlyAdmin.valid_state == kind).order_by(desc(JlyAdmin.regist_time)).limit(limit).offset(page*next_)
    D = [e.dic_return() for e in r]
    s.close()
    return {'page': page, 'limit':limit, 'next':next_, 'data': D}


def edit_user(uid=None, opt=None, bc=None, state=0):
    if not uid:
        return False
    if not state and state != 0 and state != '':
        return False
    msg = ''
    if opt == 0:
        msg = conf.reasons[0]
    elif opt and int(opt) in [0,1,2,3,4]:
        msg = conf.reasons[opt]
    elif bc:
        msg = bc[:128]
    s = DBSession()
    r = s.query(User).filter(User.id == uid).first()
    if not r:
        s.close()
        return False
    if not state:
        if state != 0 or state != '':
            s.close()
            return False
    state = int(state)
    if state in [0, 1, 3]:
        r.valid_state = state
        r.msg   = msg
        s.commit()
    s.close()
    return True 

def forbid_user(uid=None, opt=None, bc=None):
    r = edit_user(uid, opt, bc, 1)
    if opt:
        opt = int(opt)
    msg = conf.reasons[opt] if opt and opt in [0,1,2,3,4] else bc[:128]
    msg = '你被管理员禁止了,因为%s'%msg
    sendemail(uid, msg)
    return r

def allow_user(uid=None, opt=None, bc=None):
    msg = '正常'
    r = edit_user(uid, None, msg, 3)
    sendemail(uid, '你被管理员解禁了')
    return r

#num: rmb 分
def chongzhi(uid=None, num=None):
    if not uid or not num:
        return None
    s = DBSession()
    uid, num = int(uid), int(float(num)*100)
    num = int(num/10) if not conf.price else int(num/conf.price)
    ru = s.query(User).filter(User.id == uid).first()
    if ru:
        ra = s.query(User_account).filter(User_account.id == uid).first()
        if not ra:
            s.close()
            return None
        ra.num = ra.num + num
        s.commit()
        msg = '管理员已经为你充值%d示爱豆' % num
        sendemail(uid, msg)
    s.close()
    return True

def list_user(limit=None, page=None, next_=None, kind=None):
    limit = int(limit) if limit else conf.user_limit
    page  = int(page) if page else conf.user_page
    next_ = int(next_) if next_ else 0

    if not kind:
        kind = 0
    elif int(kind) not in [0,1,2,3]:
        kind = 0
    else:
        kind = int(kind)
    s = DBSession()
    r = s.query(User).filter(User.valid_state == kind).order_by(desc(User.regist_time)).limit(limit).offset(page*next_)
    ids = [e.id for e in r]
    a_m = {}
    if ids:
        ra = s.query(User_account).filter(User_account.id.in_(ids)).all()
        if ra:
            for e in ra:
                a_m[e.id] = e.dic_return()
    s.close()
    D = []
    for e in r:
        t = e.dic_return()
        a = a_m.get(e.id)
        t['num'] = 0 if not a else a.get('num', 0)
        t['free'] = 0 if not a else a.get('free', 0)
        D.append(t)
    return {'page':page, 'limit': limit, 'next': next_, 'data':D}

def list_zhenghun(limit=None, page=None, next_=None, kind=None):
    limit = int(limit) if limit else conf.zhenghun_limit
    page  = int(page) if page else conf.zhenghun_page
    next_ = int(next_) if next_ else 0

    if not kind:
        kind = 0
    elif int(kind) not in [0,1,2,3]:
        kind = 0
    else:
        kind = int(kind)
    s = DBSession()
    r = s.query(Zhenghun).filter(Zhenghun.valid_state == kind).order_by(desc(Zhenghun.time_)).limit(limit).offset(page*next_)
    ids = [e.userid for e in r]
    u_m = {}
    if ids:
        ru = s.query(User).filter(User.id.in_(ids)).all()
        if ru:
            for e in ru:
                u_m[e.id] = e.dic_return()
    D = []
    for e in r:
        t = e.dic_return()
        if u_m.get(e.userid):
            t['valid_state'] = u_m[e.userid]['valid_state']
        else:
            t['valid_state'] = -1
        D.append(t)
    s.close()
    return {'page':page, 'limit': limit, 'next': next_, 'data':D}
#kind=0 zhenghun  kind=1 dating
def edit_tiezi(oid=None, opt=None, bc=None, state=0, kind=0):
    if not oid:
        return False
    if not state and state != 0 and state != '':
        return False
    oid = int(oid)
    msg = ''
    if opt == 0:
        msg = conf.reasons[0]
    elif opt and int(opt) in [0,1,2,3,4]:
        msg = conf.reasons[opt]
    elif bc:
        msg = bc[:128]
    s = DBSession()
    r = ''
    if kind == 0:
        r = s.query(Zhenghun).filter(Zhenghun.id == oid).first()
    else:
        r = s.query(Dating).filter(Dating.id == oid).first()

    if not r:
        s.close()
        return None 
    state = int(state)
    if state in [0,1,2,3]:
        r.valid_state = state
        r.msg = msg
        s.commit()
    s.close()
    return True

def forbid_zhenghun(zid=None, opt=None, bc=None):
    r = edit_tiezi(zid, opt, bc, 1, 0)
    return r

def allow_zhenghun(oid=None, opt=None, bc=None):
    msg='通过'
    r = edit_tiezi(oid, None, msg, 3, 0)
    return r

def del_zhenghun(oid=None, opt=None, bc=None):
    msg = '删除'
    r = edit_tiezi(oid, None, msg, 2, 0)
    return r

def list_dating(limit=None, page=None, next_=None, kind=None):
    limit = int(limit) if limit else conf.dating_limit
    page  = int(page) if page else conf.dating_page
    next_ = int(next_) if next_ else 0

    if not kind:
        kind = 0
    elif int(kind) not in [0,1,2,3]:
        kind = 0
    else:
        kind = int(kind)

    s = DBSession()
    r = s.query(Dating).filter(Dating.valid_state == kind).order_by(desc(Dating.time_)).limit(limit).offset(page*next_)
    ids = [e.userid for e in r]
    u_m = {}
    if ids:
        ru = s.query(User).filter(User.id.in_(ids)).all()
        if ru:
            for e in ru:
                u_m[e.id] = e.dic_return()
    D = []
    for e in r:
        t = e.dic_return()
        if u_m.get(e.userid):
            t['user_valid_state'] = u_m[e.userid]['valid_state']
            t['nick_name'] = u_m[e.userid]['nick_name']
        else:
            t['user_valid_state'] = -1
            t['nick_name'] = ''
        D.append(t)
    s.close()
    return {'page':page, 'limit': limit, 'next': next_, 'data':D}

def forbit_dating(oid=None, opt=None, bc=None):
    r = edit_tiezi(oid, opt, bc, 1, 1)
    return r

def allow_dating(oid=None, opt=None, bc=None):
    msg = '通过'
    r = edit_tiezi(oid, None, msg, 3, 1)
    return r

def del_dating(oid=None, opt=None, bc=None):
    msg = '删除'
    r = edit_tiezi(oid, None, msg, 2, 1)
    return r

def search_user(uid=None):
    if not uid:
        return None
    uid = int(uid)
    s = DBSession()
    r = s.query(User).filter(User.id == uid).first()
    ra = s.query(User_account).filter(User_account.id == uid).first()
    D = r.dic_return() if r else {}
    if ra:
        D['num'] = ra.num
        D['free'] = ra.free
    s.close()
    return D

def search_zhenghun(zid=None):
    if not zid:
        return None
    s = DBSession()
    r = s.query(Zhenghun).filter(Zhenghun.id == zid).first()
    if not r:
        s.close()
        return None
    uid = r.userid
    ru = s.query(User).filter(User.id == uid).first()
    v_d = -1
    username = ''
    if ru:
        v_d = ru.valid_state
        username = ru.nick_name
    d = r.dic_return()
    d['user_valid_state'] = v_d
    d['user_name'] = username
    s.close()
    return d

def search_dating(did=None):
    if not did:
        return None
    s = DBSession()
    r = s.query(Dating).filter(Dating.id == did).first()
    if not r:
        s.close()
        return None
    uid = r.userid
    ru = s.query(User).filter(User.id == uid).first()
    v_d = 0
    name = ''
    if ru:
        v_d = ru.valid_state
        name = ru.nick_name
    d = r.dic_return()
    d['user_valid_state'] = v_d
    d['nick_name'] = name
    s.close()
    return d


if __name__ == '__main__':
    r = edit_tiezi(12, None, '通过', state=3, kind=0)
    print(r)
