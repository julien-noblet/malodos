'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI dialog for documents survey
'''

import wx
import docWindow
import addFileWindow
import database
import os.path

class SurveyWindow(wx.Dialog):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, -1, 'Survey directory',style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        self.docViewSizer = wx.BoxSizer(wx.VERTICAL)
        self.upPart =  wx.BoxSizer(wx.HORIZONTAL)
        self.recordSizer =  wx.BoxSizer(wx.HORIZONTAL)

        self.docList = wx.ListBox(self.panel,-1)
        self.docWin = docWindow.docWindow(self.panel,-1)
        self.docViewSizer.Add(self.upPart,1,wx.EXPAND)
        self.upPart.Add(self.docList,1,wx.EXPAND)
        self.upPart.Add(self.docWin,1,wx.EXPAND)
        
        self.recordPart = addFileWindow.RecordWidget(self.panel)
        self.recordPart.lbFileName.Disable()
        self.recordSizer.Add(self.recordPart,1,wx.EXPAND)
        self.btAddRecord = wx.Button(self.panel,-1,'Add')
        self.docViewSizer.Add(self.recordSizer,0,wx.EXPAND)
        self.recordButtonSizer = wx.BoxSizer(wx.VERTICAL)
        self.recordButtonSizer.Add(self.btAddRecord,1,wx.EXPAND)
        self.recordSizer.Add(self.recordButtonSizer)
        self.panel.SetSizerAndFit(self.docViewSizer)
        
        cur = database.theBase.get_files_under('/mnt/ntfs3/scans');
        for row in cur:
            self.docList.Append(os.path.basename(row[0]),row)
        
        self.SetSizeWH(800,600)
    