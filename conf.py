#-*- coding: utf-8 -*-
import ConfigParser

class Picconf():
    def __init__(self, name):
        p = ConfigParser.ConfigParser()
        p.read(name)
        self.sys_ip      = p.get('sys', 'sys_ip')
        self.sys_port    = p.getint('sys', 'sys_port')
        self.email_url   = p.get('sys', 'email_url')
        self.admin_id    = p.get('sys', 'admin_id')

        self.digest_salt = p.get('salt', 'digest_salt')

        self.table_jly_admin = p.get('table', 'jly_admin')
        self.table_user      = p.get('table', 'table_user')
        self.table_dating       = p.get('table', 'table_dating')
        self.table_zhenghun     = p.get('table', 'table_zhenghun')
        self.table_user_account = p.get('table', 'table_user_account')
        self.table_email        = p.get('table', 'table_email')

        self.admin_page        = p.getint('offset', 'admin_page')
        self.admin_limit       = p.getint('offset', 'admin_limit')
        self.user_page         = p.getint('offset', 'user_page')
        self.user_limit        = p.getint('offset', 'user_limit')
        self.zhenghun_page     = p.getint('offset', 'zhenghun_page')
        self.zhenghun_limit    = p.getint('offset', 'zhenghun_limit')
        self.dating_page       = p.getint('offset', 'dating_page')
        self.dating_limit      = p.getint('offset', 'dating_limit')

        self.mysql_user      = p.get('mysql', 'mysql_user')
        self.mysql_password  = p.get('mysql', 'mysql_password')
        self.mysql_host      = p.get('mysql', 'mysql_host')
        self.mysql_port      = p.getint('mysql', 'mysql_port')
        self.mysql_db        = p.get('mysql', 'mysql_db')
        self.mysql_encode    = p.get('mysql', 'mysql_encode')

        self.reason1     = p.get('reason', 'reason1')
        self.reason2     = p.get('reason', 'reason2')
        self.reason3     = p.get('reason', 'reason3')
        self.reason4     = p.get('reason', 'reason4')
        self.reason5     = p.get('reason', 'reason5')
        self.reasons     = [self.reason1, self.reason2,self.reason3,
                            self.reason4, self.reason5]

        self.index_html  = p.get('html', 'index_html')
        self.root_index_html = p.get('html', 'root_index_html')
        self.admin_index_html= p.get('html', 'admin_index_html')
        self.admin_html  = p.get('html', 'admin_html')
        self.user_html   = p.get('html', 'user_html')
        self.zhenghun_html = p.get('html', 'zhenghun_html')
        self.dating_html = p.get('html', 'dating_html')

        self.price       = p.getint('price', 'price')

    def dis(self):
        print(self.sys_port)
        for e in self.reasons:
            print(e)

conf    = Picconf('./conf.txt')

if __name__ == "__main__":
    conf.dis()
