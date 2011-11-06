#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
General file that make move
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/04/12 11:34:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

import pygtk
pygtk.require('2.0')
import gtk

import sys
import cPickle as pickle

import classes.mysql as mysql
import classes.staff as staff

class Main:
        
    def __init__(self):
        
        self.MySql = mysql.MySql()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Стройка')
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_icon_from_file(sys.path[0] + '/images/logotip.png')
        self.window.connect('destroy', lambda l: gtk.main_quit())
        
        self.go = None
        
        self.loadSession()
    
        self.sender(1)
        
        self.window.show()
        
        gtk.main()
        
    def sender(self, location = None, ID = None):
        
        if location != None and (ID != None or self.ID != None):
            
            if self.ID == None or ID != None: self.ID = ID
            
            self.module = None
            
            self.window.set_size_request(950, 600)
            
            self.go = gtk.VBox()
                        
            import modules.Menu as menu
            
            self.menu = menu.Base(self, self.ID)
            self.menuGo = self.menu.gO()
            self.go.pack_start(self.menuGo, False)
            
            self.senderD(self.menu.active)
            
            self.go.show()
        else:
            if self.go != None: 
                self.window.remove(self.go)
                f = open(sys.path[0] + '/session.pkl', 'wb')
                f.close()
            import modules.Login as module
            self.go = module.Base().gO(self)
        
        self.window.add(self.go)
    
    def senderD(self, location = None):
        
        if self.module != None:
            self.moduleGo.destroy()

        if location == 1: 
            import modules.Customers as module
                
        elif location == 2:
            import modules.Projects as module
        
        elif location == 3:
            import modules.Staff as module
        
        elif location == 4:
            import modules.Accountancy as module
        
        self.module   = module.Base(self.MySql, self.window, self.ID)
        self.moduleGo = self.module.gO()
        self.go.add(self.moduleGo)
    
    def loadSession(self):
        
        try:
            
            f = open(sys.path[0] + '/session.pkl', 'rb')
            obj = pickle.load(f)
            f.close()

            self.ID = int(staff.Staff(self.MySql).getSessId(obj['login'], \
                                                        obj['password']))
            
            if self.ID == False: self.ID = None
                
        except: self.ID = None
        
if __name__ == '__main__':
        
    Main()
