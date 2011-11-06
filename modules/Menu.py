#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Menu
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/04/15 08:10:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

import sys

import pygtk
pygtk.require('2.0')
import gtk

import cPickle as pickle 
import pango
from hashlib import md5

from classes.staff import Staff

class Base:
    
    menu_toolbar = '''<ui>
    <menubar name="MenuBar">
      <menu action="Файл">
          <menuitem action="Завершить сеанс"/>
        <menuitem action="Сохранить сессию и выйти"/>
        <menuitem action="Выйти"/>
      </menu>
      <menu action="Работа">
        <menuitem action="Клиенты"/>
        <menuitem action="Проекты"/>
          <menuitem action="Персонал"/>
          <menuitem action="Бухгалтерия"/>
      </menu>
      <menu action="Дополнительно">
        <menuitem action="Изменить пароль"/>
      </menu>
      <menu action="Помощь">
        <menuitem action="Про"/>
      </menu>
    </menubar>
    <toolbar name="Toolbar">
      <toolitem action="Клиенты"/>
      <toolitem action="Проекты"/>
      <toolitem action="Персонал"/>
      <toolitem action="Бухгалтерия"/>
      <separator/>
      <toolitem action="Завершить сеанс"/>
      <toolitem action="Сохранить сессию и выйти"/>
    </toolbar>
    </ui>'''
         
    def __init__(self, main, ID):
        
        self.Main = main
        
        self.Staff = Staff(self.Main.MySql)
        
        self.ID = ID
                
        self.PID = int(self.Staff.getOne(self.ID, 'post'))
        
        self.box = gtk.VBox()
        uimanager = gtk.UIManager()
        self.accelgroup = uimanager.get_accel_group()
        self.Main.window.add_accel_group(self.accelgroup)
        
        general_agroup = gtk.ActionGroup('General')
        
        iconfactory = gtk.IconFactory()
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(sys.path[0] +
                                              '/images/customer.png')
        iconfactory.add('STOCK_CUSTOMER', gtk.IconSet(pixbuf))
        iconfactory.add_default()
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(sys.path[0] + 
                                              '/images/project.png')
        iconfactory.add('STOCK_PROJECT', gtk.IconSet(pixbuf))
        iconfactory.add_default()
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(sys.path[0] + 
                                              '/images/staff.png')
        iconfactory.add('STOCK_STAFF', gtk.IconSet(pixbuf))
        iconfactory.add_default()
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(sys.path[0] + 
                                              '/images/accountancy.png')
        iconfactory.add('STOCK_ACCOUNTANCY', gtk.IconSet(pixbuf))
        iconfactory.add_default()
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(sys.path[0] +
                                              '/images/logout.png')
        iconfactory.add('STOCK_LOGOUT', gtk.IconSet(pixbuf))
        iconfactory.add_default()
                                     
        general_agroup.add_actions([('Файл', None, '_Файл'),
                                    ('Завершить сеанс', 
                                     'STOCK_LOGOUT', '_Завершить сеанс', 
                                     '<Control>l', 'Завершить сеанс', 
                                     lambda l: self.Main.sender()),
                                    ('Сохранить сессию и выйти', 
                                     gtk.STOCK_QUIT, 
                                     '_Сохранить сессию и выйти', 
                                     '<Control>s', 'Сохранить сессию и выйти', 
                                     lambda l: self.saveSession()),
                                    ('Выйти', gtk.STOCK_QUIT, '_Выйти', 
                                     None, 'Выйти из программы', 
                                     lambda l: self.quit()),
                                    ('Работа', None, '_Работа'),
                                    ('Дополнительно', None, '_Дополнительно'),
                                    ('Изменить пароль', 
                                     gtk.STOCK_DIALOG_AUTHENTICATION, 
                                     '_Изменить пароль', None, 
                                     'Изменить пароль', self.changePass),
                                    ('Помощь', None, '_Помощь'),
                                    ('Про', gtk.STOCK_ABOUT, '_Про', 
                                     None, 'Про', self.aboutDialog),])
                                           
        module_agroup = gtk.ActionGroup('Module')
        
        module_agroup.add_radio_actions([('Клиенты', 'STOCK_CUSTOMER', 
                                          '_Клиенты', '<alt><ctrl>c', 
                                          'Клиенты', 0), 
                                         ('Проекты', 'STOCK_PROJECT', 
                                          '_Проекты', '<alt><ctrl>p', 
                                          'Проекты', 1),
                                         ('Персонал', 'STOCK_STAFF', 
                                          '_Персонал', '<alt><ctrl>s', 
                                          'Персонал', 2),
                                         ('Бухгалтерия', 'STOCK_ACCOUNTANCY', 
                                          '_Бухгалтерия', '<alt><ctrl>a',
                                          'Бухгалтерия', 3),], 0, self.sender)
        
        uimanager.insert_action_group(general_agroup, 0)
        uimanager.insert_action_group(module_agroup, 1)
        
        customer_action    = module_agroup.get_action('Клиенты')
        project_action     = module_agroup.get_action('Проекты')
        staff_action       = module_agroup.get_action('Персонал')
        accountancy_action = module_agroup.get_action('Бухгалтерия')
        
        ## Rights ##
        
        if self.PID == 0 or self.PID == 1 or self.PID == 2:
            customer_action.set_active(True)
            self.active = 1
        elif self.PID == 3: 
            staff_action.set_active(True)
            self.active = 3
        elif self.PID == 4: 
            accountancy_action.set_active(True)
            self.active = 4
        elif self.PID == 5: 
            project_action.set_active(True) 
            self.active = 2
            
        if self.PID > 2: 
            customer_action.set_visible(False)
            customer_action.set_sensitive(False)
        if self.PID == 3 or self.PID == 4 or self.PID == 6 or self.PID == 7:
            project_action.set_visible(False)
            project_action.set_sensitive(False)
        if self.PID == 2 or self.PID > 3: 
            staff_action.set_visible(False)
            staff_action.set_sensitive(False)
        if self.PID == 2 or self.PID == 3 or self.PID > 4:
            accountancy_action.set_visible(False)
            accountancy_action.set_sensitive(False)
        
        ## End Rights ##
        
        uimanager.add_ui_from_string(self.menu_toolbar)
        
        menubar = uimanager.get_widget('/MenuBar')
        self.box.pack_start(menubar, False)
        
        toolbar = uimanager.get_widget('/Toolbar')
        self.box.pack_start(toolbar, False)
        
        self.box.show_all()
    
    def gO(self):
    
        return self.box
    
    def sender(self, action, current):

        if current.get_name() == 'Клиенты':
            self.Main.senderD(1)
        elif current.get_name() == 'Проекты':
            self.Main.senderD(2)
        elif current.get_name() == 'Персонал':
            self.Main.senderD(3)
        elif current.get_name() == 'Бухгалтерия':
            self.Main.senderD(4)
    
    def saveSession(self):

        login    = self.Staff.getOne(self.ID, 'login')
        password = self.Staff.getOne(self.ID, 'password')
        
        obj = {"login": login, "password": password}
        f = open(sys.path[0] + '/session.pkl', 'wb')
        pickle.dump(obj, f, 2)
        f.close()
        
        gtk.main_quit()

    def quit(self):
        
        f = open(sys.path[0] + '/session.pkl', 'wb')
        f.close()
        
        gtk.main_quit()
    
    def aboutDialog(self, *args):
                
        about_dialog = gtk.Dialog('Про программу')

        about_dialog.move(self.Main.window.get_position()[0] + 150, 
                          self.Main.window.get_position()[1] + 150)
        about_dialog.set_modal(True)
        about_dialog.set_has_separator(False)
        about_dialog.set_resizable(False)
        about_dialog.set_size_request(300, -1)
        about_dialog.set_skip_taskbar_hint(True)  
        about_dialog.set_icon_from_file(sys.path[0] + '/images/logotip.png')
                        
        vbox = gtk.VBox(False, 10)
        
        logotip = gtk.Image()
        logotip.set_from_file(sys.path[0] + '/images/logotip.png')
        vbox.pack_start(logotip)
        
        name_label = gtk.Label('Стройка 1.0')
        name_label.modify_font(pango.FontDescription('Monospace Bold 17'))
        name_label.set_alignment(0.5, 0.0)
        vbox.pack_start(name_label)
        
        about_label = gtk.Label('Стройка - программа для управления\n'
                                'строительной компанией.')
        about_label.set_justify(gtk.JUSTIFY_CENTER)
        about_label.set_alignment(0.5, 0.0)
        vbox.pack_start(about_label)
        
        copyright_label = gtk.Label('Copyright (c) 2009 r0n9.GOL '
                                    'ron9.gol@gmail.com')
                                    
        copyright_label.set_selectable(True)
        
        copyright_label.modify_font(pango.FontDescription('Monospace 8'))
        copyright_label.set_alignment(0.5, 0.0)
        vbox.pack_start(copyright_label)
        
        hbox = gtk.HBox(True)
        url_button = gtk.LinkButton('http://www.pamparam.net')
        url_button.set_alignment(0.5, 0.0)
        hbox.pack_start(url_button, True, False)
        vbox.pack_start(hbox, True, True)
        
        hbox = gtk.HBox(True)
        quit_button = gtk.Button(stock = gtk.STOCK_QUIT)
        quit_button.connect('clicked', lambda l: about_dialog.destroy())
        quit_button.set_alignment(0.5, 0.0)
        hbox.pack_start(quit_button, True, False)
        vbox.pack_start(hbox, True, True)
        
        about_dialog.vbox.pack_start(vbox)
        about_dialog.show_all()
    
    def changePass(self, *args):
    
        self.chpass_dialog = gtk.Dialog('Смена пароля')

        self.chpass_dialog.move(self.Main.window.get_position()[0] + 150, 
                          self.Main.window.get_position()[1] + 150)
        self.chpass_dialog.set_modal(True)
        self.chpass_dialog.set_has_separator(False)
        self.chpass_dialog.set_resizable(False)
        self.chpass_dialog.set_size_request(500, -1)
        self.chpass_dialog.set_skip_taskbar_hint(True)  
        self.chpass_dialog.set_icon_from_file(
                                            sys.path[0] + '/images/logotip.png')
        
        table = gtk.Table(2, 6, False)
        table.set_row_spacings(10)
        table.set_col_spacings(20)
        
        image = gtk.Image()
        image.set_from_file(sys.path[0] + '/images/changepass.png')
        table.attach(image, 0, 2, 0, 1)
                        
        login_label = gtk.Label('Старый пароль:')
        login_label.set_alignment(0, 0.5)
        table.attach(login_label, 0, 1, 1, 2)
            	
    	self.oldpass_entry = gtk.Entry()
    	table.attach(self.oldpass_entry, 1, 2, 1, 2)
    	    	    	
    	password_label = gtk.Label('Новый пароль:')
    	password_label.set_alignment(0, 0.5)
    	table.attach(password_label, 0, 1, 2, 3)
    	
    	self.newpassword1_entry = gtk.Entry()
    	self.newpassword1_entry.set_visibility(False)
    	table.attach(self.newpassword1_entry, 1, 2, 2, 3)
    	
    	password_label = gtk.Label('Новый пароль еще раз:')
    	password_label.set_alignment(0, 0.5)
    	table.attach(password_label, 0, 1, 3, 4)
    	
    	self.newpassword2_entry = gtk.Entry()
    	self.newpassword2_entry.set_visibility(False)
    	table.attach(self.newpassword2_entry, 1, 2, 3, 4)
    	
    	showpassword = gtk.CheckButton('Показать пароль')
    	showpassword.connect('toggled', self.showPass) 
    	               
    	table.attach(showpassword, 1, 2, 4, 5)
    	    	  	    	    	
        hbox = gtk.HBox()
        
        cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
    	cancel_button.set_size_request(90, 40)
    	cancel_button.connect('clicked', lambda l: self.chpass_dialog.destroy())
        hbox.pack_start(cancel_button)
        
    	ok_button = gtk.Button(stock = gtk.STOCK_OK)
    	ok_button.set_size_request(90, 40)
    	ok_button.connect('clicked', self.changePassOk)
    	hbox.pack_start(ok_button)
    	
    	alignment = gtk.Alignment(1.0)
    	alignment.add(hbox)
    	
    	table.attach(alignment, 1, 2, 5, 6)
    	
    	self.message = gtk.Label()
    	self.message.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#e12e2e'))
    	self.message.set_alignment(0, 0.5)
    	table.attach(self.message, 0, 2, 4, 5)
    	    	    	
    	alignment = gtk.Alignment(0.5, 0.0)
    	alignment.add(table)
        
        self.chpass_dialog.vbox.pack_start(alignment)
        self.chpass_dialog.show_all()
    
    def changePassOk(self, *args):
        
        old_password = md5(self.oldpass_entry.get_text())
        old_password = old_password.hexdigest()
        old_password = md5(old_password)
        old_password = old_password.hexdigest()
        new_password1 = self.newpassword1_entry.get_text()
        new_password2 = self.newpassword2_entry.get_text()
        
        if new_password1 == new_password2 and new_password1 != '' and \
           self.Staff.getOne(self.ID, 'password') == old_password:
           self.Staff.changePass(self.ID, new_password1)
           self.chpass_dialog.destroy()
        else:
            self.message.set_text('Неправельно \nвведены данные')
        
    def showPass(self, toggbutt):

        self.newpassword1_entry.set_visibility(toggbutt.get_active())
    	self.newpassword2_entry.set_visibility(toggbutt.get_active())
        
