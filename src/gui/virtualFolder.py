# -*- coding: utf-8 -*-
'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
view / select / edit virtual folders
'''
import wx
from database import theBase
import utilities


class FolderView (wx.Dialog):
    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, -1, _('Directory chooser'),style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.panel = wx.Panel(self, -1)
        self.totSizer = wx.GridBagSizer(3)
        self.treeView = wx.TreeCtrl(self.panel,-1,style=wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT)
        self.btSelect = wx.Button(self.panel,-1,'select')
        self.btAdd = wx.Button(self.panel,-1,'add')
        self.btDel = wx.Button(self.panel,-1,'del')
        self.btRen = wx.Button(self.panel,-1,'ren')
        self.totSizer.Add(self.treeView,(0,0),span=(1,5),flag=wx.EXPAND)
        self.totSizer.Add(self.btSelect,(1,0),flag=wx.EXPAND)
        self.totSizer.Add(self.btAdd,(1,1),flag=wx.EXPAND)
        self.totSizer.Add(self.btDel,(1,2),flag=wx.EXPAND)
        self.totSizer.Add(self.btRen,(1,3),flag=wx.EXPAND)
        self.totSizer.AddGrowableRow(0)
        self.totSizer.AddGrowableCol(4)
        self.panel.SetSizerAndFit(self.totSizer)
        self.fillDirectories()
        
        self.Bind(wx.EVT_BUTTON,self.action_add_subfolder,self.btAdd)
        self.Bind(wx.EVT_BUTTON,self.action_del_subfolder,self.btDel)
        self.Bind(wx.EVT_BUTTON,self.action_ren_subfolder,self.btRen)
        self.treeView.Bind(wx.EVT_TREE_END_DRAG,self.action_drag_drop)
    def action_drag_drop(self,event):
        print event
    def fillDirectories(self):
        def fillUnder(itemID):
            addedItems = []
            folderID = self.treeView.GetPyData(itemID)
            descendants = theBase.folders_childs_of(folderID)
            for row in descendants:
                id = row[0]
                name = row[1]
                item = self.treeView.AppendItem(itemID,name,data=wx.TreeItemData(id))
                addedItems.append(item)
            for item in addedItems : fillUnder(item)
        self.treeView.DeleteAllItems()
        itemID = self.treeView.AddRoot(_('ROOT'),data=wx.TreeItemData(0))
        fillUnder(itemID)
        #self.treeView.ExpandAll()
        #self.FitInside()
    def action_add_subfolder(self,event):
        name = utilities.ask_string(_('name :'),_('Give a sub-folder name'),_('folder'))
        item = self.treeView.GetSelection()
        folderID = self.treeView.GetPyData(item)
        if theBase.folders_add_child_under(name,folderID):
            self.fillDirectories()
        else:
            utilities.message(_('unable to add the sub-folder {0}').format(name))
    def action_del_subfolder(self,event):
        item = self.treeView.GetSelection()
        folderID = self.treeView.GetPyData(item)
        folderName = self.treeView.GetItemText(item)
        sure = utilities.ask(_('Are you sure that you want to delete the folder {0}'.format(folderName)))
        if sure==wx.ID_YES:
            if theBase.folders_remove(folderID):
                self.fillDirectories()
            else:
                utilities.message(_('unable to remove the sub-folder {0}').format(folderName))
    def action_ren_subfolder(self,event):
        item = self.treeView.GetSelection()
        folderID = self.treeView.GetPyData(item)
        folderName = self.treeView.GetItemText(item)
        name = utilities.ask_string(_('name :'),_('Give a sub-folder name'),folderName)
        sure = utilities.ask(_('Are you sure that you want to rename folder "{iniName}" to "{newName}"'.format(iniName=folderName,newName=name)))
        if sure==wx.ID_YES:
            if theBase.folders_rename(folderID,name):
                self.fillDirectories()
            else:
                utilities.message(_('unable to remove the subfolder {0}').format(folderName))