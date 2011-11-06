#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Accountancy module
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
import time
import datetime

import classes.accountancy as accountancy
import classes.staff as staff
import classes.project as project
import classes.customer as customer
from classes.staff import Staff

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
        self.current_date = datetime.datetime.now()
                       
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
                            self.current_date.day, self.current_date.hour - 1, 
                            self.current_date.minute, 0, 0, 0, 0))
        
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
        
        temp = str(self.current_date)
        temp = temp.split(' ')[1]
        hour = int(temp.split(':')[0])
        minute = int(temp.split(':')[1])
        
        if year < 1900: year = 1900
        
        self.current_date = datetime.datetime(year, month, day, hour, minute)
        text = self.current_date.strftime('%d/%m/%Y %H:%M')
        
        self.entry.set_text(text)
        
    def updateCalendar(self, *args):
        
        try:
            dt = datetime.datetime.strptime(self.entry.get_text(), 
                                            '%d/%m/%Y %H:%M')
        except:
            try:
                dt = datetime.datetime.strptime(self.entry.get_text(), 
                                                '%d/%m/%y %H:%M')
            except:
                dt = datetime.datetime.fromtimestamp(time.time())
           
        self.setDate(dt)

class Wage:

    def __init__(self, MySql, window, message, ID):
        
        self.Window = window
        
        self.message = message
        
        self.Accountancy = accountancy.Accountancy(MySql)
        self.Staff = staff.Staff(MySql)
        
        self.PID = int(Staff(MySql).getOne(ID, 'post'))
        
        self.add_dialog = []
                
        self.add_date     = []
        self.add_id_staff = []
        self.add_money    = []
        self.add_status   = []
        
        self.edit_dialog = []
        self.edit_box    = []
        self.edit_model  = []
        
        self.edit_date     = []
        self.edit_id_staff = []
        self.edit_money    = []
        self.edit_status   = []
        
        self.view_dialog = []
        self.view_box    = []
        self.view_model  = []
        
        ### List ###
        
        self.list_frame = gtk.Frame(' Список зарплаты ')
        self.list_frame.set_border_width(3)
        
        table = gtk.Table(3, 2, False)
        table.set_row_spacings(10)
        table.set_border_width(10)

        self.liststore = gtk.ListStore(int, bool, str, str, str, str)

        list_scrolled = gtk.ScrolledWindow()
        list_scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        listof = gtk.TreeView(self.liststore)
        listof.set_reorderable(True)
        
        self.treeselection = listof.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_MULTIPLE)
        
        listof.connect("key_press_event", self.pressDel)
        
        id_column       = gtk.TreeViewColumn()
        toggle_column   = gtk.TreeViewColumn()
        date_column     = gtk.TreeViewColumn('Дата')
        id_staff_column = gtk.TreeViewColumn('Фамилия Имя')
        money_column    = gtk.TreeViewColumn('Деньги')
        status_column   = gtk.TreeViewColumn('Статус')

        id_column.set_visible(False)
        toggle_column.set_min_width(20)
        toggle_column.set_clickable(True)
        date_column.set_sort_column_id(2)
        id_staff_column.set_resizable(True)
        id_staff_column.set_expand(True)
        id_staff_column.set_sort_column_id(3)
        money_column.set_resizable(True)
        money_column.set_sort_column_id(4)
        status_column.set_sort_column_id(5)

        toggle_column.connect('clicked', self.idAllToggled)
        self.toggle_all_toggled = False

        listof.append_column(id_column)
        listof.append_column(toggle_column)
        listof.append_column(date_column)
        listof.append_column(id_staff_column)
        listof.append_column(money_column)
        listof.append_column(status_column)

        id_cell       = gtk.CellRendererText()
        toggle_cell   = gtk.CellRendererToggle()
        date_cell     = gtk.CellRendererText()
        id_staff_cell = gtk.CellRendererText()
        money_cell    = gtk.CellRendererText()
        status_cell   = gtk.CellRendererText()

        toggle_cell.set_property('activatable', True)
        toggle_cell.connect('toggled', self.idToggled, self.liststore)

        id_column.pack_start(id_cell, True)
        toggle_column.pack_start(toggle_cell, True)
        date_column.pack_start(date_cell, True)
        id_staff_column.pack_start(id_staff_cell, True)
        money_column.pack_start(money_cell, True)
        status_column.pack_start(status_cell, True)

        id_column.set_attributes(id_cell, text = 0)
        toggle_column.add_attribute(toggle_cell, 'active', 1) 
        date_column.set_attributes(date_cell, text = 2)
        id_staff_column.set_attributes(id_staff_cell, text = 3)
        money_column.set_attributes(money_cell, text = 4)
        status_column.set_attributes(status_cell, text = 5)

        status_column.set_cell_data_func(status_cell, self.colorCell)
        
        list_scrolled.add(listof)

        table.attach(list_scrolled, 0, 2, 0, 1)
        
        ### End List ###
                
        ### Action list ###
        
        if self.PID == 0 or self.PID == 4:

            self.add_button = gtk.Button(stock = gtk.STOCK_ADD)
            self.add_button.connect('clicked', self.addForm) 
            alignment = gtk.Alignment(1.0)
            alignment.add(self.add_button)
            table.attach(alignment, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
                
        hbox = gtk.HBox()
        
        self.action_combobox = gtk.combo_box_new_text()
        
        self.action_combobox.append_text('Посмотреть')
        
        if self.PID == 0 or self.PID == 4:
        
            self.action_combobox.append_text('Редактировать')
            self.action_combobox.append_text('Удалить')
            self.action_combobox.append_text('Статус: Выдана')
            self.action_combobox.append_text('Статус: Не выдана')
        
        self.action_combobox.set_active(0)        
        
        hbox.pack_start(self.action_combobox)
        
        self.actionok_button = gtk.Button(stock = gtk.STOCK_OK)
        self.actionok_button.connect('clicked', self.makeAction)
        hbox.pack_start(self.actionok_button)
                
        alignment = gtk.Alignment(0.0)
        alignment.add(hbox)
        
        table.attach(alignment, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        
        self.list_frame.add(table)
        
        ### End action list ###
        
        self.getList()

    def gO(self):
        
        return self.list_frame
    
    def pressDel(self, empty, event):
    
        if gtk.gdk.keyval_name(event.keyval) == 'Delete' and \
           (self.PID == 0 or self.PID == 4):
            model, model1 = self.treeselection.get_selected_rows()
            k = 0
            for i in model1:
                result = self.Accountancy.wageDelete(self.liststore[i[0]-k][0])
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
           (self.PID == 0 or self.PID == 4): self.editForm(1)
        elif gtk.gdk.keyval_name(event.keyval) == 'a' and \
           (self.PID == 0 or self.PID == 4): self.addForm()
        
    def colorCell(self, col, cell, model, iter):

        if model[iter][5] == self.Accountancy.wageGetStatus(0):
            cell.set_property("foreground", "red")
        else:
            cell.set_property("foreground", "green")
    
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
        
        self.add_date.append(wd)
        self.add_id_staff.append(wd)
        self.add_money.append(wd)
        self.add_status.append(wd)
        
        self.add_dialog[wd] = gtk.Dialog('Заметка о зарплате')
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
        
        label = gtk.Label('Дата:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
        
        self.add_date[wd] = CalendarEntry()
        table.attach(self.add_date[wd], 1, 2, 0, 1, yoptions = gtk.FILL)
        
        label = gtk.Label('Работник:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
        
        liststore = gtk.ListStore(str, int)
        self.add_id_staff[wd] = gtk.combo_box_new_text()
        self.add_id_staff[wd].set_model(liststore)
        
        result = self.Staff.get(1)
        
        if len(result):
            for arr in result:
                liststore.append([arr[1] + ' ' + arr[2], int(arr[0])])
            
            self.add_id_staff[wd].set_active(0)
            
        table.attach(self.add_id_staff[wd], 1, 2, 1, 2, yoptions = gtk.FILL)
        
        label = gtk.Label('Кол-во денег:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
        
        self.add_money[wd] = gtk.Entry()
        self.add_money[wd].grab_focus()
        table.attach(self.add_money[wd], 1, 2, 2, 3, yoptions = gtk.FILL)
                               
        label = gtk.Label('Статус:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
        
        liststore = gtk.ListStore(str, int)
        self.add_status[wd] = gtk.combo_box_new_text()
        self.add_status[wd].set_model(liststore)
        
        liststore.append([self.Accountancy.wageGetStatus(0), 0])
        liststore.append([self.Accountancy.wageGetStatus(1), 1])
        
        self.add_status[wd].set_active(0)
        
        table.attach(self.add_status[wd], 1, 2, 3, 4, yoptions = gtk.FILL)
        
        hbox = gtk.HBox()
        
        ok_button = gtk.Button(stock = gtk.STOCK_OK)
        ok_button.connect('clicked', self.addFormOk, wd)
        hbox.pack_start(ok_button)
        
        cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
        cancel_button.connect('clicked', self.addFormCancel, wd)
        hbox.pack_start(cancel_button)
        
        table.attach(hbox, 0, 1, 4, 5, yoptions = gtk.FILL)         
          
        self.add_dialog[wd].vbox.pack_start(table)
        self.add_dialog[wd].show_all()
    
    def addFormOk(self, empty, wd):
        
        date = self.add_date[wd].getText()
        
        model = self.add_id_staff[wd].get_model()
        if len(model) > 0:
            index = self.add_id_staff[wd].get_active()
            id_staff = model[index][1]
        else: id_staff = 0
        
        money  = self.add_money[wd].get_text()
        
        model  = self.add_status[wd].get_model()
        index  = self.add_status[wd].get_active()
        status = model[index][1]
        
        if money != '':

            result = self.Accountancy.wageAdd(str(date), str(id_staff), 
                                              str(money), str(status))

            if result == False:    
                self.message.set_text('Ошибка заметка о зарплате не добавлена')
                gobject.timeout_add(10000, self.messageClear)
            else:
                self.message.set_text('')
                date = self.getNormalDateTime(date)
                    
                sername = self.Staff.getOne(id_staff, 'sername')
                if sername == False: staff = ''
                else:
                    staff = sername + \
                        ' ' + self.Staff.getOne(id_staff, 'name')
                            
                status = self.Accountancy.wageGetStatus(int(status))
                
                self.liststore.append([self.Accountancy.LastId(), False, 
                                       date, staff, str(money), status])
                                   
        self.add_dialog[wd].destroy()               
    
    def addFormCancel(self, empty, wd):
        
        self.add_dialog[wd].destroy() 
            
    def getList(self):

        result = self.Accountancy.wageGet()
        
        if len(result):
            model = [i[0] for i in self.liststore]
            for arr in result:
                if model.count(int(arr[0])) == 0:
                
                    date = self.getNormalDateTime(arr[1])
                    
                    sername = self.Staff.getOne(arr[2], 'sername')
                    if sername == False: staff = ''
                    else:
                        staff = sername + \
                            ' ' + self.Staff.getOne(arr[2], 'name')
                                
                    status = self.Accountancy.wageGetStatus(int(arr[4]))
                    
                    self.liststore.append([int(arr[0]), False, date, staff, 
                                           arr[3], status])

            model1 = [int(i[0]) for i in result]
            j = 0
            for i in range(len(model)):
                if model1.count(model[i]) == 0:
                    i = i - j
                    iter = self.liststore.get_iter(i)
                    self.liststore.remove(iter)
                    j += 1
            
            for i in range(len(self.liststore)):
                status = \
                    self.Accountancy.wageGetOne(self.liststore[i][0], 'status')
                if self.liststore[i][5] != \
                                        self.Accountancy.wageGetStatus(status):
                    self.liststore[i][5] = \
                                    self.Accountancy.wageGetStatus(int(status))

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
            result = self.Accountancy.wageMakeIn(model)
            if result == False: 
                self.message.set_text('Ошибка удаления')  
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()
        elif action == 'Статус: Выдана':
            model = [i[0] for i in self.liststore if i[1] == True]
            result = self.Accountancy.wageMakeIn(model, 1)
            if result == False: 
                self.message.set_text('Ошибка изменения статуса')  
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()                 
        elif action == 'Статус: Не выдана':
            model = [i[0] for i in self.liststore if i[1] == True]
            result = self.Accountancy.wageMakeIn(model, 2)
            if result == False: 
                self.message.set_text('Ошибка изменения статуса')  
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()
            
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
        
        for i in range(len(self.edit_model[wd])):
            self.edit_model[wd][i][3] = self.Accountancy.wageGetOne(
                                                    self.edit_model[wd][i][0], 
                                                    'id_staff')
        
        self.edit_date.append(wd)
        self.edit_id_staff.append(wd)
        self.edit_money.append(wd)
        self.edit_status.append(wd)
        
        hbox1 = self.editFormEl(wd, 0)
        
    def editFormEl(self, wd, index, bindex = None):
        
        if self.edit_box[wd] != None: self.edit_box[wd].destroy()
                     
        if bindex != None:

            model  = self.edit_status[wd][0].get_model()
            index1 = self.edit_status[wd][0].get_active()
            status = model[index1][0]
            
            model = self.edit_id_staff[wd][0].get_model()
            if len(model) > 0:
                index1 = self.edit_id_staff[wd][0].get_active()
                id_staff = model[index1][1]
            else: id_staff = 0
        
            self.edit_model[wd][bindex - 1][2] = \
                                            self.edit_date[wd][0].getEntryText()
            self.edit_model[wd][bindex - 1][3] = id_staff
                                                   
            self.edit_model[wd][bindex - 1][4] = \
                                            self.edit_money[wd][0].get_text()
            self.edit_model[wd][bindex - 1][5] = status

            model  = self.edit_status[wd][1].get_model()
            index1 = self.edit_status[wd][1].get_active()
            status = model[index1][0]
            
            model = self.edit_id_staff[wd][1].get_model()
            if len(model) > 0:
                index1 = self.edit_id_staff[wd][1].get_active()
                id_staff = model[index1][1]
            else: id_staff = 0
        
            self.edit_model[wd][bindex][2] = \
                                            self.edit_date[wd][1].getEntryText()
            self.edit_model[wd][bindex][3] = id_staff
                                                   
            self.edit_model[wd][bindex][4] = \
                                            self.edit_money[wd][1].get_text()
            self.edit_model[wd][bindex][5] = status

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
        
        self.edit_date[wd]     = [0, 1]
        self.edit_id_staff[wd] = [0, 1]
        self.edit_money[wd]    = [0, 1]
        self.edit_status[wd]   = [0, 1]
                                                    
        box = gtk.HBox()
        
        if len(self.edit_model[wd]) < 2: l = 1
        else: l = 2
                
        for i in range(l):
            
            if l == 1: 
                self.edit_dialog[wd]. \
                                set_title('Редактирование заметки о зарплате')
            else: 
                self.edit_dialog[wd]. \
                                set_title('Редактирование заметок о зарплате')
            
            if (index + i) == len(self.edit_model[wd]): k = 0
            else: k = index + i
                         
            arr = self.edit_model[wd][k]
            
            sername = self.Staff.getOne(arr[3], 'sername')
            if sername == False:
                staff = ''
            else: staff = sername + ' ' + self.Staff.getOne(arr[3], 'name')
             
            frame = gtk.Frame(' ' + staff + ' ')
            frame.set_border_width(3)                
            table = gtk.Table(2, 6, False)
            table.set_border_width(5)
            table.set_row_spacings(10)
            table.set_col_spacings(10)        
            
            label = gtk.Label('Дата:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
            
            self.edit_date[wd][i] = CalendarEntry()
            self.edit_date[wd][i].setDate(datetime.datetime.strptime(arr[2], 
                                                            '%d/%m/%Y %H:%M'))
            table.attach(self.edit_date[wd][i], 1, 2, 0, 1, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Работник:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
            
            liststore = gtk.ListStore(str, int)
            self.edit_id_staff[wd][i] = gtk.combo_box_new_text()
            self.edit_id_staff[wd][i].set_model(liststore)
            
            result = self.Staff.get(1)
            
            if len(result):
                k1 = 0
                for arr1 in result:
                    liststore.append([arr1[1] + ' ' + arr1[2], int(arr1[0])])
                    if int(arr1[0]) == int(arr[3]):
                        self.edit_id_staff[wd][i].set_active(k1)
                    k1 += 1
                            
            table.attach(self.edit_id_staff[wd][i], 1, 2, 1, 2, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Кол-во денег:')
            label.set_alignment(0, 0)
            table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
            
            self.edit_money[wd][i] = gtk.Entry()
            self.edit_money[wd][i].set_text(arr[4])
            table.attach(self.edit_money[wd][i], 1, 2, 2, 3, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Статус:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
            
            liststore = gtk.ListStore(str, int)
            self.edit_status[wd][i] = gtk.combo_box_new_text()
            self.edit_status[wd][i].set_model(liststore)
            
            liststore.append([self.Accountancy.wageGetStatus(0), 0])
            liststore.append([self.Accountancy.wageGetStatus(1), 1])
            
            for j in range(2):
                if self.Accountancy.wageGetStatus(j) == arr[5]: break
                  
            self.edit_status[wd][i].set_active(j)
            
            table.attach(self.edit_status[wd][i], 1, 2, 3, 4, 
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
        
        model  = self.edit_status[wd][bindex1].get_model()
        index1 = self.edit_status[wd][bindex1].get_active()
        status = model[index1][0]
        
        model = self.edit_id_staff[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_staff[wd][bindex1].get_active()
            id_staff = model[index1][1]
        else: id_staff = 0
    
        self.edit_model[wd][bindex][2] = \
                                    self.edit_date[wd][bindex1].getEntryText()
        self.edit_model[wd][bindex][3] = id_staff
                                               
        self.edit_model[wd][bindex][4] = \
                                    self.edit_money[wd][bindex1].get_text()
        self.edit_model[wd][bindex][5] = status
                
        if index == (len(self.edit_model[wd]) - 1): forward = 0
        else: forward = index
        
        self.edit_model[wd].pop(index)
               
        self.editFormEl(wd, forward)        
    
    def editFormOk(self, empty, wd, index, bindex1):
        
        date = self.edit_date[wd][bindex1].getText()
        
        model = self.edit_id_staff[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_staff[wd][bindex1].get_active()
            id_staff = model[index1][1]
        else: id_staff = 0
        
        money  = self.edit_money[wd][bindex1].get_text()
        
        model  = self.edit_status[wd][bindex1].get_model()
        index1  = self.edit_status[wd][bindex1].get_active()
        status = model[index1][1]

        if money != '':
            
            result = self.Accountancy.wageUpdate(self.edit_model[wd][index][0], 
                                                 str(date), str(id_staff), 
                                                 str(money), str(status))

            if result == False:
                self.message. \
                        set_text('Ошибка заметка о зарплате не отредоктирована')
                gobject.timeout_add(10000, self.messageClear)
            else:
                self.message.set_text('')
                k = 0
                for i in self.liststore:
                    if i[0] == self.edit_model[wd][index][0]: break
                    k += 1
                
                sername = self.Staff.getOne(id_staff, 'sername')
                if sername == False: staff = ''
                else:
                    staff = sername + \
                            ' ' + self.Staff.getOne(id_staff, 'name')

                self.liststore[k][2] = self.getNormalDateTime(date)
                self.liststore[k][3] = staff
                self.liststore[k][4] = money
                self.liststore[k][5] = self.Accountancy.wageGetStatus(status)
           
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
        
        model  = self.edit_status[wd][bindex1].get_model()
        index1 = self.edit_status[wd][bindex1].get_active()
        status = model[index1][0]
        
        model = self.edit_id_staff[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_staff[wd][bindex1].get_active()
            id_staff = model[index1][1]
        else: id_staff = 0
    
        self.edit_model[wd][bindex][2] = \
                                    self.edit_date[wd][bindex1].getEntryText()
        self.edit_model[wd][bindex][3] = id_staff
                                               
        self.edit_model[wd][bindex][4] = \
                                    self.edit_money[wd][bindex1].get_text()
        self.edit_model[wd][bindex][5] = status
        
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
        else: l = 2
                
        for i in range(l):
            
            if l == 1: 
                self.view_dialog[wd].set_title('Просмотр заметки о зарплате')
            else: self.view_dialog[wd].set_title('Просмотр заметак о зарплате')
            
            if (index + i) == len(self.view_model[wd]): k = 0
            else: k = index + i
                         
            arr = self.view_model[wd][k]
            
            frame = gtk.Frame(' ' + arr[3] + ' ')
            frame.set_border_width(3)
            table = gtk.Table(2, 7, False)
            table.set_border_width(5)
            table.set_row_spacings(10)
            table.set_col_spacings(10)
                                    
            label = gtk.Label('Дата:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
            
            view_date = gtk.Label(arr[2])
            view_date.set_alignment(0, 0.5)
            view_date.set_selectable(True)
            table.attach(view_date, 1, 2, 0, 1, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Работник:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
            
            if arr[3] != '': 
            
                view_id_staff = gtk.Label(arr[3])
                
                event_box = gtk.EventBox()
                event_box.connect('realize', lambda l: \
                        l.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2)))
                event_box.add(view_id_staff)
                event_box.connect('button_press_event', self.viewFormStaff, 
                                  self.Accountancy.wageGetOne(arr[0], 
                                                              'id_staff'))
        
                view_id_staff.set_alignment(0, 0.5)
                table.attach(event_box, 1, 2, 1, 2, yoptions = gtk.FILL)
            
            label = gtk.Label('Кол-во денег:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
            
            view_money = gtk.Label(arr[4])
            view_money.set_selectable(True)
            view_money.set_alignment(0, 0.5)
            table.attach(view_money, 1, 2, 2, 3, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Статус:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
            
            view_status = gtk.Label(arr[5])
            view_status.set_selectable(True)
            view_status.set_alignment(0, 0.5)
            table.attach(view_status, 1, 2, 3, 4, yoptions = gtk.FILL)
                         
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
    
    def getNormalDateTime(self, dt):
        
        temp = datetime.datetime.fromtimestamp(float(dt))
        
        ndt = temp.strftime('%d/%m/%Y %H:%M')
        
        return ndt
    
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
            
        arr = self.Staff.get(ids)[0]
                    
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
        
class Pay:

    def __init__(self, MySql, window, message, ID):
        
        self.Window = window
        
        self.message = message
        
        self.Accountancy = accountancy.Accountancy(MySql)
        self.Project = project.Project(MySql)
        self.Customer = customer.Customer(MySql)
        self.Staff = staff.Staff(MySql)
        
        self.PID = int(Staff(MySql).getOne(ID, 'post'))
        
        self.add_dialog = []
                
        self.add_date       = []
        self.add_id_project = []
        self.add_money      = []
        self.add_status     = []
        
        self.edit_dialog = []
        self.edit_box    = []
        self.edit_model  = []
        
        self.edit_date       = []
        self.edit_id_project = []
        self.edit_money      = []
        self.edit_status     = []
        
        self.view_dialog = []
        self.view_box    = []
        self.view_model  = []
        
        ### List ###
        
        self.list_frame = gtk.Frame(' Список оплат за проекты ')
        self.list_frame.set_border_width(3)
        
        table = gtk.Table(3, 2, False)
        table.set_row_spacings(10)
        table.set_border_width(10)

        self.liststore = gtk.ListStore(int, bool, str, str, str, str)

        list_scrolled = gtk.ScrolledWindow()
        list_scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        listof = gtk.TreeView(self.liststore)
        listof.set_reorderable(True)
        
        self.treeselection = listof.get_selection()
        self.treeselection.set_mode(gtk.SELECTION_MULTIPLE)
        
        listof.connect("key_press_event", self.pressDel)

        id_column         = gtk.TreeViewColumn()
        toggle_column     = gtk.TreeViewColumn()
        date_column       = gtk.TreeViewColumn('Дата')
        id_project_column = gtk.TreeViewColumn('Проект')
        money_column      = gtk.TreeViewColumn('Деньги')
        status_column     = gtk.TreeViewColumn('Статус')

        id_column.set_visible(False)
        toggle_column.set_min_width(20)
        toggle_column.set_clickable(True)
        date_column.set_sort_column_id(2)
        id_project_column.set_resizable(True)
        id_project_column.set_expand(True)
        id_project_column.set_sort_column_id(3)
        money_column.set_resizable(True)
        money_column.set_sort_column_id(4)
        status_column.set_sort_column_id(5)

        toggle_column.connect('clicked', self.idAllToggled)
        self.toggle_all_toggled = False

        listof.append_column(id_column)
        listof.append_column(toggle_column)
        listof.append_column(date_column)
        listof.append_column(id_project_column)
        listof.append_column(money_column)
        listof.append_column(status_column)

        id_cell         = gtk.CellRendererText()
        toggle_cell     = gtk.CellRendererToggle()
        date_cell       = gtk.CellRendererText()
        id_project_cell = gtk.CellRendererText()
        money_cell      = gtk.CellRendererText()
        status_cell     = gtk.CellRendererText()

        toggle_cell.set_property('activatable', True)
        toggle_cell.connect('toggled', self.idToggled, self.liststore)

        id_column.pack_start(id_cell, True)
        toggle_column.pack_start(toggle_cell, True)
        date_column.pack_start(date_cell, True)
        id_project_column.pack_start(id_project_cell, True)
        money_column.pack_start(money_cell, True)
        status_column.pack_start(status_cell, True)

        id_column.set_attributes(id_cell, text = 0)
        toggle_column.add_attribute(toggle_cell, 'active', 1) 
        date_column.set_attributes(date_cell, text = 2)
        id_project_column.set_attributes(id_project_cell, text = 3)
        money_column.set_attributes(money_cell, text = 4)
        status_column.set_attributes(status_cell, text = 5)

        status_column.set_cell_data_func(status_cell, self.colorCell)
        
        list_scrolled.add(listof)

        table.attach(list_scrolled, 0, 2, 0, 1)
        
        ### End List ###
                
        ### Action list ###
        
        if self.PID == 0 or self.PID == 4:

            self.add_button = gtk.Button(stock = gtk.STOCK_ADD)
            self.add_button.connect('clicked', self.addForm) 
            alignment = gtk.Alignment(1.0)
            alignment.add(self.add_button)
            table.attach(alignment, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
                
        hbox = gtk.HBox()
        
        self.action_combobox = gtk.combo_box_new_text()
        
        self.action_combobox.append_text('Посмотреть')
        
        if self.PID == 0 or self.PID == 4:
         
            self.action_combobox.append_text('Редактировать')
            self.action_combobox.append_text('Удалить')
            self.action_combobox.append_text('Статус: Оплачен')
            self.action_combobox.append_text('Статус: Не оплачен')
        
        self.action_combobox.set_active(0)        
        
        hbox.pack_start(self.action_combobox)
        
        self.actionok_button = gtk.Button(stock = gtk.STOCK_OK)
        self.actionok_button.connect('clicked', self.makeAction)
        hbox.pack_start(self.actionok_button)
                
        alignment = gtk.Alignment(0.0)
        alignment.add(hbox)
        
        table.attach(alignment, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        
        self.list_frame.add(table)
        
        ### End action list ###
        
        self.getList()

    def gO(self):
        
        return self.list_frame
    
    def pressDel(self, empty, event):
    
        if gtk.gdk.keyval_name(event.keyval) == 'Delete' and \
           (self.PID == 0 or self.PID == 4):
            model, model1 = self.treeselection.get_selected_rows()
            k = 0
            for i in model1:
                result = self.Accountancy.payDelete(self.liststore[i[0]-k][0])
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
           (self.PID == 0 or self.PID == 4): self.editForm(1)
        elif gtk.gdk.keyval_name(event.keyval) == 'a' and \
           (self.PID == 0 or self.PID == 4): self.addForm()
    
    def colorCell(self, col, cell, model, iter):

        if model[iter][5] == self.Accountancy.payGetStatus(0):
            cell.set_property("foreground", "red")
        else:
            cell.set_property("foreground", "green")
    
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
        
        self.add_date.append(wd)
        self.add_id_project.append(wd)
        self.add_money.append(wd)
        self.add_status.append(wd)
        
        self.add_dialog[wd] = gtk.Dialog('Заметка о оплате за проект')
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
        
        label = gtk.Label('Дата:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
        
        self.add_date[wd] = CalendarEntry()
        table.attach(self.add_date[wd], 1, 2, 0, 1, yoptions = gtk.FILL)
        
        label = gtk.Label('Проект:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
        
        liststore = gtk.ListStore(str, int)
        self.add_id_project[wd] = gtk.combo_box_new_text()
        self.add_id_project[wd].set_model(liststore)
        
        result = self.Project.get()
        
        if len(result):
            for arr in result:
                liststore.append([arr[1], int(arr[0])])
            
            self.add_id_project[wd].set_active(0)
            
        table.attach(self.add_id_project[wd], 1, 2, 1, 2, yoptions = gtk.FILL)
        
        label = gtk.Label('Кол-во денег:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
        
        self.add_money[wd] = gtk.Entry()
        self.add_money[wd].grab_focus()
        table.attach(self.add_money[wd], 1, 2, 2, 3, yoptions = gtk.FILL)
                               
        label = gtk.Label('Статус:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
        
        liststore = gtk.ListStore(str, int)
        self.add_status[wd] = gtk.combo_box_new_text()
        self.add_status[wd].set_model(liststore)
        
        liststore.append([self.Accountancy.payGetStatus(0), 0])
        liststore.append([self.Accountancy.payGetStatus(1), 1])
        
        self.add_status[wd].set_active(0)
        
        table.attach(self.add_status[wd], 1, 2, 3, 4, yoptions = gtk.FILL)
        
        hbox = gtk.HBox()
        
        ok_button = gtk.Button(stock = gtk.STOCK_OK)
        ok_button.connect('clicked', self.addFormOk, wd)
        hbox.pack_start(ok_button)
        
        cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
        cancel_button.connect('clicked', self.addFormCancel, wd)
        hbox.pack_start(cancel_button)
        
        table.attach(hbox, 0, 1, 4, 5, yoptions = gtk.FILL)         
          
        self.add_dialog[wd].vbox.pack_start(table)
        self.add_dialog[wd].show_all()
    
    def addFormOk(self, empty, wd):
        
        date = self.add_date[wd].getText()
        
        model = self.add_id_project[wd].get_model()
        if len(model) > 0:
            index = self.add_id_project[wd].get_active()
            id_project = model[index][1]
        else: id_project = 0
        
        money  = self.add_money[wd].get_text()
        
        model  = self.add_status[wd].get_model()
        index  = self.add_status[wd].get_active()
        status = model[index][1]
        
        if money != '':

            result = self.Accountancy.payAdd(str(date), str(id_project), 
                                             str(money), str(status))

            if result == False:    
                self.message.set_text('Ошибка заметка о зарплате не добавлена')
                gobject.timeout_add(10000, self.messageClear)
            else:
                self.message.set_text('')
                date = self.getNormalDateTime(date)
                    
                project = self.Project.getOne(id_project, 'name')
                if project == False: project = ''
                
                status = self.Accountancy.payGetStatus(int(status))
                
                self.liststore.append([self.Accountancy.LastId(), False, 
                                       date, project, str(money), status])
                                   
        self.add_dialog[wd].destroy()               
    
    def addFormCancel(self, empty, wd):
        
        self.add_dialog[wd].destroy() 
            
    def getList(self):

        result = self.Accountancy.payGet()
        
        if len(result):
            model = [i[0] for i in self.liststore]
            for arr in result:
                if model.count(int(arr[0])) == 0:
                
                    date = self.getNormalDateTime(arr[1])
                    
                    project = self.Project.getOne(arr[2], 'name')
                    if project == False: project = ''

                    status = self.Accountancy.payGetStatus(int(arr[4]))
                    
                    self.liststore.append([int(arr[0]), False, date, project, 
                                           arr[3], status])

            model1 = [int(i[0]) for i in result]
            j = 0
            for i in range(len(model)):
                if model1.count(model[i]) == 0:
                    i = i - j
                    iter = self.liststore.get_iter(i)
                    self.liststore.remove(iter)
                    j += 1
            
            for i in range(len(self.liststore)):
                status = self.Accountancy.payGetOne(self.liststore[i][0], 
                                                    'status')
                if self.liststore[i][5] != \
                                        self.Accountancy.payGetStatus(status):
                    self.liststore[i][5] = \
                                    self.Accountancy.payGetStatus(int(status))

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
            result = self.Accountancy.payMakeIn(model)
            if result == False: 
                self.message.set_text('Ошибка удаления')  
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()
        elif action == 'Статус: Оплачен':
            model = [i[0] for i in self.liststore if i[1] == True]
            result = self.Accountancy.payMakeIn(model, 1)
            if result == False: 
                self.message.set_text('Ошибка изменения статуса')
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()                 
        elif action == 'Статус: Не оплачен':
            model = [i[0] for i in self.liststore if i[1] == True]
            result = self.Accountancy.payMakeIn(model, 2)
            if result == False: 
                self.message.set_text('Ошибка изменения статуса')
                gobject.timeout_add(10000, self.messageClear)
            else: self.message.set_text('')
            self.getList()
            
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
        
        for i in range(len(self.edit_model[wd])):
            self.edit_model[wd][i][3] = self.Accountancy.payGetOne(
                                                    self.edit_model[wd][i][0], 
                                                    'id_project')
        
        self.edit_date.append(wd)
        self.edit_id_project.append(wd)
        self.edit_money.append(wd)
        self.edit_status.append(wd)
        
        hbox1 = self.editFormEl(wd, 0)
        
    def editFormEl(self, wd, index, bindex = None):
        
        if self.edit_box[wd] != None: self.edit_box[wd].destroy()
                     
        if bindex != None:

            model  = self.edit_status[wd][0].get_model()
            index1 = self.edit_status[wd][0].get_active()
            status = model[index1][0]
            
            model = self.edit_id_project[wd][0].get_model()
            if len(model) > 0:
                index1 = self.edit_id_project[wd][0].get_active()
                id_project = model[index1][1]
            else: id_project = 0
        
            self.edit_model[wd][bindex - 1][2] = \
                                            self.edit_date[wd][0].getEntryText()
            self.edit_model[wd][bindex - 1][3] = id_project
                                                   
            self.edit_model[wd][bindex - 1][4] = \
                                            self.edit_money[wd][0].get_text()
            self.edit_model[wd][bindex - 1][5] = status

            model  = self.edit_status[wd][1].get_model()
            index1 = self.edit_status[wd][1].get_active()
            status = model[index1][0]
            
            model = self.edit_id_project[wd][1].get_model()
            if len(model) > 0:
                index1 = self.edit_id_project[wd][1].get_active()
                id_project = model[index1][1]
            else: id_project = 0
        
            self.edit_model[wd][bindex][2] = \
                                            self.edit_date[wd][1].getEntryText()
            self.edit_model[wd][bindex][3] = id_project
                                                   
            self.edit_model[wd][bindex][4] = \
                                            self.edit_money[wd][1].get_text()
            self.edit_model[wd][bindex][5] = status

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
        
        self.edit_date[wd]       = [0, 1]
        self.edit_id_project[wd] = [0, 1]
        self.edit_money[wd]      = [0, 1]
        self.edit_status[wd]     = [0, 1]
                                                    
        box = gtk.HBox()
        
        if len(self.edit_model[wd]) < 2: l = 1
        else: l = 2
                
        for i in range(l):
            
            if l == 1: 
                self.edit_dialog[wd]. \
                            set_title('Редактирование заметки о оплате проекта')
            else: 
                self.edit_dialog[wd]. \
                        set_title('Редактирование заметок о о оплате проектов')
            
            if (index + i) == len(self.edit_model[wd]): k = 0
            else: k = index + i
                         
            arr = self.edit_model[wd][k]
            
            project = self.Project.getOne(arr[3], 'name')
            if project == False: project = ''
             
            frame = gtk.Frame(' ' + project + ' ')
            frame.set_border_width(3)                
            table = gtk.Table(2, 6, False)
            table.set_border_width(5)
            table.set_row_spacings(10)
            table.set_col_spacings(10)        
            
            label = gtk.Label('Дата:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
            
            self.edit_date[wd][i] = CalendarEntry()
            self.edit_date[wd][i].setDate(datetime.datetime.strptime(arr[2], 
                                                            '%d/%m/%Y %H:%M'))
            table.attach(self.edit_date[wd][i], 1, 2, 0, 1, yoptions = gtk.FILL)
            
            label = gtk.Label('Проект:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
            
            liststore = gtk.ListStore(str, int)
            self.edit_id_project[wd][i] = gtk.combo_box_new_text()
            self.edit_id_project[wd][i].set_model(liststore)
            
            result = self.Project.get()
            
            if len(result):
                k1 = 0
                for arr1 in result:
                    liststore.append([arr1[1], int(arr1[0])])
                    if int(arr1[0]) == int(arr[3]):
                        self.edit_id_project[wd][i].set_active(k1)
                    k1 += 1

            table.attach(self.edit_id_project[wd][i], 1, 2, 1, 2, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Кол-во денег:')
            label.set_alignment(0, 0)
            table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
            
            self.edit_money[wd][i] = gtk.Entry()
            self.edit_money[wd][i].set_text(arr[4])
            table.attach(self.edit_money[wd][i], 1, 2, 2, 3, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Статус:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
            
            liststore = gtk.ListStore(str, int)
            self.edit_status[wd][i] = gtk.combo_box_new_text()
            self.edit_status[wd][i].set_model(liststore)
            
            liststore.append([self.Accountancy.payGetStatus(0), 0])
            liststore.append([self.Accountancy.payGetStatus(1), 1])
            
            for j in range(2):
                if self.Accountancy.payGetStatus(j) == arr[5]: break
                  
            self.edit_status[wd][i].set_active(j)
            
            table.attach(self.edit_status[wd][i], 1, 2, 3, 4, 
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
        
        model  = self.edit_status[wd][bindex1].get_model()
        index1 = self.edit_status[wd][bindex1].get_active()
        status = model[index1][0]
        
        model = self.edit_id_project[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_project[wd][bindex1].get_active()
            id_project = model[index1][1]
        else: id_project = 0
    
        self.edit_model[wd][bindex][2] = \
                                    self.edit_date[wd][bindex1].getEntryText()
        self.edit_model[wd][bindex][3] = id_project
                                               
        self.edit_model[wd][bindex][4] = \
                                    self.edit_money[wd][bindex1].get_text()
        self.edit_model[wd][bindex][5] = status
                
        if index == (len(self.edit_model[wd]) - 1): forward = 0
        else: forward = index
        
        self.edit_model[wd].pop(index)
               
        self.editFormEl(wd, forward)        
    
    def editFormOk(self, empty, wd, index, bindex1):
        
        date = self.edit_date[wd][bindex1].getText()
        
        model = self.edit_id_project[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_project[wd][bindex1].get_active()
            id_project = model[index1][1]
        else: id_project = 0
        
        money  = self.edit_money[wd][bindex1].get_text()
        
        model  = self.edit_status[wd][bindex1].get_model()
        index1  = self.edit_status[wd][bindex1].get_active()
        status = model[index1][1]

        if money != '':
            
            result = self.Accountancy.payUpdate(self.edit_model[wd][index][0], 
                                                str(date), str(id_project), 
                                                str(money), str(status))

            if result == False:
                self.message. \
                set_text('Ошибка заметка о оплате за проект не отредоктирована')
                gobject.timeout_add(10000, self.messageClear)
            else:
                self.message.set_text('')
                k = 0
                for i in self.liststore:
                    if i[0] == self.edit_model[wd][index][0]: break
                    k += 1
                
                project = self.Project.getOne(id_project, 'name')
                if project == False: project = ''
                
                self.liststore[k][2] = self.getNormalDateTime(date)
                self.liststore[k][3] = project
                self.liststore[k][4] = money
                self.liststore[k][5] = self.Accountancy.payGetStatus(status)
           
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
        
        model  = self.edit_status[wd][bindex1].get_model()
        index1 = self.edit_status[wd][bindex1].get_active()
        status = model[index1][0]
        
        model = self.edit_id_project[wd][bindex1].get_model()
        if len(model) > 0:
            index1 = self.edit_id_project[wd][bindex1].get_active()
            id_project = model[index1][1]
        else: id_project = 0
    
        self.edit_model[wd][bindex][2] = \
                                    self.edit_date[wd][bindex1].getEntryText()
        self.edit_model[wd][bindex][3] = id_project
                                               
        self.edit_model[wd][bindex][4] = \
                                    self.edit_money[wd][bindex1].get_text()
        self.edit_model[wd][bindex][5] = status
        
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
        else: l = 2
                
        for i in range(l):
            
            if l == 1: 
                self.view_dialog[wd].set_title('Просмотр заметки о зарплате')
            else: self.view_dialog[wd].set_title('Просмотр заметак о зарплате')
            
            if (index + i) == len(self.view_model[wd]): k = 0
            else: k = index + i
                         
            arr = self.view_model[wd][k]
            
            frame = gtk.Frame(' ' + arr[3] + ' ')
            frame.set_border_width(3)
            table = gtk.Table(2, 7, False)
            table.set_border_width(5)
            table.set_row_spacings(10)
            table.set_col_spacings(10)
                                    
            label = gtk.Label('Дата:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
            
            view_date = gtk.Label(arr[2])
            view_date.set_alignment(0, 0.5)
            view_date.set_selectable(True)
            table.attach(view_date, 1, 2, 0, 1, yoptions = gtk.FILL)
            
            label = gtk.Label('Проект:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
            
            if arr[3] != '': 
                
                view_id_project = gtk.Label(arr[3])
                
                event_box = gtk.EventBox()
                event_box.connect('realize', lambda l: \
                        l.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2)))
                event_box.add(view_id_project)
                event_box.connect('button_press_event', self.viewFormProject, 
                                  self.Accountancy.payGetOne(arr[0], 
                                                             'id_project'))
                      
                view_id_project.set_alignment(0, 0.5)
                table.attach(event_box, 1, 2, 1, 2, yoptions = gtk.FILL)
            
            label = gtk.Label('Кол-во денег:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
            
            view_money = gtk.Label(arr[4])
            view_money.set_selectable(True)
            view_money.set_alignment(0, 0.5)
            table.attach(view_money, 1, 2, 2, 3, 
                         yoptions = gtk.FILL)
            
            label = gtk.Label('Статус:')
            label.set_alignment(0, 0.5)
            table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
            
            view_status = gtk.Label(arr[5])
            view_status.set_selectable(True)
            view_status.set_alignment(0, 0.5)
            table.attach(view_status, 1, 2, 3, 4, 
                         yoptions = gtk.FILL)
                         
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
    
    def getNormalDateTime(self, dt):
        
        temp = datetime.datetime.fromtimestamp(float(dt))
        
        ndt = temp.strftime('%d/%m/%Y %H:%M')
        
        return ndt
    
    def viewFormProject(self, empty, empty1, ids):
        
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
        
        view_dialog.set_title('Просмотр проекта')                
            
        arr = self.Project.get(ids)[0]
        
        frame = gtk.Frame(' ' + arr[1] + ' ')
        frame.set_border_width(3)                
        table = gtk.Table(2, 7, False)
        table.set_border_width(5)
        table.set_row_spacings(10)
        table.set_col_spacings(10)        
                                
        label = gtk.Label('Название:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 0, 1, yoptions = gtk.FILL)
        
        if arr[1] != '':
            view_name = gtk.Label(arr[1])
            view_name.set_alignment(0, 0.5)
            view_name.set_selectable(True)
            table.attach(view_name, 1, 2, 0, 1, yoptions = gtk.FILL)
        
        label = gtk.Label('Дата начала:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 1, 2, yoptions = gtk.FILL)
        
        view_dates = gtk.Label(self.getNormalDateTime(arr[3], 1))
        view_dates.set_alignment(0, 0.5)
        view_dates.set_selectable(True)
        table.attach(view_dates, 1, 2, 1, 2, 
                     yoptions = gtk.FILL)
        
        label = gtk.Label('Дата окончания:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 2, 3, yoptions = gtk.FILL)
        
        view_datee = gtk.Label(self.getNormalDateTime(arr[4]))
        view_datee.set_selectable(True)
        view_datee.set_alignment(0, 0.5)
        table.attach(view_datee, 1, 2, 2, 3, yoptions = gtk.FILL)
        
        label = gtk.Label('Статус:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 3, 4, yoptions = gtk.FILL)
        
        view_status = gtk.Label(self.Project.getStatus(arr[5]))
        view_status.set_selectable(True)
        view_status.set_alignment(0, 0.5)
        table.attach(view_status, 1, 2, 3, 4, yoptions = gtk.FILL)
                                
        label = gtk.Label('Клиент:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 4, 5, yoptions = gtk.FILL)
        
        sername = self.Customer.getOne(arr[6], 'sername')
        if sername == False: customer = ''
        else: customer = sername + ' ' + self.Customer.getOne(arr[6], 'name')
        
        if customer != '': 
            
            view_id_customer = gtk.Label(customer)
            
            event_box = gtk.EventBox()
            event_box.connect('realize', lambda l: \
                    l.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2)))
            event_box.add(view_id_customer)
            event_box.connect('button_press_event', self.viewFormCustomer, 
                              arr[6])
    
            view_id_customer.set_alignment(0, 0.5)
            table.attach(event_box, 1, 2, 4, 5, yoptions = gtk.FILL)
        
        label = gtk.Label('Архитектор:')
        label.set_alignment(0, 0.5)
        table.attach(label, 0, 1, 5, 6, yoptions = gtk.FILL)
        
        sername = self.Staff.getOne(arr[7], 'sername')
        if sername == False: staff = ''
        else: staff = sername + ' ' + self.Staff.getOne(arr[7], 'name')
        
        if staff != '':
        
            view_id_staff = gtk.Label(staff)
            
            event_box = gtk.EventBox()
            event_box.connect('realize', lambda l: \
                    l.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2)))
            event_box.add(view_id_staff)
            event_box.connect('button_press_event', self.viewFormStaff, arr[7])
    
            view_id_staff.set_alignment(0, 0.5)
            table.attach(event_box, 1, 2, 5, 6, yoptions = gtk.FILL)
            
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
            
        arr = self.Staff.get(ids)[0]
                    
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

class Base:
        
    def __init__(self, MySql, window, ID):
                      
                      
        self.box = gtk.VBox()
        self.box.set_border_width(10)
                    
        ### Title ###

        hbox = gtk.HBox()

        title_image = gtk.Image()
        title_image.set_from_file(sys.path[0] + '/images/accountancy.png')
        hbox.pack_start(title_image, False)
        
        title_label = gtk.Label('Бухгалтерия')
        title_label.modify_font(pango.FontDescription('Monospace Bold 20'))
        title_label.set_alignment(0, 1.0)
        
        hbox.pack_start(title_label)
        
        self.wage_togbutton = gtk.ToggleButton(' Зарплата ')
        self.wage_togbutton.set_active(True)
        self.wage_togbutton.connect('clicked', self.chooseList)
        hbox.pack_start(self.wage_togbutton, False)
        
        self.pay_togbutton = gtk.ToggleButton(' Оплата за проекты ')
        self.pay_togbutton.set_active(True)
        self.pay_togbutton.connect('clicked', self.chooseList)
        hbox.pack_start(self.pay_togbutton, False)

        self.box.pack_start(hbox, False)
        
        ### End Title ###
               
        hbox = gtk.HBox()
        
        self.message = gtk.Label()
        self.message.modify_fg(gtk.STATE_NORMAL, 
                                   gtk.gdk.color_parse('#e12e2e'))
        hbox.pack_start(self.message)     
        
        self.box.pack_start(hbox, False)
        
        box1 = gtk.HBox()
        
        self.wage_list_frame = Wage(MySql, window, self.message, ID).gO()
        self.pay_list_frame  = Pay(MySql, window, self.message, ID).gO()
        
        box1.pack_start(self.wage_list_frame)
        box1.pack_start(self.pay_list_frame)
        
        self.box.pack_start(box1)
        
        self.box.show_all()
        
        self.chooseList(0)

    def gO(self):
               
        return self.box   
        
    def chooseList(self, toggbutton):
        
        if self.wage_togbutton.get_active() == True:
            self.wage_list_frame.show_all()
        else: self.wage_list_frame.hide_all()
        
        if self.pay_togbutton.get_active() == True:
            self.pay_list_frame.show_all()
        else: self.pay_list_frame.hide_all()
        
        if self.wage_togbutton.get_active() == False and \
           self.pay_togbutton.get_active() == False:
            toggbutton.set_active(True)

