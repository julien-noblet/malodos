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



class FolderView (wx.Dialog):
    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, -1, _('Directory chooser'),style=wx.DEFAULT_DIALOG_STYLE| wx.RESIZE_BORDER)
        self.panel = wx.Panel(self, -1)
        self.totSizer = wx.GridBagSizer(1)
        self.treeView = wx.TreeCtrl(self.panel,-1,style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT)
        self.btSelect = wx.Button(self.panel,-1,'select')
        self.btAdd = wx.Button(self.panel,-1,'add')
        self.totSizer.Add(self.treeView,(0,0),span=(1,3),flag=wx.EXPAND)
        self.totSizer.Add(self.btSelect,(1,0),flag=wx.SHAPED)
        self.totSizer.Add(self.btAdd,(1,1),flag=wx.SHAPED)
        self.totSizer.AddGrowableRow(0)
        self.totSizer.AddGrowableCol(2)
        self.panel.SetSizerAndFit(self.totSizer)
