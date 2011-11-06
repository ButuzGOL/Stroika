#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Login panel
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/04/14 07:59:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

import sys

import pygtk
pygtk.require('2.0')
import gtk

import classes.staff as staff

class Base:
        
    def __init__(self):
        
        self.box = gtk.VBox()

        table = gtk.Table(2, 5, False)
        table.set_row_spacings(10)
        table.set_col_spacings(20)
        
        logotip = gtk.Image()
        logotip.set_from_file(sys.path[0] + '/images/logotip.png')
        table.attach(logotip, 0, 2, 0, 1)
                        
        login_label = gtk.Label('Логин:')
        login_label.set_alignment(0, 0.5)
        table.attach(login_label, 0, 1, 1, 2)
                
        self.login_entry = gtk.Entry()
        table.attach(self.login_entry, 1, 2, 1, 2)
                        
        password_label = gtk.Label('Пароль:')
        password_label.set_alignment(0, 0.5)
        table.attach(password_label, 0, 1, 2, 3)
        
        self.password_entry = gtk.Entry()
        self.password_entry.connect('key_press_event', self.pressPE)
        self.password_entry.set_visibility(False)
        table.attach(self.password_entry, 1, 2, 2, 3)
        
        showpassword = gtk.CheckButton('Показать пароль')
        showpassword.connect('toggled', lambda l: 
                             self.password_entry.set_visibility(l.get_active()))
        table.attach(showpassword, 1, 2, 3, 4)
                                      
        enter_button = gtk.Button(stock = gtk.STOCK_OK)
        enter_button.set_size_request(90, 40)
        enter_button.connect('clicked', self.checkLogPass)
        
        alignment = gtk.Alignment(1.0)
        alignment.add(enter_button)
        
        table.attach(alignment, 1, 2, 4, 5)
        
        self.message = gtk.Label()
        self.message.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#e12e2e'))
        self.message.set_alignment(0, 0.5)
        table.attach(self.message, 0, 2, 4, 5)
                        
        alignment = gtk.Alignment(0.5, 0.5)
        alignment.add(table)
        
        self.box.pack_start(alignment)
        self.box.show_all()
            
    def gO(self, mainclass):
                   
        self.MainClass = mainclass
        
        self.Staff = staff.Staff(self.MainClass.MySql)
        
        self.MainClass.window.resize(1, 1)
        self.MainClass.window.set_size_request(500, 400)
        
        return self.box
        
    def checkLogPass(self, empty):
                
        if self.Staff.checkLP(self.login_entry.get_text(), 
                              self.password_entry.get_text()) == True:
            
            ID = int(self.Staff.getId(self.login_entry.get_text(), 
                                      self.password_entry.get_text()))
            
            self.box.destroy()
            self.MainClass.sender(1, ID)
        else:
            self.message.set_text('Неправельный \nлогин либо пароль')
      
    def pressPE(self, empty, event):
    
        if gtk.gdk.keyval_name(event.keyval) == 'Return': 
            self.checkLogPass(None)
