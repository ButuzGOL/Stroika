#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Customer class
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/03/21 23:32:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

class Customer:

    table  = 'customers'
    table1 = 'projects'

    def __init__(self, MySql):

        self.mysql = MySql
        
    def add(self, sername, name, company, email, phone):
        
        sql = 'insert into ' + self.table + ' values(null, "' + sername + '", \
               "' + name + '", "' + company + '", "' + email + '", \
               "' + phone + '")' 
        
        return self.mysql.query(sql)
        
    def get(self, ids = None):
        
        if ids == None: sql = 'select * from ' + self.table + ''
        else: sql = 'select * from ' + self.table + ' \
                     where id="' + str(ids) + '"' 
        
        return self.mysql.fetchRow(sql)
    
    def updateOne(self, ids, field, value):
        
        if self.existsId(ids) == False: return False    
            
        sql = 'update ' + self.table + ' set ' + field + '="' + value + '" \
               where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
    
    def delete(self, ids):
        
        if self.existsId(ids) == False: return False
            
        sql = 'delete from ' + self.table + ' where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
        
    def lastId(self):
        
        return self.mysql.lastId()
    
    def makeIn(self, model):
    
        for i in model:
            sql = 'delete from ' + self.table + ' where id=' + str(i) + ''
            result = self.mysql.query(sql)
            if result == False: return False

    def update(self, ids, sername, name, company, email, phone):
        
        if self.existsId(ids) == False: return False
        
        sql = 'update ' + self.table + ' set sername="' + sername + '", \
               name="' + name + '", company="' + company + '", \
               email="' + email + '", phone="' + phone + '"    \
               where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
    
    def existsId(self, ids):
        
        sql = 'select count(*) from ' + self.table + ' \
               where id="' + str(ids) + '"'
        
        if self.mysql.result(sql) == '1': return True
        return False
    
    def getOne(self, ids, field):
    
        if self.existsId(ids) == False: return False
                    
        sql = 'select ' + field + ' from ' + self.table + ' \
               where id="' + str(ids) +  '"'
        
        return self.mysql.result(sql)
        
    def getCountPro(self, ids, status = '0'):
        
        sql = 'select count(*) from ' + self.table1 + ' where \
               id_customer="' + str(ids) + '" and status="' + str(status) + '"' 
        
        return self.mysql.result(sql)
