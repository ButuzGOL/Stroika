#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MySql class it make work easy
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/04/21 07:13:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

from xml.dom import minidom

import sys

import _mysql

class MySql:
    
    conn = None
        
    def __init__(self):
        
        try:
            self.getConfig()
            self.conn = _mysql.connect(host = self.host, port = self.port,
                                       user = self.user, passwd = self.passwd, 
                                       db = self.db)
        except: pass
                         
    def online(self):
    
        if not self.conn: return False
        else: return True
                        
    def query(self, sql):
        
        try:
            self.conn.query(sql)
            return True
        except: return False
        
    def result(self, sql):
        
        q = self.query(sql)
        try:
            use_result = self.conn.use_result()
            fetch_row = use_result.fetch_row()
            return fetch_row[0][0]
        except: return False
    
    def fetchRow(self, sql):
        
        q = self.query(sql)
        try:
            use_result = self.conn.use_result()
            
            fetch_array = []
            while True:
                res = use_result.fetch_row()
                if not res: break
                fetch_array.append(res[0])
                                
            return fetch_array
        except: return False
    
    def lastId(self):
        
        try:
            return self.conn.insert_id()
        except: return False

    def getConfig(self):
        
        dom = minidom.parse(sys.path[0] + '/config.xml')

        a = dom.getElementsByTagName('MySQLConf')
        for b in a: 
            self.host   = \
                    b.getElementsByTagName('host')[0].firstChild.data.strip()
            self.port   = \
                int(b.getElementsByTagName('port')[0].firstChild.data.strip())
            self.user   = \
                    b.getElementsByTagName('user')[0].firstChild.data.strip()
            self.passwd = \
                    b.getElementsByTagName('passwd')[0].firstChild.data.strip()
            self.db     = \
                    b.getElementsByTagName('db')[0].firstChild.data.strip()
            
