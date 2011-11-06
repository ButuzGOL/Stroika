#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Accountancy class
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/03/21 23:32:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

class Accountancy:

    table  = 'accountancy_wage'
    table1 = 'accountancy_pay'
    
    def __init__(self, MySql):

        self.mysql = MySql
        
    def wageAdd(self, date, id_staff, money, status):
        
        sql = 'insert into ' + self.table + ' values(null, "' + date + '", \
               "' + id_staff + '", "' + money + '", "' + status + '")'

        return self.mysql.query(sql)
        
    def wageGet(self, ids = None):
        
        if ids == None: sql = 'select * from ' + self.table + ''
        else: sql = 'select * from ' + self.table + ' \
                     where id="' + str(ids) + '"' 
        
        return self.mysql.fetchRow(sql)
    
    def LastId(self):
        
        return self.mysql.lastId()
    
    def wageMakeIn(self, model, value = 0):
    
        if value == 0:
            for i in model:
                sql = 'delete from ' + self.table + ' where id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False

        elif value == 1:
            for i in model:
                sql = 'update ' + self.table + ' set status = 1 \
                       where id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False

        elif value == 2:
            for i in model:
                sql = 'update ' + self.table + ' set status = 0 \
                       where id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False
    
    def wageGetStatus(self, value):
        
        if int(value) == 0: return 'Не выдана'
        elif int(value) == 1: return 'Выдана'
    
    def wageExistsId(self, ids):
        
        sql = 'select count(*) from ' + self.table + ' \
               where id="' + str(ids) + '"'
        
        if self.mysql.result(sql) == '1': return True
        return False
    
    def wageGetOne(self, ids, field):
    
        if self.wageExistsId(ids) == False: return False
                    
        sql = 'select ' + field + ' from ' + self.table + ' \
               where id="' + str(ids) +  '"'
        
        return self.mysql.result(sql)        
    
    def wageUpdate(self, ids, date, id_staff, money, status):
        
        if self.wageExistsId(ids) == False: return False
        
        sql = 'update ' + self.table + ' set date="' + date + '", \
               id_staff="' + id_staff + '", \
               money="' + money + '", status="' + status + '" \
               where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
    
    def wageDelete(self, ids):
        
        if self.wageExistsId(ids) == False: return False
            
        sql = 'delete from ' + self.table + ' where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
    
    def payAdd(self, date, id_project, money, status):
        
        sql = 'insert into ' + self.table1 + ' values(null, "' + date + '", \
               "' + id_project + '", "' + money + '", "' + status + '")'

        return self.mysql.query(sql)
        
    def payGet(self, ids = None):
        
        if ids == None: sql = 'select * from ' + self.table1 + ''
        else: sql = 'select * from ' + self.table1 + ' \
                     where id="' + str(ids) + '"' 
        
        return self.mysql.fetchRow(sql)
    
    def payMakeIn(self, model, value = 0):
    
        if value == 0:
            for i in model:
                sql = 'delete from ' + self.table1 + ' where id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False

        elif value == 1:
            for i in model:
                sql = 'update ' + self.table1 + ' set status = 1 \
                       where id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False

        elif value == 2:
            for i in model:
                sql = 'update ' + self.table1 + ' set status = 0 \
                       where id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False
    
    def payGetStatus(self, value):
        
        if int(value) == 0: return 'Не оплачен'
        elif int(value) == 1: return 'Оплачен'
    
    def payExistsId(self, ids):
        
        sql = 'select count(*) from ' + self.table1 + ' \
               where id="' + str(ids) + '"'
        
        if self.mysql.result(sql) == '1': return True
        return False
    
    def payGetOne(self, ids, field):
    
        if self.payExistsId(ids) == False: return False
                    
        sql = 'select ' + field + ' from ' + self.table1 + ' \
               where id="' + str(ids) +  '"'
        
        return self.mysql.result(sql)        
    
    def payUpdate(self, ids, date, id_project, money, status):
        
        if self.payExistsId(ids) == False: return False
        
        sql = 'update ' + self.table1 + ' set date="' + date + '", \
               id_project="' + id_project + '", \
               money="' + money + '", status="' + status + '" \
               where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
    
    def payDelete(self, ids):
        
        if self.payExistsId(ids) == False: return False
            
        sql = 'delete from ' + self.table1 + ' where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
