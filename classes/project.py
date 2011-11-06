#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Project class
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/04/02 22:13:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

class Project:

    table  = 'projects'
    table1 = 'projprog'

    def __init__(self, MySql):

        self.mysql = MySql

    def add(self, name, info, dates, datee, status, id_customer, id_staff):
        
        sql = 'insert into ' + self.table + ' values(null, \
               "' + name + '", "' + info + '", "' + dates + '", \
               "' + datee + '", "' + status + '", "' + id_customer + '", \
               "' + id_staff + '")'
        
        result = self.mysql.query(sql)
        if result == False: return False
        
        id_project = self.lastId()
        
        sql = 'insert into ' + self.table1 + ' values(null, \
               "' + str(id_project) + '", "")'
        
        result = self.mysql.query(sql)
        if result == False: return False
        
        return id_project
        
    def get(self, ids = None, id_staff = None):
    
        if ids == None and id_staff == None: sql = 'select * \
                                                    from ' + self.table + ''
        elif ids != None: sql = 'select * from ' + self.table + ' where \
                                  id="' + str(ids) + '"'
        elif id_staff != None: sql = 'select * from ' + self.table + ' where \
                                       id_staff="' + str(id_staff) + '"'
        
        return self.mysql.fetchRow(sql)
    
    def updateOne(self, ids, field, value):
        
        if self.existsId(ids) == False: return False    
        
        sql = 'update ' + self.table + ' set ' + field + '="' + value + '" \
               where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
    
    def lastId(self):
        
        return self.mysql.lastId()
    
    def makeIn(self, model, value = 0):
    
        if value == 0:
            for i in model:
                sql = 'delete from ' + self.table + ' where id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False
                
                sql = 'delete from ' + self.table1 + ' where \
                       id_project=' + str(i) + ''
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
            
    def update(self, ids, name, info, datee, status, id_customer, id_personal):
        
        if self.existsId(ids) == False: return False
        
        sql = 'update ' + self.table + ' set name="' + name + '", \
               info="' + info + '", \
               datee="' + datee + '", status="' + status + '", \
               id_customer="' + id_customer + '", \
               id_staff="' + id_personal + '" where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
    
    def existsId(self, ids):
        
        sql = 'select count(*) from ' + self.table + ' where \
               id="' + str(ids) + '"'
        
        if self.mysql.result(sql) == '1': return True
        return False
    
    def getOne(self, ids, field):
    
        if self.existsId(ids) == False: return False
                        
        sql = 'select ' + field + ' from ' + self.table + ' \
               where id="' + str(ids) + '"'
        
        return self.mysql.result(sql)
    
    def getStatus(self, value):
        
        if int(value) == 0: return 'В процессе'
        elif int(value) == 1: return 'Выполнен'
    
    def getProjprogInfo(self, id_project):
    
        sql = 'select info from ' + self.table1 + ' where \
               id_project="' + str(id_project) + '"'
        
        return self.mysql.fetchRow(sql)[0][0]
    
    def updateProjprogInfo(self, id_project, info):
        
        if self.existsId(id_project) == False: return False
        
        sql = 'update ' + self.table1 + ' set info="' + info + '" \
               where id_project="' + str(id_project) +  '"'
        
        return self.mysql.query(sql)
    
    def delete(self, ids):
        
        if self.existsId(ids) == False: return False
            
        sql = 'delete from ' + self.table + ' where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
