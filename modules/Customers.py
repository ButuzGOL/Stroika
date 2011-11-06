#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Customers module
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/03/16 14:48:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

import sys

import pygtk
pygtk.require('2.0')
import gtk

import pango
import random
import gobject

import classes.customer as customer
from classes.staff import Staff

class Base:
        
    def __init__(self, MySql, window, ID):
                      
        self.Window = window
        
        self.Customer = customer.Customer(MySql)
        
        self.PID = int(Staff(MySql).getOne(ID, 'post'))
        
        ### veriables ###
        
        self.add_dialog = []
                
        self.add_sername = []
        self.add_name    = []
        self.add_company = []
        self.add_email   = []
        self.add_phone   = []
        
        self.edit_dialog = []
        self.edit_box    = []
        self.edit_model  = []
        
        self.edit_sername = []
        self.edit_name    = []
        self.edit_company = []
        self.edit_email   = []
        self.edit_phone   = []
        
        self.view_dialog = []
        self.view_box    = []
        self.view_model  = []
                        
        ### end veriables ###
        
        self.box = gtk.VBox()
        self.box.set_border_width(10)
            	    
        ### Title ###
                
        hbox = gtk.HBox()
                                                        
        title_image = gtk.Image()
        title_image.set_from_file(sys.path[0] + '/images/customer.png')       
        hbox.pack_start(title_image, False)
        
        title_label = gtk.Label('Клиенты')
        title_label.modify_font(pango.FontDescription('Monospace Bold 20'))
        title_label.set_alignment(0, 1.0)
        
        hbox.pack_start(title_label)     
                                                         	
    	self.box.pack_start(hbox, False)
    	
    	### End Title ###
    	   	
    	hbox = gtk.HBox()
    	
    	self.message = gtk.Label()
    	self.message.modify_fg(gtk.STATE_NORMAL, 
        						   gtk.gdk.color_parse('#e12e2e'))
    	hbox.pack_start(self.message)     
        
    	self.box.pack_start(hbox, False)
    	
    	### List ###
    	
    	list_frame = gtk.Frame(' Список клиентов ')
    	list_frame.set_border_width(3)
    	
    	table = gtk.Table(3, 2, False)
    	table.set_row_spacings(10)
    	table.set_border_width(10)
    	 
    	self.liststore = gtk.ListStore(int, bool, str, str, str, str, 
    	                               str, int, int)
    	
    	list_scrolled = gtk.ScrolledWindow()
    	list_scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    	
    	listof = gtk.TreeView(self.liststore)
        
    	listof.set_reorderable(True)
    	
    	self.treeselection = listof.get_selection()
    	self.treeselection.set_mode(gtk.SELECTION_MULTIPLE)
    	
    	listof.connect('key_press_event', self.pressDel)
    	
    	id_column            = gtk.TreeViewColumn()
    	toggle_column        = gtk.TreeViewColumn()
    	sername_column       = gtk.TreeViewColumn('Фамилия')
    	name_column          = gtk.TreeViewColumn('Имя')
    	company_column       = gtk.TreeViewColumn('Фирма')
    	email_column         = gtk.TreeViewColumn('Email')
    	phone_column         = gtk.TreeViewColumn('Телефон')
    	endproj_column       = gtk.TreeViewColumn('Зав. Пр.')
    	performedproj_column = gtk.TreeViewColumn('Проц. Пр.')
    	    	
    	id_column.set_visible(False)
    	toggle_column.set_min_width(20)
    	toggle_column.set_clickable(True)
    	sername_column.set_resizable(True)
    	sername_column.set_expand(True)
    	sername_column.set_sort_column_id(2)
    	name_column.set_resizable(True)
    	name_column.set_min_width(200)
    	name_column.set_sort_column_id(3)
    	company_column.set_clickable(True)
    	company_column.set_resizable(True)
    	company_column.set_sort_column_id(4)
    	email_column.set_resizable(True)
    	email_column.set_sort_column_id(5)    	
    	phone_column.set_resizable(True)
    	phone_column.set_sort_column_id(6)
    	endproj_column.set_sort_column_id(7)    	
    	performedproj_column.set_sort_column_id(8)
    	    	    	    	   	
    	toggle_column.connect('clicked', self.idAllToggled)
    	self.toggle_all_toggled = False
    	
    	listof.append_column(id_column)    	        
        listof.append_column(toggle_column)        
        listof.append_column(sername_column)
        listof.append_column(name_column)
        listof.append_column(company_column)
        listof.append_column(email_column)
        listof.append_column(phone_column)
        listof.append_column(endproj_column)
        listof.append_column(performedproj_column)
                                        
        id_cell            = gtk.CellRendererText()
        toggle_cell        = gtk.CellRendererToggle()
        sername_cell       = gtk.CellRendererText()
        name_cell          = gtk.CellRendererText()
        company_cell       = gtk.CellRendererText()
        email_cell         = gtk.CellRendererText()
        phone_cell         = gtk.CellRendererText()
        endproj_cell       = gtk.CellRendererText()
        performedproj_cell = gtk.CellRendererText()
        
        toggle_cell.set_property('activatable', True)
        toggle_cell.connect('toggled', self.idToggled, self.liststore)
        
        if self.PID == 0 or self.PID == 2:
            sername_cell.set_property('editable', True)
            sername_cell.connect('edited', self.edit, self.liststore, 2)
            name_cell.set_property('editable', True)
            name_cell.connect('edited', self.edit, self.liststore, 3)
            company_cell.set_property('editable', True)
            company_cell.connect('edited', self.edit, self.liststore, 4)
            email_cell.set_property('editable', True)
            email_cell.connect('edited', self.edit, self.liststore, 5)
            phone_cell.set_property('editable', True)
            phone_cell.connect('edited', self.edit, self.liststore, 6)
                               
        id_column.pack_start(id_cell, True)        
        toggle_column.pack_start(toggle_cell, True)
        sername_column.pack_start(sername_cell, True)
        name_column.pack_start(name_cell, True)
        company_column.pack_start(company_cell, True)
        email_column.pack_start(email_cell, True)
        phone_column.pack_start(phone_cell, True)
        endproj_column.pack_start(endproj_cell, True)
        performedproj_column.pack_start(performedproj_cell, True)
        
        id_column.set_attributes(id_cell, text = 0)
        toggle_column.add_attribute(toggle_cell, 'active', 1) 
        sername_column.set_attributes(sername_cell, text = 2)
        name_column.set_attributes(name_cell, text = 3)
        company_column.set_attributes(company_cell, text = 4)
        email_column.set_attributes(email_cell, text = 5)
        phone_column.set_attributes(phone_cell, text = 6)
        endproj_column.set_attributes(endproj_cell, text = 7)
        performedproj_column.set_attributes(performedproj_cell, text = 8)
               
        list_scrolled.add(listof)
        
        table.attach(list_scrolled, 0, 2, 0, 1)
        
        ### End List ###
    	    	
    	### Action list ###
    	
    	if self.PID == 0 or self.PID == 2:
            self.add_button = gtk.Button(stock = gtk.STOCK_ADD)
            self.add_button.connect('clicked', self.addForm) 
            alignment = gtk.Alignment(1.0)
            alignment.add(self.add_button)
            table.attach(alignment, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
                
        hbox = gtk.HBox()
        
        self.action_combobox = gtk.combo_box_new_text()
        
        self.action_combobox.append_text('Посмотреть')
        
        if self.PID == 0 or self.PID == 2:
            self.action_combobox.append_text('Редактировать')
            self.action_combobox.append_text('Удалить')
        
        self.action_combobox.set_active(0)        
        
        hbox.pack_start(self.action_combobox)
        
        self.actionok_button = gtk.Button(stock = gtk.STOCK_OK)
        self.actionok_button.connect('clicked', self.makeAction)
        hbox.pack_start(self.actionok_button)
                
        alignment = gtk.Alignment(0.0)
        alignment.add(hbox)
        
        ### End action list ###
        
        self.getList()
                
        table.attach(alignment, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
                        
        list_frame.add(table)
                
        box1 = gtk.HBox()
        box1.pack_start(list_frame)
                                
        self.box.pack_start(box1)
        
        self.box.show_all()
        
    def gO(self):
               
        return self.box   
    
    def pressDel(self, empty, event):
    
        if gtk.gdk.keyval_name(event.keyval) == 'Delete' and \
           (self.PID == 0 or self.PID == 2):
            model, model1 = self.treeselection.get_selected_rows()
            k = 0
            for i in model1:
                result = self.Customer.delete(self.liststore[i[0]-k][0])
                if result == False: 
                    self.message.set_text('Ошибка поле не удалено')
                    gobject.timeout_add(10000, self.messageClear)
                else: self.message.set_text('')

                iter = self.liststore.get_iter(i[0]-k)
                self.liststore.remove(iter)
                k += 1
            
            if len([i for i in self.liststore if i[1] == True]) == 0:
                self.action_combobox.set_sensitive(False)
                self.actionok_button.set_sensitive(False)
        elif gtk.gdk.keyval_name(event.keyval) == 'p': self.viewForm(1)
        elif gtk.gdk.keyval_name(event.keyval) == 'r' and \
           (self.PID == 0 or self.PID == 2): self.editForm(1)
        elif gtk.gdk.keyval_name(event.keyval) == 'a' and \
           (self.PID == 0 or self.PID == 2): self.addForm()

    def idToggled(self, cell, path, liststore):
     
        liststore[path][1] = not liststore[path][1]
        
        for i in range(len(self.liststore)):
            if liststore[i][1] == True:
                self.action_combobox.set_sensitive(True)
                self.actionok_button.set_sensitive(True)
                return
    	                
        self.action_combobox.set_sensitive(False)
    	self.actionok_button.set_sensitive(False)
        
    def idAllToggled(self, *args):
    
    	self.toggle_all_toggled = not self.toggle_all_toggled
    	
    	for i in range(len(self.liststore)):
    		self.liststore[i][1] = self.toggle_all_toggled
    		
    	if self.toggle_all_toggled == True and len(self.liststore):
    	    self.action_combobox.set_sensitive(True)
    	    self.actionok_button.set_sensitive(True)
    	else:
    	    self.action_combobox.set_sensitive(False)
    	    self.actionok_button.set_sensitive(False)        
        
    def addForm(self, *args):
                   
        wd = len(self.add_dialog)
        self.add_dialog.append(wd)
        
        self.add_sername.append(wd)
        self.add_name.append(wd)
        self.add_company.append(wd)
        self.add_email.append(wd)
        self.add_phone.append(wd)
        
        self.add_dialog[wd] = gtk.Dialog('Добавление клиента')

        self.add_dialog[wd].move(self.Window.get_position()[0] + 150 + 
        						 random.randrange(30), 
        						 self.Window.get_position()[1] + 150 + 
        						 random.randrange(30))
        self.add_dialog[wd].set_has_separator(False)
        self.add_dialog[wd].set_resizable(False)
        self.add_dialog[wd].set_skip_taskbar_hint(True)  
        self.add_dialog[wd].set_icon_from_file(sys.path[0] + 
                                               '/images/logotip.png')
                        
        table = gtk.Table(2, 6, False)
        table.set_border_width(5)
        table.set_row_spacings(10)
        table.set_col_spacings(10)        
        
        label = gtk.Label('Фамилия:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
        
        self.add_sername[wd] = gtk.Entry()
        self.add_sername[wd].grab_focus()
        table.attach(self.add_sername[wd], 1, 2, 0, 1, yoptions = gtk.FILL)
        
        label = gtk.Label('Имя:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
        
        self.add_name[wd] = gtk.Entry()
        table.attach(self.add_name[wd], 1, 2, 1, 2, yoptions = gtk.FILL)
        
        label = gtk.Label('Фирма:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
        
        self.add_company[wd] = gtk.Entry()
        table.attach(self.add_company[wd], 1, 2, 2, 3, yoptions = gtk.FILL)
                               
        label = gtk.Label('Email:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
        
        self.add_email[wd] = gtk.Entry()
        table.attach(self.add_email[wd], 1, 2, 3, 4, yoptions = gtk.FILL)
        
        label = gtk.Label('Телефон:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
        
        self.add_phone[wd] = gtk.Entry()
        table.attach(self.add_phone[wd], 1, 2, 4, 5, yoptions = gtk.FILL)
        
        hbox = gtk.HBox()
        
        ok_button = gtk.Button(stock = gtk.STOCK_OK)
        ok_button.connect('clicked', self.addFormOk, wd)
        hbox.pack_start(ok_button)
        
        cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
        cancel_button.connect('clicked', self.addFormCancel, wd)
        hbox.pack_start(cancel_button)
        
        table.attach(hbox, 0, 1, 5, 6, yoptions = gtk.FILL)         
          
        self.add_dialog[wd].vbox.pack_start(table)
        self.add_dialog[wd].show_all()   
    
    def addFormOk(self, empty, wd):
        
        sername = self.add_sername[wd].get_text()
        name    = self.add_name[wd].get_text()
        company = self.add_company[wd].get_text()
        email   = self.add_email[wd].get_text()
        phone   = self.add_phone[wd].get_text()
        
        if name != '' or sername != '' or email != '' or phone != '' \
           or company !='':
        	
        	result = self.Customer.add(sername, name, company, email, phone)
        							    
        	if result == False:	
        	    self.message.set_text('Ошибка клиент не добавлен')
        	    gobject.timeout_add(10000, self.messageClear)
        	else:
        	    self.message.set_text('')
                self.liststore.append([self.Customer.lastId(), False, 
                                       sername, name, company, email, 
                                       phone, 0, 0])

        self.add_dialog[wd].destroy()               
    
    def addFormCancel(self, empty, wd):
        
        self.add_dialog[wd].destroy() 
            
    def getList(self):

        result = self.Customer.get()
        
        if len(result):
            model = [i[0] for i in self.liststore]
            for arr in result:
                if model.count(int(arr[0])) == 0:                 
                    self.liststore.append([int(arr[0]), False,  
		                                   arr[1], arr[2], arr[3], 
                                           arr[4], arr[5], 
                                    int(self.Customer.getCountPro(arr[0], 1)), 
                                    int(self.Customer.getCountPro(arr[0]))])
            
            model1 = [int(i[0]) for i in result]
            j = 0
            for i in range(len(model)):
                if model1.count(model[i]) == 0:
                    i = i - j
                    iter = self.liststore.get_iter(i)
                    self.liststore.remove(iter)
                    j += 1        
                                                                              
       	else: 
       	    self.liststore.clear()
    	
    	model = [i[0] for i in self.liststore if i[1] == True]
        
        if len(model) > 0:
            self.action_combobox.set_sensitive(True)
    	    self.actionok_button.set_sensitive(True)
    	else:
    	    self.action_combobox.set_sensitive(False)
    	    self.actionok_button.set_sensitive(False)
    	            	       	
       	gobject.timeout_add(5000, self.getList)
       	       	       			            
    def makeAction(self, *args): 
        
        model  = self.action_combobox.get_model()
        index  = self.action_combobox.get_active()
        action = model[index][0]

        if action == 'Посмотреть':
            self.viewForm()
        elif action == 'Редактировать':
            model = [i[0] for i in self.liststore if i[1] == True]
            self.editForm()
        elif action == 'Удалить':
            model = [i[0] for i in self.liststore if i[1] == True]
            result = self.Customer.makeIn(model)
            if result == False: 
                self.message.set_text('Ошибка удаления')  
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()                
            
    def edit(self, cell, row, new_text, liststore, coll):
        
        liststore[row][coll] = new_text
        
        result = self.Customer.updateOne(str(liststore[row][0]), 
        								  self.getNameField(coll), new_text)
        								  
        if result == False: 
            self.message.set_text('Ошибка поле не изменино')
            gobject.timeout_add(10000, self.messageClear)
        else: self.message.set_text('')
                   
    def getNameField(self, coll):
    	
    	if coll == 2: field = 'sername'
    	elif coll == 3: field = 'name'
    	elif coll == 4: field = 'company'
    	elif coll == 5: field = 'email'
    	else: field = 'phone'
    	
    	return field
    
    def editForm(self, tp = 0):
    
    	wd = len(self.edit_dialog)
        self.edit_dialog.append(wd)
        
        self.edit_dialog[wd] = gtk.Dialog()
        self.edit_dialog[wd].set_border_width(10)
        self.edit_dialog[wd].move(self.Window.get_position()[0] + 150 + 
        						  random.randrange(30), 
        						  self.Window.get_position()[1] + 150 + 
        						  random.randrange(30))
        self.edit_dialog[wd].set_has_separator(False)
        self.edit_dialog[wd].set_resizable(False)
        self.edit_dialog[wd].set_skip_taskbar_hint(True)  
        self.edit_dialog[wd].set_icon_from_file(sys.path[0] + 
        									    '/images/logotip.png')          
        
        self.edit_box.append(wd)
        self.edit_box[wd] = None
        
        self.edit_model.append(wd)
        
        temp = []
        if tp == 0: temp = [i for i in self.liststore if i[1] == True]
        else: 
            model, model1 = self.treeselection.get_selected_rows()
            k = [j[0] for j in model1]
            for i in range(len(model)):
                if i in k: temp.append(model[i])
                
        self.edit_model[wd] = []        
        for i in temp:
        	self.edit_model[wd].append([j for j in i])
        
        self.edit_sername.append(wd)       	            
        self.edit_name.append(wd)
        self.edit_company.append(wd)
        self.edit_email.append(wd)
        self.edit_phone.append(wd)
        
        hbox1 = self.editFormEl(wd, 0)
        
    def editFormEl(self, wd, index, bindex = None):
        
        if self.edit_box[wd] != None: self.edit_box[wd].destroy()
                     
        if bindex != None:
        	
        	self.edit_model[wd][bindex - 1][2] = \
        	                                self.edit_sername[wd][0].get_text()
        	self.edit_model[wd][bindex - 1][3] = \
        	                                self.edit_name[wd][0].get_text()
        	self.edit_model[wd][bindex - 1][4] = \
        	                                self.edit_company[wd][0].get_text()
        	self.edit_model[wd][bindex - 1][5] = \
        	                                self.edit_email[wd][0].get_text()
        	self.edit_model[wd][bindex - 1][6] = \
        	                                self.edit_phone[wd][0].get_text()
        	
        	self.edit_model[wd][bindex][2] = self.edit_sername[wd][1].get_text()
        	self.edit_model[wd][bindex][3] = self.edit_name[wd][1].get_text()
        	self.edit_model[wd][bindex][4] = self.edit_company[wd][1].get_text()
        	self.edit_model[wd][bindex][5] = self.edit_email[wd][1].get_text()
        	self.edit_model[wd][bindex][6] = self.edit_phone[wd][1].get_text()
        
        temp  = [i for i in self.liststore]        
        temp2 = [i for i in self.edit_model[wd]]
        
        k = 0
        for i in temp2:
            if k == index: 
                vindex = i[0]
                break
            k += 1
        
        k = 0        
        for i in temp2:
            k1 = 0
            for j in temp:       
                if i[0] == j[0]:
                    k1 = 1
                    break  
            if k1 == 0: 
                self.edit_model[wd].pop(k)
                k -= 1
            k += 1  
               
        if len(self.edit_model[wd]) == 0: 
            self.edit_dialog[wd].destroy()
            return
        
        k2 = index
        k1 = 0    
        temp2 = [i for i in self.edit_model[wd]]
        for i in temp2:
            if vindex == i[0]:
                index = k1 
                break             
            k1 += 1
        
        if k2 == index:
            if index >= len(self.edit_model[wd]): 
                index = len(self.edit_model[wd]) - 1          
        
        self.edit_sername[wd] = [0, 1]
        self.edit_name[wd]    = [0, 1]
        self.edit_company[wd] = [0, 1]
        self.edit_email[wd]   = [0, 1]
        self.edit_phone[wd]   = [0, 1]
                                            
        box = gtk.HBox()
        
        if len(self.edit_model[wd]) < 2: l = 1
        else: l = 2
                
        for i in range(l):
            
            if l == 1: self.edit_dialog[wd].set_title('Редактирование клиента')
            else: self.edit_dialog[wd].set_title('Редактирование клиентов')
            
            if (index + i) == len(self.edit_model[wd]): k = 0
            else: k = index + i
                         
            arr = self.edit_model[wd][k]
                        
            frame = gtk.Frame(' ' + arr[2] + ' ' + arr[3] + ' ')
            frame.set_border_width(3)                
            table = gtk.Table(2, 6, False)
            table.set_border_width(5)
            table.set_row_spacings(10)
            table.set_col_spacings(10)        
                                    
            label = gtk.Label('Фамилия:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
            
            self.edit_sername[wd][i] = gtk.Entry()
            self.edit_sername[wd][i].set_text(arr[2])
            if i == 0: self.edit_sername[wd][i].grab_focus()
            table.attach(self.edit_sername[wd][i], 1, 2, 0, 1, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Имя:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
            
            self.edit_name[wd][i] = gtk.Entry()
            self.edit_name[wd][i].set_text(arr[3])
            table.attach(self.edit_name[wd][i], 1, 2, 1, 2, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Фирма:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
            
            self.edit_company[wd][i] = gtk.Entry()
            self.edit_company[wd][i].set_text(arr[4])
            table.attach(self.edit_company[wd][i], 1, 2, 2, 3, 
                         yoptions = gtk.FILL)
                        
            label = gtk.Label('Email:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
            
            self.edit_email[wd][i] = gtk.Entry()
            self.edit_email[wd][i].set_text(arr[5])
            table.attach(self.edit_email[wd][i], 1, 2, 3, 4, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Телефон:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
            
            self.edit_phone[wd][i] = gtk.Entry()
            self.edit_phone[wd][i].set_text(arr[6])
            table.attach(self.edit_phone[wd][i], 1, 2, 4, 5, 
                         yoptions = gtk.FILL)
            
            hbox = gtk.HBox()
            
            ok_button = gtk.Button(stock = gtk.STOCK_OK)
            ok_button.connect('clicked', self.editFormOk, wd, k, i)
            hbox.pack_start(ok_button)
            
            cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
            cancel_button.connect('clicked', self.editFormCancel, wd, k, i)
            hbox.pack_start(cancel_button)
            
            table.attach(hbox, 0, 1, 5, 6, yoptions = gtk.FILL)         
            
            frame.add(table)
            box.pack_start(frame)
        
        self.edit_box[wd] = gtk.VBox()
        
        self.edit_box[wd].pack_start(box)
        
        box1 = gtk.HBox()
        
        if len(self.edit_model[wd]) > 2:    
                    
            if index == (len(self.edit_model[wd]) - 1): 
                back    = index - 1
                forward = 0
            elif index == 0:
                back    = len(self.edit_model[wd]) - 1
                forward = index + 1 
            else:
                back    = index - 1
                forward = index + 1 
                    
            back_button = gtk.Button(stock = gtk.STOCK_GO_BACK)
            back_button.connect('clicked', 
                                lambda l: self.editFormEl(wd, back, k))
            box1.pack_start(back_button, True, False)
            
            forward_button = gtk.Button(stock = gtk.STOCK_GO_FORWARD)
            forward_button.connect('clicked', lambda l: 
                                              self.editFormEl(wd, forward, k))
            box1.pack_start(forward_button, True, False)
        
        quit_button = gtk.Button(stock = gtk.STOCK_QUIT)
        quit_button.connect('clicked', lambda l: self.edit_dialog[wd].destroy())
        box1.pack_start(quit_button, True, False)
        
        self.edit_box[wd].pack_start(box1)
                
        self.edit_dialog[wd].vbox.pack_start(self.edit_box[wd])
        self.edit_dialog[wd].show_all()
        
    def editFormCancel(self, empty, wd, index, bindex1):
    
        if len(self.edit_model[wd]) == 1: 
            self.edit_dialog[wd].destroy()
            return
        
        if bindex1 == 0: 
            bindex1 = 1
            bindex = index + 1
            if bindex == len(self.edit_model[wd]): bindex = 0
        else: 
            bindex1 = 0
            bindex = index - 1
        
        self.edit_model[wd][bindex][2] = \
                                    self.edit_sername[wd][bindex1].get_text()
    	self.edit_model[wd][bindex][3] = \
    	                            self.edit_name[wd][bindex1].get_text()
    	self.edit_model[wd][bindex][4] = \
    	                            self.edit_company[wd][bindex1].get_text()
    	self.edit_model[wd][bindex][5] = self.edit_email[wd][bindex1].get_text()
    	self.edit_model[wd][bindex][6] = self.edit_phone[wd][bindex1].get_text()
        
        if index == (len(self.edit_model[wd]) - 1): forward = 0
        else: forward = index
        
        self.edit_model[wd].pop(index)
               
        self.editFormEl(wd, forward)        
    
    def editFormOk(self, empty, wd, index, bindex1):
        
        sername = self.edit_sername[wd][bindex1].get_text()
        name    = self.edit_name[wd][bindex1].get_text()
        company = self.edit_company[wd][bindex1].get_text()
        email   = self.edit_email[wd][bindex1].get_text()
        phone   = self.edit_phone[wd][bindex1].get_text()
        
        if name != '' or sername != '' or email != '' or phone != '' \
           or company != '':
        	
        	result = self.Customer.update(self.edit_model[wd][index][0], 
        	                               sername, name, company, email, phone)
        						    
        	if result == False:
        	    self.message.set_text('Ошибка клиент не отредоктирован')
        	    gobject.timeout_add(10000, self.messageClear)
        	else:
        	    self.message.set_text('')
        	    k = 0
        	    for i in self.liststore:
        	        if i[0] == self.edit_model[wd][index][0]: break
        	        k += 1 
        	        
        	    self.liststore[k][2] = sername
        	    self.liststore[k][3] = name
        	    self.liststore[k][4] = company
        	    self.liststore[k][5] = email
        	    self.liststore[k][6] = phone
       	
       	if len(self.edit_model[wd]) == 1: 
            self.edit_dialog[wd].destroy()
            return
        
        if bindex1 == 0: 
            bindex1 = 1
            bindex = index + 1
            if bindex == len(self.edit_model[wd]): bindex = 0
        else: 
            bindex1 = 0
            bindex = index - 1
        
        self.edit_model[wd][bindex][2] = \
                                    self.edit_sername[wd][bindex1].get_text()
    	self.edit_model[wd][bindex][3] = self.edit_name[wd][bindex1].get_text()
    	self.edit_model[wd][bindex][4] = \
    	                            self.edit_company[wd][bindex1].get_text()
    	self.edit_model[wd][bindex][5] = self.edit_email[wd][bindex1].get_text()
    	self.edit_model[wd][bindex][6] = self.edit_phone[wd][bindex1].get_text()
        
        if index == (len(self.edit_model[wd]) - 1): forward = 0
        else: forward = index
        
        self.edit_model[wd].pop(index)
                
        self.editFormEl(wd, forward)				        
    
    def viewForm(self, tp = 0):
    
    	wd = len(self.view_dialog)
        self.view_dialog.append(wd)
        
        self.view_dialog[wd] = gtk.Dialog()
        self.view_dialog[wd].set_border_width(10)
        self.view_dialog[wd].move(self.Window.get_position()[0] + 150 + 
        						  random.randrange(30), 
        						  self.Window.get_position()[1] + 150 + 
        						  random.randrange(30))
        self.view_dialog[wd].set_has_separator(False)
        self.view_dialog[wd].set_resizable(False)
        self.view_dialog[wd].set_skip_taskbar_hint(True)  
        self.view_dialog[wd].set_icon_from_file(sys.path[0] + 
        									    '/images/logotip.png')
        
        self.view_box.append(wd)
        self.view_box[wd] = None
        
        self.view_model.append(wd)
        
        temp = []
        if tp == 0: temp = [i for i in self.liststore if i[1] == True]
        else: 
            model, model1 = self.treeselection.get_selected_rows()
            k = [j[0] for j in model1]
            for i in range(len(model)):
                if i in k: temp.append(model[i])
        
        self.view_model[wd] = []
        for i in temp:
        	self.view_model[wd].append([j for j in i])
                
        hbox1 = self.viewFormEl(wd, 0)
        
    def viewFormEl(self, wd, index):
        
        if self.view_box[wd] != None: self.view_box[wd].destroy()
                             
        temp  = [i for i in self.liststore]        
        temp2 = [i for i in self.view_model[wd]]
        
        k = 0
        for i in temp2:
            if k == index: 
                vindex = i[0]
                break
            k += 1
        
        k = 0        
        for i in temp2:
            k1 = 0
            for j in temp:       
                if i[0] == j[0]:
                    k1 = 1
                    break  
            if k1 == 0: 
                self.view_model[wd].pop(k)
                k -= 1
            k += 1  
               
        if len(self.view_model[wd]) == 0: 
            self.view_dialog[wd].destroy()
            return
        
        k2 = index
        k1 = 0    
        temp2 = [i for i in self.view_model[wd]]
        for i in temp2:
            if vindex == i[0]:
                index = k1 
                break             
            k1 += 1
        
        if k2 == index:
            if index >= len(self.view_model[wd]): 
                                            index = len(self.view_model[wd]) - 1          
                                            
        box = gtk.HBox()
        
        if len(self.view_model[wd]) < 2: l = 1
        elif len(self.view_model[wd]) < 3: l = 2
        else: l = 3
                
        for i in range(l):
            
            if l == 1: 
                self.view_dialog[wd].set_title('Просмотр клиента')                
            else: self.view_dialog[wd].set_title('Просмотр клиентов')
            
            if (index + i) == len(self.view_model[wd]): k = 0
            elif (index + i - 1) == len(self.view_model[wd]): k = 1
            else: k = index + i
                         
            arr = self.view_model[wd][k]
                        
            frame = gtk.Frame(' ' + arr[2] + ' ' + arr[3] + ' ')
            frame.set_border_width(3)
            table = gtk.Table(2, 5, False)
            table.set_border_width(5)
            table.set_row_spacings(10)
            table.set_col_spacings(10)
                                    
            label = gtk.Label('Фамилия:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
            
           
            if arr[2] != '': 
                view_sername = gtk.Label(arr[2])
                view_sername.set_selectable(True)
                view_sername.set_alignment(0, 0.5)
                table.attach(view_sername, 1, 2, 0, 1, yoptions = gtk.FILL)
            
            label = gtk.Label('Имя:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
            
            if arr[3] != '': 
                view_name = gtk.Label(arr[3])
                view_name.set_alignment(0, 0.5)
                view_name.set_selectable(True)
                table.attach(view_name, 1, 2, 1, 2, yoptions = gtk.FILL)
            
            label = gtk.Label('Фирма:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
            
            if arr[4] != '': 
                view_company = gtk.Label(arr[4])
                view_company.set_selectable(True)
                view_company.set_alignment(0, 0.5)
                table.attach(view_company, 1, 2, 2, 3, yoptions = gtk.FILL)
                 
            label = gtk.Label('Email:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
            
            if arr[5] != '': 
                view_email = gtk.Label(arr[5])
                view_email.set_selectable(True)
                view_email.set_alignment(0, 0.5)
                table.attach(view_email, 1, 2, 3, 4, yoptions = gtk.FILL)
            
            label = gtk.Label('Телефон:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
            
            if arr[6] != '': 
                view_phone = gtk.Label(arr[6])
                view_phone.set_selectable(True)
                view_phone.set_alignment(0, 0.5)
                table.attach(view_phone, 1, 2, 4, 5, yoptions = gtk.FILL)
            
            frame.add(table)
            box.pack_start(frame)
        
        self.view_box[wd] = gtk.VBox()
        
        self.view_box[wd].pack_start(box)
        
        box1 = gtk.HBox()
        
        if len(self.view_model[wd]) > 3:
                    
            if index == (len(self.view_model[wd]) - 1): 
                back    = index - 1
                forward = 0
            elif index == 0:
                back    = len(self.view_model[wd]) - 1
                forward = index + 1 
            else:
                back    = index - 1
                forward = index + 1 
                    
            back_button = gtk.Button(stock = gtk.STOCK_GO_BACK)
            back_button.connect('clicked', lambda l: self.viewFormEl(wd, back))
            box1.pack_start(back_button, True, False)
                        
            forward_button = gtk.Button(stock = gtk.STOCK_GO_FORWARD)
            forward_button.connect('clicked', lambda l: 
                                              self.viewFormEl(wd, forward))
            box1.pack_start(forward_button, True, False)
        
        
        quit_button = gtk.Button(stock = gtk.STOCK_QUIT)
        quit_button.connect('clicked', lambda l: self.view_dialog[wd].destroy())
        box1.pack_start(quit_button, True, False)
                
        self.view_box[wd].pack_start(box1)    
                
        self.view_dialog[wd].vbox.pack_start(self.view_box[wd])
        self.view_dialog[wd].show_all()
    
    def messageClear(self):
    
        self.message.set_text('')
                                                      
