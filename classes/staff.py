#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Staff class
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/04/21 10:11:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

from hashlib import md5

class Staff:

    table = 'staff'
 
    def __init__(self, MySql):

        self.mysql = MySql
    
    def add(self, sername, name, date, post, wage, email, phone, login, 
            password, status):
        
        sql = 'select count(*) from ' + self.table + ' where \
               login="' + login + '" and login<>""'
        
        if self.mysql.result(sql) == '1': return False
        
        sql = 'insert into ' + self.table + ' values(null, \
               "' + sername + '", "' + name + '", "' + date + '", \
               "' + post + '", "' + wage + '", "' + email + '", \
               "' + phone + '", "' + login + '", "' + password + '", \
               "' + status + '")'

        return self.mysql.query(sql)
        
    def checkLP(self, login, password):
        
        sql = 'select count(*) from ' + self.table + ' where \
               login="' + login + '" and password=md5(md5("' + password + '")) \
               and post<"6" and status="1"'
        
        if self.mysql.result(sql) == '1': return True
        return False
    
    def get(self, ID, ids = None):

        if ID == 1 and ids == None: sql = 'select * from ' + self.table + ''
        elif ids == None: sql = 'select * from ' + self.table + ' where id<>"1"'
        else: sql = 'select * from ' + self.table + ' where \
                     id="' + str(ids) + '"'
        
        return self.mysql.fetchRow(sql)
    
    def getArh(self):
    
        sql = 'select * from ' + self.table + ' where post="5"'
        
        return self.mysql.fetchRow(sql)
    
    def getOne(self, ids, field):
    
        if self.existsId(ids) == False: return False
                    
        sql = 'select ' + field + ' from ' + self.table + ' \
               where id="' + str(ids) +  '"'
        
        return self.mysql.result(sql)
    
    def existsId(self, ids):
        
        sql = 'select count(*) from ' + self.table + ' where \
               id="' + str(ids) + '"'
        
        if self.mysql.result(sql) == '1': return True
        return False
    
    def getStatus(self, value):
        
        if int(value) == 0: return 'Уволен'
        elif int(value) == 1: return 'Работает'
    
    def getPost(self, value):
        
        if int(value) == 0: return 'Администратор'
        elif int(value) == 1: return 'Руководство'
        elif int(value) == 2: return 'Менеджер'
        elif int(value) == 3: return 'Менеджер по персоналу'
        elif int(value) == 4: return 'Бухгалтер'
        elif int(value) == 5: return 'Архитектор'    
        elif int(value) == 6: return 'Прораб'
        elif int(value) == 7: return 'Строитель'
    
    def makeIn(self, model, value, ID = None):
    
        if value == None:
            for i in model:
                if int(i) == 1 or ids == ID: 
                    sql = 'delete from ' + self.table + ' where \
                           id=' + str(i) + ''
                    result = self.mysql.query(sql)
                    if result == False: return False
                
        elif value == 1:
            for i in model:
                sql = 'update ' + self.table + ' set status = 1 where \
                       id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False
        
        elif value == 2:
            for i in model:
                sql = 'update ' + self.table + ' set status = 0 where \
                       id=' + str(i) + ''
                result = self.mysql.query(sql)
                if result == False: return False
    
    def lastId(self):
        
        return self.mysql.lastId()
        
    def updateOne(self, ids, field, value):
        
        if self.existsId(ids) == False: return False    
            
        sql = 'update ' + self.table + ' set ' + field + '="' + value + '" \
               where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)

    def update(self, ids, sername, name, post, wage, email, phone, login, 
               password, status):
        
        if self.existsId(ids) == False: return False
        
        sql = 'select count(*) from ' + self.table + ' where \
               login="' + login + '" and ids<>"' + str(ids) +'"'
        
        if self.mysql.result(sql) == '1': return False
        
        sql = 'update ' + self.table + ' set sername="' + sername + '", \
               name="' + name + '", post="' + post + '", wage="' + wage + '", \
               email="' + email + '", phone="' + phone + '", \
               login="' + login + '", status="' + status + '" \
               where id="' + str(ids) + '"'

        if password != '':
            result = self.mysql.query(sql)
            if result == False: return False
            sql = 'update ' + self.table + ' set \
                   password="' + password + '" where id="' + str(ids) + '"'

        return self.mysql.query(sql)
    
    def delete(self, ids, ID):
        
        if self.existsId(ids) == False: return False
            
        if int(ids) == 1 or int(ids) == ID: return False
        
        sql = 'delete from ' + self.table + ' where id="' + str(ids) +  '"'
        
        return self.mysql.query(sql)
    
    def getId(self, login, password):
        
        sql = 'select id from ' + self.table + ' where \
               login="' + login + '" and password=md5(md5("' + password + '")) \
               and post<"6"'
        
        return self.mysql.result(sql)
    
    def getSessId(self, login, password):
        
        sql = 'select id from ' + self.table + ' where \
               login="' + login + '" and password="' + password + '" \
               and post<"6" and status="1"'
        
        return self.mysql.result(sql)
    
    def changePass(self, ids, password):
        
        password = md5(password)
        password = password.hexdigest()
        password = md5(password)
        password = password.hexdigest()
        
        sql = 'update ' + self.table + ' set password="' + password + '" \
               where id="' + str(ids) + '"'
               
        return self.mysql.query(sql)
