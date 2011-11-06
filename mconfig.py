#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Make config
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/05/07 08:43:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

import pygtk
pygtk.require('2.0')
import gtk

import gtk.glade
import os
import pango
import datetime
import time
import gobject

from xml.dom import minidom
from hashlib import md5

class MakeConfig:

    def __init__(self):

        path = os.path.join(os.path.dirname(__file__), 'mconfig.glade')
        glade_xml = gtk.glade.XML(path)
        self.window = glade_xml.get_widget('window1')
        self.window.connect('destroy', lambda l: gtk.main_quit())
        
        title = glade_xml.get_widget('title')
        title.modify_font(pango.FontDescription('Monospace Bold 20'))
        mysql = glade_xml.get_widget('mysql')
        mysql.modify_font(pango.FontDescription('Monospace Bold 15'))
        admin = glade_xml.get_widget('admin')
        admin.modify_font(pango.FontDescription('Monospace Bold 15'))
        
        self.db_server = glade_xml.get_widget('db_server')
        self.db_port   = glade_xml.get_widget('db_port')
        self.db_name   = glade_xml.get_widget('db_name')
        self.db_user   = glade_xml.get_widget('db_user')
        self.db_pass   = glade_xml.get_widget('db_pass')
        
        self.user_name = glade_xml.get_widget('user_name')
        self.user_pass = glade_xml.get_widget('user_pass')
        
        self.message = glade_xml.get_widget('message')
        self.message.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#e12e2e'))
        
        button_ok     = glade_xml.get_widget('button_ok')
        button_ok.connect('clicked', self.makeConfig)
        button_quit = glade_xml.get_widget('button_quit')
        button_quit.connect('clicked', lambda l: gtk.main_quit())
        
        self.checkbutton_serv = glade_xml.get_widget('checkbutton_serv')
        self.checkbutton_serv.connect('toggled', self.isServer)
        
        self.window.show()
        
        gtk.main()
    
    def messageClear(self):
    
        self.message.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#e12e2e'))
        self.message.set_text('')
    
    def isServer(self, widget):
        
        self.user_name.set_sensitive(widget.get_active())
        self.user_pass.set_sensitive(widget.get_active())
    
    def makeConfig(self, *args):
        
        host   = self.db_server.get_text()
        port   = self.db_port.get_text()
        user   = self.db_user.get_text()
        passwd = self.db_pass.get_text()
        db     = self.db_name.get_text()
        
        if host == '' or port == '' or db == '':
            self.message.set_text('Ошибка поля не заполнены')
            gobject.timeout_add(10000, self.messageClear)
            return
        
        dom = minidom.Document()
        e1 = dom.createElement('MySQLConf')
        dom.appendChild(e1)

        p1 = dom.createElement('host')
        p1.appendChild(dom.createTextNode(host))
        e1.appendChild(p1)

        p2 = dom.createElement('port')
        p2.appendChild(dom.createTextNode(port))
        e1.appendChild(p2)

        p3 = dom.createElement('user')
        p3.appendChild(dom.createTextNode(user))
        e1.appendChild(p3)

        p4 = dom.createElement('passwd')
        p4.appendChild(dom.createTextNode(passwd))
        e1.appendChild(p4)

        p5 = dom.createElement('db')
        p5.appendChild(dom.createTextNode(db))
        e1.appendChild(p5)
        
        try:
            f = open(os.path.dirname(__file__) + '/config.xml', 'wb')
            dom.writexml(f, '', '    ', '\n', 'UTF-8')
            f.close()
        except:
            self.message.set_text('Ошибка создания config файла')
            gobject.timeout_add(10000, self.messageClear)
        
        if self.checkbutton_serv.get_active() == True:
            
            user_name = self.user_name.get_text()
            user_pass = self.user_pass.get_text()
            
            if user_name == '' or user_pass == '':
                self.message.set_text('Ошибка поля не заполнены')
                gobject.timeout_add(10000, self.messageClear)
                return                
            
            import classes.mysql as mysql

            MySql = mysql.MySql()
            
            sql = 'DROP TABLE IF EXISTS customers'
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return
                
            sql = 'CREATE TABLE customers ( \
                   `id` smallint(5) NOT NULL auto_increment,  \
                   `sername` varchar(50) NOT NULL default "", \
                   `name` varchar(30) NOT NULL default "",    \
                   `company` varchar(50) NOT NULL default "",      \
                   `email` varchar(50) NOT NULL default "",   \
                   `phone` varchar(50) NOT NULL default "",   \
                   PRIMARY KEY  (`id`) \
                   ) engine=myisam'
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return
                
            sql = "DROP TABLE IF EXISTS staff"
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            sql = 'CREATE TABLE staff ( \
                   `id` smallint(5) NOT NULL auto_increment,  \
                   `sername` varchar(50) NOT NULL default "", \
                   `name` varchar(30) NOT NULL default "",    \
                   `post` smallint(2) NOT NULL, \
                   `date` varchar(20) NOT NULL,   \
                   `wage` float(10, 2) NOT NULL default 0.00,  \
                   `email` varchar(50) NOT NULL default "",   \
                   `phone` varchar(50) NOT NULL default "",   \
                   `login` varchar(30) NOT NULL, \
                   `password` varchar(32), \
                   `status` smallint(2) NOT NULL, \
                   PRIMARY KEY  (`id`) \
                   ) engine=myisam'
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            password = md5(user_pass)
            password = password.hexdigest()
            password = md5(password)
            password = password.hexdigest()

            temp = datetime.datetime.now()
            date = time.mktime((temp.year, temp.month, 
                                temp.day, temp.hour, temp.minute, 0, 0, 0, 0))

            sql = 'insert into staff value("", "", "", "0", \
                                           "' + str(date) + '", "", "", "", \
                                           "' + user_name + '", \
                                           "' + password + '", "1")'
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            sql = "DROP TABLE IF EXISTS projects"
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            sql = 'CREATE TABLE projects ( \
                   `id` smallint(5) NOT NULL auto_increment,  \
                   `name` varchar(50) NOT NULL default "",    \
                   `info` text NOT NULL default "",      \
                   `dates` varchar(20) NOT NULL,   \
                   `datee` varchar(20) NOT NULL,   \
                   `status` smallint(1) NOT NULL default "0", \
                   `id_customer` smallint(5) NOT NULL default "0", \
                   `id_staff` smallint(5) NOT NULL default "0", \
                   PRIMARY KEY  (`id`) \
                   ) engine=myisam'
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            sql = "DROP TABLE IF EXISTS accountancy_wage"
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            sql = 'CREATE TABLE accountancy_wage ( \
                   `id` smallint(5) NOT NULL auto_increment,  \
                   `date` varchar(50) NOT NULL default "",    \
                   `id_staff` smallint(5) NOT NULL default "0", \
                   `money` float(10, 2) NOT NULL default 0.00, \
                   `status` smallint(1) NOT NULL default "0", \
                   PRIMARY KEY  (`id`) \
                   ) engine=myisam'
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return
                
            sql = "DROP TABLE IF EXISTS accountancy_pay"
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            sql = 'CREATE TABLE accountancy_pay ( \
                   `id` smallint(5) NOT NULL auto_increment,  \
                   `date` varchar(50) NOT NULL default "",    \
                   `id_project` smallint(5) NOT NULL default "0", \
                   `money` float(10, 2) NOT NULL default 0.00, \
                   `status` smallint(1) NOT NULL default "0", \
                   PRIMARY KEY  (`id`) \
                   ) engine=myisam'
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            sql = "DROP TABLE IF EXISTS projprog"
            if MySql.query(sql) == False: 
                self.message.set_text('Ошибка при добленый таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return

            sql = 'CREATE TABLE projprog ( \
                   `id` smallint(5) NOT NULL auto_increment,  \
                   `id_project` smallint(5) NOT NULL default "0", \
                   `info` text NOT NULL default "",      \
                   PRIMARY KEY  (`id`) \
                   ) engine=myisam'
            if MySql.query(sql) == False:
                self.message.set_text('Ошибка при доблений таблиц в базу')
                gobject.timeout_add(10000, self.messageClear)
                return
        
        self.message.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#1C0772'))
        self.message.set_text('config файл создан')
        gobject.timeout_add(10000, self.messageClear)
        
if __name__ == '__main__':
        
    MakeConfig()
