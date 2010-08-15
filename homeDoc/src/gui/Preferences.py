'''
Created on 15 aout 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI dialog to define general user preferences

'''

import wx
from database import theBase

class PrefGui(wx.Dialog):
    '''
    classdocs
    '''


    def __init__(self,parent):
        wx.Dialog.__init__(self, parent, -1, 'Scanning a new document', wx.DefaultPosition, style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        '''
        Constructor
        '''
        self.panel = wx.Panel(self, -1)
        self.txtDatabase = wx.StaticText(self.panel,-1,"Database name :" + theBase.base_name);
        self.btChangeBase = wx.Button(self.panel,-1,"Change")
        self.lstSurveyDirs = wx.ListBox(self.panel,-1)

        self.prefSizer = wx.BoxSizer(wx.VERTICAL)

        self.prefSizer.Add(self.txtDatabase,0,0)
        self.prefSizer.Add(self.btChangeBase,0,wx.EXPAND)
        self.prefSizer.Add(wx.StaticText(self.panel,-1,"Survey directories"))
        self.prefSizer.Add(self.lstSurveyDirs,1,wx.EXPAND|wx.ALIGN_BOTTOM)
        
        self.panel.SetSizerAndFit(self.prefSizer)
        self.SetSizeWH(800,600)
