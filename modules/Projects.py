#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Projects module
'''

__author__    = 'r0n9.GOL (http://www.pamparam.net/ email:ron9.gol@gmail.com)'
__version__   = '$Revision: 1.0 $'
__date__      = '$Date: 2009/04/04 23:17:59 $'
__copyright__ = 'Copyright (c) 2009 r0n9.GOL'

import sys

import pygtk
pygtk.require('2.0')
import gtk

import pango
import random
import gobject
import time
import datetime

import classes.project as project
import classes.customer as customer
import classes.staff as staff

class CalendarEntry(gtk.HBox):

    def __init__ (self):
        
        gtk.HBox.__init__(self, False, 0)
        self.calendar = gtk.Calendar()
        self.calendar.display_options(gtk.CALENDAR_SHOW_HEADING |
                                      gtk.CALENDAR_SHOW_DAY_NAMES |
                                      gtk.CALENDAR_SHOW_WEEK_NUMBERS)
        self.entry = gtk.Entry()
        self.button = gtk.Button(label = '^')
        self.cwindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.cwindow.set_skip_taskbar_hint(True)
        self.current_date = datetime.date.today()
                       
        self.cwindow.set_position(gtk.WIN_POS_MOUSE)
        self.cwindow.set_decorated(False)
        self.cwindow.set_modal(True)
        self.cwindow.add(self.calendar)
                                          
        self.pack_start(self.entry, True, True, 0)
        self.pack_start(self.button, False, False, 0)
       
        self.__connectSignals()
        self.updateEntry()

    def __connectSignals(self):
    
        self.day_selected_handle        = self.calendar.connect('day-selected', 
                                                            self.updateEntry)
        self.day_selected_double_handle = self.calendar.connect(
                                                    'day-selected-double-click', 
                                                    self.hideWidget)
        self.clicked_handle             = self.button.connect('clicked', 
                                                              self.showWidget)
        self.activate                   = self.entry.connect('activate', 
                                                        self.updateCalendar)
        self.focus_out                  = self.entry.connect('focus-out-event', 
                                                            self.updateCalendar)
       
    def getText(self):
        
        text = time.mktime((self.current_date.year, self.current_date.month, 
                            self.current_date.day, 0, 0, 0, 0, 0, 0))
        
        return text
    
    def getEntryText(self):
    
        return self.entry.get_text()
        
    def setDate(self, date):
        
        self.current_date = date
        self.calendar.select_month(self.current_date.month - 1, 
                                   self.current_date.year)
        self.calendar.select_day(self.current_date.day)
        self.updateEntry()

    def hideWidget(self, *args):
    
        self.cwindow.hide_all()

    def showWidget(self, *args):
    
        self.cwindow.show_all()

    def updateEntry(self, *args):
        
        year, month, day = self.calendar.get_date()
        month = month + 1;
        
        if year < 1900: year = 1900
        
        self.current_date = datetime.date(year, month, day)
        text = self.current_date.strftime('%d/%m/%Y')
        
        self.entry.set_text(text)
        
    def updateCalendar(self, *args):
        
        try:
            dt = datetime.datetime.strptime(self.entry.get_text(), '%d/%m/%Y')
        except:
            try:
                dt = datetime.datetime.strptime(self.entry.get_text(), 
                                                '%d/%m/%y')
            except:
                dt = datetime.date.fromtimestamp(time.time())
           
        self.setDate(dt)

class Base:
        
    def __init__(self, MySql, window, ID):
                      
        self.Window = window
        
        self.Project = project.Project(MySql)
        self.Customer = customer.Customer(MySql)
        self.Staff = staff.Staff(MySql)
        
        self.ID = ID
        self.PID = int(self.Staff.getOne(self.ID, 'post'))
        
        ### veriables ###
        
        self.add_dialog = []
              
        self.add_name        = []
        self.add_info        = []
        self.add_datee       = []
        self.add_id_customer = []
        self.add_id_staff    = []
                        
        self.edit_dialog = []
        self.edit_box    = []
        self.edit_model  = []
        
        self.edit_name        = []
        self.edit_info        = []
        self.edit_datee       = []
        self.edit_status      = []
        self.edit_id_customer = []
        self.edit_id_staff    = []
        
        self.view_dialog = []
        self.view_box    = []
        self.view_model  = []
        
        self.projprog_dialog = []
              
        self.projprog_id_project  = []
        self.projprog_info        = []
        self.projprog_info_list   = []
        self.projprog_save_button = []
                
        ### end veriables ###
        
        self.box = gtk.VBox()
        self.box.set_border_width(10)
                    
        ### Title ###
                
        hbox = gtk.HBox()
                                    
        title_image = gtk.Image()
        title_image.set_from_file(sys.path[0] + '/images/project.png')
        hbox.pack_start(title_image, False)
        
        title_label = gtk.Label('Проекты')
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
        
        ### List customers ###
        
        list_frame = gtk.Frame(' Список проектов ')
        list_frame.set_border_width(3)
        
        table = gtk.Table(3, 2, False)
        table.set_row_spacings(10)
        table.set_border_width(10)
                
        self.liststore = gtk.ListStore(int, bool, str, str, str, str, 
                                       str, str)
        
        list_scrolled = gtk.ScrolledWindow()
        list_scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        listof = gtk.TreeView(self.liststore)
        listof.set_reorderable(True)
        
        self.treeselection = listof.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_MULTIPLE)
        
        listof.connect("key_press_event", self.pressDel)
        
        id_column          = gtk.TreeViewColumn()
        toggle_column      = gtk.TreeViewColumn()
        name_column        = gtk.TreeViewColumn('Название')
        dates_column       = gtk.TreeViewColumn('Дата нач.')
        datee_column       = gtk.TreeViewColumn('Дата оконч.')
        status_column      = gtk.TreeViewColumn('Статус')
        id_customer_column = gtk.TreeViewColumn('Клиент')
        id_staff_column    = gtk.TreeViewColumn('Архитектор')
                
        id_column.set_visible(False)
        toggle_column.set_min_width(20)
        toggle_column.set_clickable(True)
        
        name_column.set_resizable(True)
        name_column.set_expand(True)
        name_column.set_sort_column_id(2)
        
        dates_column.set_sort_column_id(3)
        
        datee_column.set_sort_column_id(4)
        
        status_column.set_sort_column_id(5)
        id_customer_column.set_sort_column_id(6)
        id_customer_column.set_resizable(True)
        id_staff_column.set_sort_column_id(7)
        id_staff_column.set_resizable(True)
                                       
        toggle_column.connect('clicked', self.idAllToggled)
        self.toggle_all_toggled = False
        
        listof.append_column(id_column)                
        listof.append_column(toggle_column)        
        listof.append_column(name_column)
        listof.append_column(dates_column)
        listof.append_column(datee_column)
        listof.append_column(status_column)
        listof.append_column(id_customer_column)
        listof.append_column(id_staff_column)
                                        
        id_cell          = gtk.CellRendererText()
        toggle_cell      = gtk.CellRendererToggle()
        name_cell        = gtk.CellRendererText()
        dates_cell       = gtk.CellRendererText()
        datee_cell       = gtk.CellRendererText()
        status_cell      = gtk.CellRendererText()
        id_customer_cell = gtk.CellRendererText()
        id_staff_cell    = gtk.CellRendererText()
                        
        toggle_cell.set_property('activatable', True)
        toggle_cell.connect('toggled', self.idToggled, self.liststore)
        
        if self.PID == 0 or self.PID == 2:
            
            name_cell.set_property('editable', True)
            name_cell.connect('edited', self.edit, self.liststore, 2)
                               
        id_column.pack_start(id_cell, True)
        toggle_column.pack_start(toggle_cell, True)
        name_column.pack_start(name_cell, True)
        dates_column.pack_start(dates_cell, True)
        datee_column.pack_start(datee_cell, True)
        status_column.pack_start(status_cell, True)
        id_customer_column.pack_start(id_customer_cell, True)
        id_staff_column.pack_start(id_staff_cell, True)
                
        id_column.set_attributes(id_cell, text = 0)
        toggle_column.add_attribute(toggle_cell, 'active', 1) 
        name_column.set_attributes(name_cell, text = 2)
        dates_column.set_attributes(dates_cell, text = 3)
        datee_column.set_attributes(datee_cell, text = 4)
        status_column.set_attributes(status_cell, text = 5)
        id_customer_column.set_attributes(id_customer_cell, text = 6)
        id_staff_column.set_attributes(id_staff_cell, text = 7)
        
        status_column.set_cell_data_func(status_cell, self.colorCell)
                       
        list_scrolled.add(listof)
        
        table.attach(list_scrolled, 0, 2, 0, 1)
        
        ### End List ###
                
        ### Action list ###
        
        hbox = gtk.HBox()
        
        if self.PID == 0 or self.PID == 2:
            
            self.add_button = gtk.Button(stock = gtk.STOCK_ADD)
            self.add_button.connect('clicked', self.addForm)
            hbox.pack_start(self.add_button, False, False) 
        
        if self.PID == 0 or self.PID == 5:
            
            self.projprog_button = gtk.Button(label = ' Ход проектов ')
            self.projprog_button.connect('clicked', self.projprogForm) 
            hbox.pack_start(self.projprog_button, False, False)
        
        alignment = gtk.Alignment(1.0)
        alignment.add(hbox)
        
        table.attach(alignment, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
                
        hbox = gtk.HBox()
        
        self.action_combobox = gtk.combo_box_new_text()
        
        self.action_combobox.append_text('Посмотреть')
        
        if self.PID == 0 or self.PID == 2:
        
            self.action_combobox.append_text('Редактировать')
            self.action_combobox.append_text('Удалить')
            self.action_combobox.append_text('Статус: Выполнен')
            self.action_combobox.append_text('Статус: В процессе')
        
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
        
    def colorCell(self, col, cell, model, iter):

        if model[iter][5] == self.Project.getStatus(0):
            cell.set_property("foreground", "red")
        else:
            cell.set_property("foreground", "green")
            
    def pressDel(self, empty, event):
    
        if gtk.gdk.keyval_name(event.keyval) == 'Delete' and \
           (self.PID == 0 or self.PID == 2):
            model, model1 = self.treeselection.get_selected_rows()
            k = 0
            for i in model1:
                result = self.Project.delete(self.liststore[i[0]-k][0])
                if result == False: 
                    self.message.set_text('Ошибка поле не удалено')
                    gobject.timeout_add(10000, self.messageClear)
                else: self.message.set_text('')
                
                iter = self.liststore.get_iter(i[0]-k)
                self.liststore.remove(iter)
                k += 1
            if len(self.liststore) == 0 and self.PID != 2: 
                self.projprog_button.set_sensitive(False)
            if len([i for i in self.liststore if i[1] == True]) == 0:
                self.action_combobox.set_sensitive(False)
                self.actionok_button.set_sensitive(False)
        elif gtk.gdk.keyval_name(event.keyval) == 'p': self.viewForm(1)
        elif gtk.gdk.keyval_name(event.keyval) == 'r' and \
           (self.PID == 0 or self.PID == 2): self.editForm(1)
        elif gtk.gdk.keyval_name(event.keyval) == 'a' and \
           (self.PID == 0 or self.PID == 2): self.addForm()
        elif gtk.gdk.keyval_name(event.keyval) == 'h' and \
           (self.PID == 0 or self.PID == 5): self.projprogForm()
        
    def gO(self):
               
        return self.box   
    
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
        
        self.add_name.append(wd)
        self.add_datee.append(wd)
        self.add_id_customer.append(wd)
        self.add_id_staff.append(wd)
        self.add_info.append(wd)
        
        self.add_dialog[wd] = gtk.Dialog('Добавление проекта')
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
        
        label = gtk.Label('Название:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
        
        self.add_name[wd] = gtk.Entry()
        self.add_name[wd].grab_focus()
        table.attach(self.add_name[wd], 1, 2, 0, 1, yoptions = gtk.FILL)
        
        label = gtk.Label('Дата окончания:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
        
        self.add_datee[wd] = CalendarEntry()
        table.attach(self.add_datee[wd], 1, 2, 1, 2, yoptions = gtk.FILL)      
        
        label = gtk.Label('Клиент:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
        
        liststore = gtk.ListStore(str, int)
        self.add_id_customer[wd] = gtk.combo_box_new_text()
        self.add_id_customer[wd].set_model(liststore)
        
        result = self.Customer.get()
        
        if len(result):
            for arr in result:
                liststore.append([arr[1] + ' ' + arr[2], int(arr[0])])
                
            self.add_id_customer[wd].set_active(0)
        
        table.attach(self.add_id_customer[wd], 1, 2, 2, 3, yoptions = gtk.FILL)
                               
        label = gtk.Label('Архитектор:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
        
        liststore = gtk.ListStore(str, int)
        self.add_id_staff[wd] = gtk.combo_box_new_text()
        self.add_id_staff[wd].set_model(liststore)
        
        result = self.Staff.getArh()
        
        if len(result):
            for arr in result:
                liststore.append([arr[1] + ' ' + arr[2], int(arr[0])])
            
            self.add_id_staff[wd].set_active(0)
        
        table.attach(self.add_id_staff[wd], 1, 2, 3, 4, yoptions = gtk.FILL)
        
        label = gtk.Label('Информация:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
        
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add_info[wd] = gtk.TextBuffer()
        textview = gtk.TextView()
        textview.set_buffer(self.add_info[wd])
        textview.set_size_request(-1, 100)
        textview.set_pixels_above_lines(5)
        textview.set_pixels_below_lines(5)
        textview.set_left_margin(5)
        textview.set_right_margin(5)
        scrolled.add(textview)
        table.attach(scrolled, 1, 2, 4, 5, yoptions = gtk.FILL)
        
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
        
        name  = self.add_name[wd].get_text()
        datee = self.add_datee[wd].getText()
        
        model = self.add_id_customer[wd].get_model()
        if len(model) > 0:
            index = self.add_id_customer[wd].get_active()
            id_customer = model[index][1]
        else: id_customer = 0
        
        model = self.add_id_staff[wd].get_model()
        if len(model) > 0:
            index = self.add_id_staff[wd].get_active()
            id_staff = model[index][1]
        else: id_staff = 0
        
        info = self.add_info[wd].get_text(self.add_info[wd].get_start_iter(),
                                          self.add_info[wd].get_end_iter())
        
        temp  = datetime.datetime.now()
        dates = time.mktime((temp.year, temp.month, 
                             temp.day, temp.hour, temp.minute, 0, 0, 0, 0))
                                     
        if name != '' or info != '':
            
            result = self.Project.add(name, info, str(dates), str(datee), '0', 
                                      str(id_customer), str(id_staff))
                                        
            if result == False:    
                self.message.set_text('Ошибка проект не добавлен')
                gobject.timeout_add(10000, self.messageClear)
            else:
                self.message.set_text('')
                sername = self.Customer.getOne(id_customer, 'sername')
                if sername == False:
                    customer = ''
                else: 
                    customer = sername + ' ' + \
                               self.Customer.getOne(id_customer, 'name')
                
                sername = self.Staff.getOne(id_staff, 'sername')
                if sername == False: staff = ''
                else:
                    staff = sername + \
                            ' ' + self.Staff.getOne(id_staff, 'name')

                status = self.Project.getStatus(0)
                datee  = self.getNormalDateTime(datee)
                dates  = self.getNormalDateTime(dates, 1)
                self.liststore.append([result, False, 
                                       name, dates, datee, status, 
                                       str(customer), str(staff)])
                
                if self.PID != 2: self.projprog_button.set_sensitive(True)
                
        self.add_dialog[wd].destroy()
    
    def addFormCancel(self, empty, wd):
        
        self.add_dialog[wd].destroy() 
            
    def getList(self):
        
        if self.PID == 5: 
            result = self.Project.get(None, self.ID)
        else: result = self.Project.get()
        
        if len(result):
            model = [i[0] for i in self.liststore]
            for arr in result:
                if model.count(int(arr[0])) == 0:
                    sername = self.Customer.getOne(arr[6], 'sername')
                    if sername == False:
                        customer = ''
                    else: 
                        customer = sername + ' ' + \
                                   self.Customer.getOne(arr[6], 'name')
                    
                    sername = self.Staff.getOne(arr[7], 'sername')
                    if sername == False: staff = ''
                    else:
                        staff = sername + \
                                ' ' + self.Staff.getOne(arr[7], 'name')
                    status = self.Project.getStatus(int(arr[5]))
                    
                    dates = self.getNormalDateTime(arr[3], 1)
                    datee = self.getNormalDateTime(arr[4])
                     
                    self.liststore.append([int(arr[0]), False,
                                           arr[1], dates, datee,
                                           status, str(customer), 
                                           str(staff)])
                                        
            model1 = [int(i[0]) for i in result]
            j = 0
            for i in range(len(model)):
                if model1.count(model[i]) == 0:
                    i = i - j
                    iter = self.liststore.get_iter(i)
                    self.liststore.remove(iter)
                    j += 1
            
            for i in range(len(self.liststore)):
                status = self.Project.getOne(self.liststore[i][0], 'status')
                if self.liststore[i][5] != self.Project.getStatus(status):
                    self.liststore[i][5] = self.Project.getStatus(int(status))
                                                                
        else: 
            self.liststore.clear()
        
        model = [i[0] for i in self.liststore if i[1] == True]
        
        if len(model) > 0:
            self.action_combobox.set_sensitive(True)
            self.actionok_button.set_sensitive(True)
        else:
            self.action_combobox.set_sensitive(False)
            self.actionok_button.set_sensitive(False)
        
        model = [i[0] for i in self.liststore]
        
        if self.PID == 0 or self.PID == 5:
            if len(model) > 0: self.projprog_button.set_sensitive(True)
            else: self.projprog_button.set_sensitive(False)
                                   
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
            result = self.Project.makeIn(model)
            if result == False: 
                self.message.set_text('Ошибка удаления')  
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()
        elif action == 'Статус: Выполнен':
            model = [i[0] for i in self.liststore if i[1] == True]
            result = self.Project.makeIn(model, 1)
            if result == False: 
                self.message.set_text('Ошибка изменения статуса')  
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()                 
        elif action == 'Статус: В процессе':
            model = [i[0] for i in self.liststore if i[1] == True]
            result = self.Project.makeIn(model, 2)
            if result == False: 
                self.message.set_text('Ошибка изменения статуса')  
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList() 
            
    def edit(self, cell, row, new_text, liststore, coll):
        
        liststore[row][coll] = new_text
        
        result = self.Project.updateOne(str(liststore[row][0]), 
                                         self.getNameField(coll), new_text)
                                          
        if result == False: 
            self.message.set_text('Ошибка поле не изменино')
            gobject.timeout_add(10000, self.messageClear)
        else: self.message.set_text('')
                   
    def getNameField(self, coll):
        
        if coll == 2: field = 'name'        
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
            temp1 = [j for j in i]
            temp1.append(self.Project.getOne(temp1[0], 'info'))
            self.edit_model[wd].append(temp1)
        
        for i in range(len(self.edit_model[wd])):
            self.edit_model[wd][i][6] = self.Project.getOne(
                                                    self.edit_model[wd][i][0], 
                                                    'id_customer')
            self.edit_model[wd][i][7] = self.Project.getOne(
                                                    self.edit_model[wd][i][0], 
                                                    'id_staff')
            
        self.edit_name.append(wd)
        self.edit_datee.append(wd)
        self.edit_status.append(wd)
        self.edit_id_customer.append(wd)
        self.edit_id_staff.append(wd)
        self.edit_info.append(wd)
        
        hbox1 = self.editFormEl(wd, 0)
        
    def editFormEl(self, wd, index, bindex = None):
        
        if self.edit_box[wd] != None: self.edit_box[wd].destroy()
                     
        if bindex != None:

            model  = self.edit_status[wd][0].get_model()
            index1 = self.edit_status[wd][0].get_active()
            status = model[index1][0]
            
            model  = self.edit_id_customer[wd][0].get_model()
            if len(model) > 0:
                index1 = self.edit_id_customer[wd][0].get_active()
                id_customer = model[index1][1]
            else: id_customer = 0
            
            model = self.edit_id_staff[wd][0].get_model()
            if len(model) > 0:
                index1 = self.edit_id_staff[wd][0].get_active()
                id_staff = model[index1][1]
            else: id_staff = 0
            
            info = self.edit_info[wd][0].get_text(
                                        self.edit_info[wd][0].get_start_iter(),
                                        self.edit_info[wd][0].get_end_iter())
            
            self.edit_model[wd][bindex - 1][2] = \
                                            self.edit_name[wd][0].get_text()
            self.edit_model[wd][bindex - 1][4] = \
                                        self.edit_datee[wd][0].getEntryText()
            
            self.edit_model[wd][bindex - 1][5] = status
            self.edit_model[wd][bindex - 1][6] = id_customer
            self.edit_model[wd][bindex - 1][7] = id_staff
            self.edit_model[wd][bindex - 1][8] = info

            model  = self.edit_status[wd][1].get_model()
            index1 = self.edit_status[wd][1].get_active()
            status = model[index1][0]

            model       = self.edit_id_customer[wd][1].get_model()
            if len(model) > 0:
                index1      = self.edit_id_customer[wd][1].get_active()
                id_customer = model[index1][1]
            else: id_customer = 0
            
            model    = self.edit_id_staff[wd][1].get_model()
            if len(model) > 0:
                index1   = self.edit_id_staff[wd][1].get_active()
                id_staff = model[index1][1]
            else: id_staff = 0
            
            info = self.edit_info[wd][1].get_text(
                                        self.edit_info[wd][1].get_start_iter(),
                                        self.edit_info[wd][1].get_end_iter())

            self.edit_model[wd][bindex][2] = self.edit_name[wd][1].get_text()
            self.edit_model[wd][bindex][4] = \
                                        self.edit_datee[wd][1].getEntryText()
            self.edit_model[wd][bindex][5] = status
            self.edit_model[wd][bindex][6] = id_customer
            self.edit_model[wd][bindex][7] = id_staff
            self.edit_model[wd][bindex][8] = info

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
        
        self.edit_name[wd]        = [0, 1]
        self.edit_datee[wd]       = [0, 1]
        self.edit_status[wd]      = [0, 1]
        self.edit_id_customer[wd] = [0, 1]
        self.edit_id_staff[wd] = [0, 1]
        self.edit_info[wd]        = [0, 1]
                                                    
        box = gtk.HBox()
        
        if len(self.edit_model[wd]) < 2: l = 1
        else: l = 2
                
        for i in range(l):
            
            if l == 1: self.edit_dialog[wd].set_title('Редактирование проекта')
            else: self.edit_dialog[wd].set_title('Редактирование проектов')
            
            if (index + i) == len(self.edit_model[wd]): k = 0
            else: k = index + i
                         
            arr = self.edit_model[wd][k]
           
            frame = gtk.Frame(' ' + arr[2] + ' ')
            frame.set_border_width(3)                
            table = gtk.Table(2, 7, False)
            table.set_border_width(5)
            table.set_row_spacings(10)
            table.set_col_spacings(10)        
                                    
            label = gtk.Label('Название:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
            
            self.edit_name[wd][i] = gtk.Entry()
            self.edit_name[wd][i].set_text(arr[2])
            if i == 0: self.edit_name[wd][i].grab_focus()
            table.attach(self.edit_name[wd][i], 1, 2, 0, 1, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Дата окончания:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
            
            self.edit_datee[wd][i] = CalendarEntry()
            self.edit_datee[wd][i].setDate(datetime.datetime.strptime(arr[4], 
                                                                    '%d/%m/%Y'))
            table.attach(self.edit_datee[wd][i], 1, 2, 1, 2, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Статус:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
            
            liststore = gtk.ListStore(str, int)
            self.edit_status[wd][i] = gtk.combo_box_new_text()
            self.edit_status[wd][i].set_model(liststore)
            
            liststore.append([self.Project.getStatus(0), 0])
            liststore.append([self.Project.getStatus(1), 1])
            
            for j in range(2):
                if self.Project.getStatus(j) == arr[5]: break
                  
            self.edit_status[wd][i].set_active(j)
            
            table.attach(self.edit_status[wd][i], 1, 2, 2, 3, 
                         yoptions = gtk.FILL)
                        
            label = gtk.Label('Клиент:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
            
            liststore = gtk.ListStore(str, int)
            self.edit_id_customer[wd][i] = gtk.combo_box_new_text()
            self.edit_id_customer[wd][i].set_model(liststore)
            
            result = self.Customer.get()
            
            if len(result):
                k1 = 0
                for arr1 in result:
                    liststore.append([arr1[1] + ' ' + arr1[2], int(arr1[0])])
                    if int(arr1[0]) == int(arr[6]):
                        self.edit_id_customer[wd][i].set_active(k1)
                    k1 += 1
                            
            table.attach(self.edit_id_customer[wd][i], 1, 2, 3, 4, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Архитектор:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
            
            liststore = gtk.ListStore(str, int)
            self.edit_id_staff[wd][i] = gtk.combo_box_new_text()
            self.edit_id_staff[wd][i].set_model(liststore)
            
            result = self.Staff.getArh()
            
            if len(result):
                k1 = 0
                for arr1 in result:
                    liststore.append([arr1[1] + ' ' + arr1[2], int(arr1[0])])
                    if int(arr1[0]) == int(arr[7]):
                        self.edit_id_staff[wd][i].set_active(k1)
                    k1 += 1
                            
            table.attach(self.edit_id_staff[wd][i], 1, 2, 4, 5, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Информация:')
            label.set_alignment(0, 0)
            table.attach(label, 0, 1, 5, 6, yoptions = gtk.FILL)
            
            scrolled = gtk.ScrolledWindow()
            scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            self.edit_info[wd][i] = gtk.TextBuffer()
            self.edit_info[wd][i].set_text(arr[8])
            textview = gtk.TextView()
            textview.set_buffer(self.edit_info[wd][i])
            textview.set_size_request(-1, 100)
            textview.set_pixels_above_lines(5)
            textview.set_pixels_below_lines(5)
            textview.set_left_margin(5)
            textview.set_right_margin(5)
            scrolled.add(textview)
            table.attach(scrolled, 1, 2, 5, 6, yoptions = gtk.FILL)
            
            hbox = gtk.HBox()
            
            ok_button = gtk.Button(stock = gtk.STOCK_OK)
            ok_button.connect('clicked', self.editFormOk, wd, k, i)
            hbox.pack_start(ok_button)
            
            cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
            cancel_button.connect('clicked', self.editFormCancel, wd, k, i)
            hbox.pack_start(cancel_button)
            
            table.attach(hbox, 0, 1, 6, 7, yoptions = gtk.FILL)         
            
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
        
        model = self.edit_status[wd][bindex1].get_model()
        index1 = self.edit_status[wd][bindex1].get_active()
        status = model[index1][0]

        model = self.edit_id_customer[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_customer[wd][bindex1].get_active()
            id_customer = model[index1][1]
        else: id_customer = 0
        
        model = self.edit_id_staff[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_staff[wd][bindex1].get_active()
            id_staff = model[index1][1]
        else: id_staff = 0

        info = self.edit_info[wd][bindex1].get_text(
                                self.edit_info[wd][bindex1].get_start_iter(),
                                self.edit_info[wd][bindex1].get_end_iter())

        self.edit_model[wd][bindex][2] = self.edit_name[wd][bindex1].get_text()
        self.edit_model[wd][bindex][4] = \
                                    self.edit_datee[wd][bindex1].getEntryText()
        self.edit_model[wd][bindex][5] = status
        self.edit_model[wd][bindex][6] = id_customer
        self.edit_model[wd][bindex][7] = id_staff
        self.edit_model[wd][bindex][8] = info
        
        if index == (len(self.edit_model[wd]) - 1): forward = 0
        else: forward = index
        
        self.edit_model[wd].pop(index)
               
        self.editFormEl(wd, forward)        
    
    def editFormOk(self, empty, wd, index, bindex1):
        
        name  = self.edit_name[wd][bindex1].get_text()
        datee = self.edit_datee[wd][bindex1].getText()
        
        model = self.edit_status[wd][bindex1].get_model()
        index1 = self.edit_status[wd][bindex1].get_active()
        status = model[index1][1]
        
        model = self.edit_id_customer[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_customer[wd][bindex1].get_active()
            id_customer = model[index1][1]
        else: id_customer = 0
        
        model = self.edit_id_staff[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_staff[wd][bindex1].get_active()
            id_staff = model[index1][1]
        else: id_staff = 0
        
        info = self.edit_info[wd][bindex1].get_text(
                                self.edit_info[wd][bindex1].get_start_iter(),
                                self.edit_info[wd][bindex1].get_end_iter())

        if name != '' or info != '':
            
            result = self.Project.update(self.edit_model[wd][index][0], name, 
                                         info, str(datee), str(status), 
                                         str(id_customer), str(id_staff))

            if result == False:
                self.message.set_text('Ошибка проект не отредоктирован')
                gobject.timeout_add(10000, self.messageClear)
            else:
                self.message.set_text('')
                k = 0
                for i in self.liststore:
                    if i[0] == self.edit_model[wd][index][0]: break
                    k += 1
                    
                sername = self.Customer.getOne(id_customer, 'sername')
                if sername == False:
                    customer = ''
                else: 
                    customer = sername + ' ' + \
                               self.Customer.getOne(id_customer, 'name')
                
                sername = self.Staff.getOne(id_staff, 'sername')
                if sername == False: staff = ''
                else:
                    staff = sername + \
                            ' ' + self.Staff.getOne(id_staff, 'name')

                self.liststore[k][2] = name
                self.liststore[k][4] = self.getNormalDateTime(datee)
                self.liststore[k][5] = self.Project.getStatus(status)
                self.liststore[k][6] = customer
                self.liststore[k][7] = staff
           
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
        
        model = self.edit_status[wd][bindex1].get_model()
        index1 = self.edit_status[wd][bindex1].get_active()
        status = model[index1][0]

        model = self.edit_id_customer[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_customer[wd][bindex1].get_active()
            id_customer = model[index1][1]
        else: id_customer = 0
        
        model = self.edit_id_staff[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_staff[wd][bindex1].get_active()
            id_staff = model[index1][1]
        else: id_staff = 0
        
        info = self.edit_info[wd][bindex1].get_text(
                                self.edit_info[wd][bindex1].get_start_iter(),
                                self.edit_info[wd][bindex1].get_end_iter())

        self.edit_model[wd][bindex][2] = self.edit_name[wd][bindex1].get_text()
        self.edit_model[wd][bindex][4] = \
                                    self.edit_datee[wd][bindex1].getEntryText()
        self.edit_model[wd][bindex][5] = status
        self.edit_model[wd][bindex][6] = id_customer
        self.edit_model[wd][bindex][7] = id_staff
        self.edit_model[wd][bindex][8] = info
        
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
            temp1 = [j for j in i]
            temp1.append(self.Project.getOne(temp1[0], 'info'))
            self.view_model[wd].append(temp1)
                
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
        else: l = 2
                
        for i in range(l):
            
            if l == 1: self.view_dialog[wd].set_title('Просмотр проекта')
            else: self.view_dialog[wd].set_title('Просмотр проектов')
            
            if (index + i) == len(self.view_model[wd]): k = 0
            else: k = index + i
                         
            arr = self.view_model[wd][k]
                        
            frame = gtk.Frame(' ' + arr[2] + ' ')
            frame.set_border_width(3)                
            table = gtk.Table(2, 7, False)
            table.set_border_width(5)
            table.set_row_spacings(10)
            table.set_col_spacings(10)        
                                    
            label = gtk.Label('Название:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
            
            if arr[2] != '':
                view_name = gtk.Label(arr[2])
                view_name.set_alignment(0, 0.5)
                view_name.set_selectable(True)
                table.attach(view_name, 1, 2, 0, 1, yoptions = gtk.FILL)
            
            label = gtk.Label('Дата начала:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
            
            view_dates = gtk.Label(arr[3])
            view_dates.set_alignment(0, 0.5)
            view_dates.set_selectable(True)
            table.attach(view_dates, 1, 2, 1, 2, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Дата окончания:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
            
            view_datee = gtk.Label(arr[4])
            view_datee.set_selectable(True)
            view_datee.set_alignment(0, 0.5)
            table.attach(view_datee, 1, 2, 2, 3, yoptions = gtk.FILL)
            
            label = gtk.Label('Статус:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
            
            view_status = gtk.Label(arr[5])
            view_status.set_selectable(True)
            view_status.set_alignment(0, 0.5)
            table.attach(view_status, 1, 2, 3, 4, 
                         yoptions = gtk.FILL)
                                    
            label = gtk.Label('Клиент:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
                        
            if arr[6] != '' and self.PID != 5: 
                
                view_id_customer = gtk.Label(arr[6])
                
                event_box = gtk.EventBox()
                event_box.connect('realize', lambda l: \
                        l.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2)))
                event_box.add(view_id_customer)
                event_box.connect('button_press_event', self.viewFormCustomer, 
                                  self.Project.getOne(arr[0], 'id_customer'))
        
                view_id_customer.set_alignment(0, 0.5)
                table.attach(event_box, 1, 2, 4, 5, yoptions = gtk.FILL)
            
            elif arr[6] != '' and self.PID == 5:
                
                view_id_customer = gtk.Label(arr[6])
                view_id_customer.set_selectable(True)
                view_id_customer.set_alignment(0, 0.5)
                table.attach(view_id_customer, 1, 2, 4, 5, yoptions = gtk.FILL)
                
            
            label = gtk.Label('Архитектор:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 5, 6, yoptions = gtk.FILL)
            
            if arr[7] != '' and self.PID != 5:
            
                view_id_staff = gtk.Label(arr[7])
                
                event_box = gtk.EventBox()
                event_box.connect('realize', lambda l: \
                        l.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2)))
                event_box.add(view_id_staff)
                event_box.connect('button_press_event', self.viewFormStaff, 
                                  self.Project.getOne(arr[0], 'id_staff'))
                
        
                view_id_staff.set_alignment(0, 0.5)
                table.attach(event_box, 1, 2, 5, 6, yoptions = gtk.FILL)
            
            elif arr[7] != '' and self.PID == 5:
                
                view_id_staff = gtk.Label(arr[7])
                view_id_staff.set_selectable(True)
                view_id_staff.set_alignment(0, 0.5)
                table.attach(view_id_staff, 1, 2, 5, 6, yoptions = gtk.FILL)
            
            label = gtk.Label('Информация:')
            label.set_alignment(0, 0)
            table.attach(label, 0, 1, 6, 7, yoptions = gtk.FILL)
            
            scrolled = gtk.ScrolledWindow()
            scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            view_info = gtk.TextBuffer()
            view_info.set_text(arr[2])
            textview = gtk.TextView()
            textview.set_cursor_visible(False)
            textview.set_editable(False)
            textview.set_buffer(view_info)
            textview.set_size_request(200, 150)
            scrolled.add(textview)
            table.attach(scrolled, 1, 2, 6, 7, yoptions = gtk.FILL)
            
            expander = gtk.Expander('Ход проекта')
            scrolled = gtk.ScrolledWindow()
            scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            view_projprog = gtk.TextBuffer()
            view_projprog.set_text(self.Project.getProjprogInfo(arr[0]))
            textview = gtk.TextView()
            textview.set_cursor_visible(False)
            textview.set_editable(False)
            textview.set_buffer(view_projprog)
            textview.set_size_request(-1, 150)
            scrolled.add(textview)
            expander.add(scrolled)
            table.attach(expander, 0, 2, 7, 8, yoptions = gtk.FILL)
            
            frame.add(table)
            box.pack_start(frame)
        
        self.view_box[wd] = gtk.VBox()
        
        self.view_box[wd].pack_start(box)
        
        box1 = gtk.HBox()
        
        if len(self.view_model[wd]) > 2:
                    
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
    
    def getNormalDateTime(self, dt, watch = 0):
        
        temp = datetime.datetime.fromtimestamp(float(dt))
        
        if watch == 0: ndt = temp.strftime('%d/%m/%Y')
        elif watch == 1: ndt = temp.strftime('%d/%m/%Y %H:%M')
        
        return ndt
    
    def viewFormCustomer(self, empty, empty1, ids):
        
        view_dialog = gtk.Dialog()
        view_dialog.set_border_width(10)
        view_dialog.move(self.Window.get_position()[0] + 150 + 
                                  random.randrange(30), 
                                  self.Window.get_position()[1] + 150 + 
                                  random.randrange(30))
        view_dialog.set_has_separator(False)
        view_dialog.set_resizable(False)
        view_dialog.set_skip_taskbar_hint(True)  
        view_dialog.set_icon_from_file(sys.path[0] + 
                                       '/images/logotip.png')
        
        view_dialog.set_title('Просмотр клиента')                
            
        arr = self.Customer.get(ids)[0]
        
        frame = gtk.Frame(' ' + arr[1] + ' ' + arr[2] + ' ')
        frame.set_border_width(3)
        table = gtk.Table(2, 5, False)
        table.set_border_width(5)
        table.set_row_spacings(10)
        table.set_col_spacings(10)
                                
        label = gtk.Label('Фамилия:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
        
        if arr[1] != '': 
            view_sername = gtk.Label(arr[1])
            view_sername.set_selectable(True)
            view_sername.set_alignment(0, 0.5)
            table.attach(view_sername, 1, 2, 0, 1, yoptions = gtk.FILL)
        
        label = gtk.Label('Имя:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
    
        if arr[2] != '': 
            view_name = gtk.Label(arr[2])
            view_name.set_alignment(0, 0.5)
            view_name.set_selectable(True)
            table.attach(view_name, 1, 2, 1, 2, yoptions = gtk.FILL)
        
        label = gtk.Label('Фирма:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
        
        if arr[3] != '': 
            view_company = gtk.Label(arr[3])
            view_company.set_selectable(True)
            view_company.set_alignment(0, 0.5)
            table.attach(view_company, 1, 2, 2, 3, yoptions = gtk.FILL)
             
        label = gtk.Label('Email:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
        
        if arr[4] != '': 
            view_email = gtk.Label(arr[4])
            view_email.set_selectable(True)
            view_email.set_alignment(0, 0.5)
            table.attach(view_email, 1, 2, 3, 4, yoptions = gtk.FILL)
        
        label = gtk.Label('Телефон:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
        
        if arr[5] != '': 
            view_phone = gtk.Label(arr[5])
            view_phone.set_selectable(True)
            view_phone.set_alignment(0, 0.5)
            table.attach(view_phone, 1, 2, 4, 5, yoptions = gtk.FILL)
        
        box = gtk.VBox()
        
        frame.add(table)
        box.pack_start(frame)
        
        hbox = gtk.HBox() 
        
        quit_button = gtk.Button(stock = gtk.STOCK_QUIT)
        quit_button.connect('clicked', lambda l: view_dialog.destroy())
        hbox.pack_start(quit_button, True, False)
        
        box.pack_start(hbox)
        view_dialog.vbox.pack_start(box)
        view_dialog.show_all()
    
    def viewFormStaff(self, empty, empty1, ids):
        
        view_dialog = gtk.Dialog()
        view_dialog.set_border_width(10)
        view_dialog.move(self.Window.get_position()[0] + 150 + 
                                  random.randrange(30), 
                                  self.Window.get_position()[1] + 150 + 
                                  random.randrange(30))
        view_dialog.set_has_separator(False)
        view_dialog.set_resizable(False)
        view_dialog.set_skip_taskbar_hint(True)  
        view_dialog.set_icon_from_file(sys.path[0] + 
                                       '/images/logotip.png')
        
        view_dialog.set_title('Просмотр архитектора')

        arr = self.Staff.get(None, ids)[0]
        
        frame = gtk.Frame(' ' + arr[1] + ' '+ arr[2] + ' ')
        frame.set_border_width(3)
        table = gtk.Table(2, 8, False)
        table.set_border_width(5)
        table.set_row_spacings(10)
        table.set_col_spacings(10)        
                                
        label = gtk.Label('Фамилия:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
        
        if arr[1] != '': 
            view_sername = gtk.Label(arr[1])
            view_sername.set_alignment(0, 0.5)
            view_sername.set_selectable(True)
            table.attach(view_sername, 1, 2, 0, 1, yoptions = gtk.FILL)
        
        label = gtk.Label('Имя:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
        
        if arr[2] != '': 
            view_name = gtk.Label(arr[2])
            view_name.set_alignment(0, 0.5)
            view_name.set_selectable(True)
            table.attach(view_name, 1, 2, 1, 2, yoptions = gtk.FILL)
        
        label = gtk.Label('Должность:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
        
        view_post = gtk.Label(self.Staff.getPost(arr[3]))
        view_post.set_alignment(0, 0.5)
        view_post.set_selectable(True)
        table.attach(view_post, 1, 2, 2, 3, yoptions = gtk.FILL)
        
        label = gtk.Label('Зарплата:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
        
        if arr[5] != '': 
            view_wage = gtk.Label(arr[5])
            view_wage.set_selectable(True)
            view_wage.set_alignment(0, 0.5)
            table.attach(view_wage, 1, 2, 3, 4, yoptions = gtk.FILL)
        
        label = gtk.Label('Дата принятия на работу:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
        
        view_date = gtk.Label(self.getNormalDateTime(arr[4]))
        view_date.set_alignment(0, 0.5)
        view_date.set_selectable(True)
        table.attach(view_date, 1, 2, 4, 5, yoptions = gtk.FILL)
        
        label = gtk.Label('Email:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 5, 6, yoptions = gtk.FILL)
        
        if arr[6] != '': 
            view_email = gtk.Label(arr[6])
            view_email.set_selectable(True)
            view_email.set_alignment(0, 0.5)
            table.attach(view_email, 1, 2, 5, 6, yoptions = gtk.FILL)
        
        label = gtk.Label('Телефон:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 6, 7, yoptions = gtk.FILL)
        
        if arr[7] != '': 
            view_phone = gtk.Label(arr[7])
            view_phone.set_selectable(True)
            view_phone.set_alignment(0, 0.5)
            table.attach(view_phone, 1, 2, 6, 7, yoptions = gtk.FILL)

        label = gtk.Label('Логин:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 7, 8, yoptions = gtk.FILL)
        
        if arr[8] != '': 
            view_login = gtk.Label(arr[8])
            view_login.set_selectable(True)
            view_login.set_alignment(0, 0.5)
            table.attach(view_login, 1, 2, 7, 8, yoptions = gtk.FILL)
        
        label = gtk.Label('Статус:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 8, 9, yoptions = gtk.FILL)
        
        view_status = gtk.Label(self.Staff.getStatus(arr[10]))
        view_status.set_selectable(True)
        view_status.set_alignment(0, 0.5)
        table.attach(view_status, 1, 2, 8, 9, yoptions = gtk.FILL)
        
        box = gtk.VBox()
        
        frame.add(table)
        box.pack_start(frame)
        
        hbox = gtk.HBox() 
        
        quit_button = gtk.Button(stock = gtk.STOCK_QUIT)
        quit_button.connect('clicked', lambda l: view_dialog.destroy())
        hbox.pack_start(quit_button, True, False)
        
        box.pack_start(hbox)
        view_dialog.vbox.pack_start(box)
        view_dialog.show_all()
        
    def projprogForm(self, *args):
        
        wd = len(self.projprog_dialog)
        self.projprog_dialog.append(wd)
        
        self.projprog_id_project.append(wd)
        self.projprog_info.append(wd)
        self.projprog_info_list.append(wd)
        self.projprog_save_button.append(wd)
        self.projprog_info_list[wd] = []
        
        self.projprog_dialog[wd] = gtk.Dialog('Ход проектов')
        self.projprog_dialog[wd].move(self.Window.get_position()[0] + 150 + 
                                random.randrange(30), 
                                self.Window.get_position()[1] + 150 + 
                                random.randrange(30))
        self.projprog_dialog[wd].set_has_separator(False)
        self.projprog_dialog[wd].set_resizable(False)
        self.projprog_dialog[wd].set_skip_taskbar_hint(True)  
        self.projprog_dialog[wd].set_icon_from_file(sys.path[0] + 
                                                    '/images/logotip.png')
        
        self.projprog_dialog[wd].set_size_request(550, 400)
        
        table = gtk.Table(1, 3, False)
        table.set_border_width(5)
        table.set_row_spacings(10)
        table.set_col_spacings(10)
        
        liststore = gtk.ListStore(str, int)
        self.projprog_id_project[wd] = gtk.combo_box_new_text()
        self.projprog_id_project[wd].set_model(liststore)
        
        if self.PID == 5:
            result = self.Project.get(id_staff = self.ID)
        else: result = self.Project.get()
        
        id_project = 0
        if len(result):
            for arr in result:
                if id_project == 0: id_project = arr[0]
                liststore.append([arr[1], int(arr[0])])
                
                info = self.Project.getProjprogInfo(arr[0])
                self.projprog_info_list[wd].append(info)
            
            self.projprog_id_project[wd].set_active(0)
        
        table.attach(self.projprog_id_project[wd], 0, 1, 0, 1, 
                     yoptions = gtk.FILL)
        
        self.projprog_id_project[wd].connect('changed', self.changedProject, wd)
        
        info = self.Project.getProjprogInfo(id_project)

        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.projprog_info[wd] = gtk.TextBuffer()
        self.projprog_info[wd].set_text(info)
        textview = gtk.TextView()
        textview.set_buffer(self.projprog_info[wd])
        textview.set_size_request(-1, 100)
        textview.set_pixels_above_lines(5)
        textview.set_pixels_below_lines(5)
        textview.set_left_margin(5)
        textview.set_right_margin(5)
        scrolled.add(textview)
        table.attach(scrolled, 0, 1, 1, 2)
        
        self.projprog_info[wd].connect('changed', self.changedInfo, wd)
        
        hbox = gtk.HBox()
        
        self.projprog_save_button[wd] = gtk.Button(stock = gtk.STOCK_SAVE)
        self.projprog_save_button[wd].connect('clicked', self.projprogFormSave, 
                                              wd)
        hbox.pack_start(self.projprog_save_button[wd], False, False)
        
        self.projprog_save_button[wd].set_sensitive(False)
        
        ok_button = gtk.Button(stock = gtk.STOCK_OK)
        ok_button.connect('clicked', self.projprogFormOk, wd)
        hbox.pack_start(ok_button, False, False)
        
        cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
        cancel_button.connect('clicked', self.projprogFormCancel, wd)
        hbox.pack_start(cancel_button, False, False)
        
        table.attach(hbox, 0, 1, 2, 3, yoptions = gtk.FILL)
          
        self.projprog_dialog[wd].vbox.pack_start(table)
        self.projprog_dialog[wd].show_all()
        
    def projprogFormCancel(self, empty, wd):
            
        self.projprog_dialog[wd].destroy()
    
    def changedProject(self, combobox, wd):
        
        index = combobox.get_active()
        info = self.projprog_info_list[wd][index]
        
        self.projprog_info[wd].set_text(info)
        
        model = self.projprog_id_project[wd].get_model()
        id_project = model[index][1]
        
        if info != self.Project.getProjprogInfo(id_project):
            self.projprog_save_button[wd].set_sensitive(True)
        else:
            self.projprog_save_button[wd].set_sensitive(False)
        
    def projprogFormOk(self, empty, wd):
        
        model = self.projprog_id_project[wd].get_model()
        
        for i in range(len(model)):
            
            id_project = model[i][1]
            info = self.projprog_info_list[wd][i]
            result = self.Project.updateProjprogInfo(id_project, info)
        
            if result == False:    
                self.message.set_text('Ошибка не отредоктирован ход проекта')
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            
        self.projprog_dialog[wd].destroy()
    
    def projprogFormSave(self, empty, wd):
        
        model = self.projprog_id_project[wd].get_model()
        index = self.projprog_id_project[wd].get_active()
        id_project = model[index][1]
        
        info = self.projprog_info[wd].get_text(
                                    self.projprog_info[wd].get_start_iter(),
                                    self.projprog_info[wd].get_end_iter())
        
        result = self.Project.updateProjprogInfo(id_project, info)
        
        if result == False:    
            self.message.set_text('Ошибка не отредоктирован ход проекта')
            gobject.timeout_add(10000, self.messageClear)
        else:
            self.message.set_text('')
            self.projprog_save_button[wd].set_sensitive(False)
    
    def changedInfo(self, empty, wd):
        
        model = self.projprog_id_project[wd].get_model()
        index = self.projprog_id_project[wd].get_active()
        id_project = model[index][1]
        
        info = self.projprog_info[wd].get_text(
                                    self.projprog_info[wd].get_start_iter(),
                                    self.projprog_info[wd].get_end_iter())
        
        self.projprog_info_list[wd][index] = info
        
        if info != self.Project.getProjprogInfo(id_project):
            self.projprog_save_button[wd].set_sensitive(True)
        else:
            self.projprog_save_button[wd].set_sensitive(False)
