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
import database

class PrefGui(wx.Dialog):
    '''
    classdocs
    '''


    def __init__(self,parent):
        wx.Dialog.__init__(self, parent, -1, 'Preference window', wx.DefaultPosition, style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        '''
        Constructor
        '''
               
        self.panel = wx.Panel(self, -1)
        self.txtDatabaseName = wx.StaticText(self.panel,-1,database.theBase.base_name);
        self.btChangeBase = wx.Button(self.panel,-1,"Change")
        self.cbLanguage = wx.Choice(self.panel,-1)
        self.cbLanguage.SetSelection(0)
        self.lstSurveyDirs = wx.CheckListBox(self.panel,-1,style=wx.LB_EXTENDED)
        self.txtSurveyExt = wx.TextCtrl(self.panel,-1)
        self.btAddDir = wx.Button(self.panel,-1,"Add")
        self.btRemDir = wx.Button(self.panel,-1,"Remove")
        self.btOk = wx.Button(self.panel,-1,"Ok")
        self.btCancel = wx.Button(self.panel,-1,"Cancel")

        self.prefSizer = wx.GridBagSizer(1,1)

        self.prefSizer.Add(wx.StaticText(self.panel,-1,"Database name :" ),(0,0),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.prefSizer.Add(self.btChangeBase,(0,1),flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,span=(1,2))
        self.prefSizer.Add(self.txtDatabaseName,(0,3),flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.prefSizer.Add(wx.StaticText(self.panel,-1,"Language"),(1,0),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.prefSizer.Add(self.cbLanguage,(1,1),span=(1,2),flag=wx.EXPAND|wx.ALL)
        self.prefSizer.Add(wx.StaticText(self.panel,-1,"Survey directories") , (2,0),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL )
        self.prefSizer.Add(self.btAddDir,(2,1),flag=wx.EXPAND|wx.ALL)
        self.prefSizer.Add(self.btRemDir,(2,2),flag=wx.EXPAND|wx.ALL)
        self.prefSizer.Add(wx.StaticText(self.panel,-1,"(check directories that have to be recursively surveyed)") , (2,3),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL )
        self.prefSizer.Add(self.lstSurveyDirs,(3,0),span=(1,4),flag=wx.ALL | wx.EXPAND | wx.ALIGN_BOTTOM)
        self.prefSizer.Add(wx.StaticText(self.panel,-1,"Survey extensions" ),(4,0),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.prefSizer.Add(self.txtSurveyExt,(4,1),flag=wx.EXPAND|wx.ALL,span=(1,3))
        self.prefSizer.Add(self.btOk,(5,0),flag=wx.EXPAND|wx.ALL)
        self.prefSizer.Add(self.btCancel,(5,1),flag=wx.EXPAND|wx.ALL)
        
        self.prefSizer.AddGrowableCol(3)
        self.prefSizer.AddGrowableRow(3)

        database.theConfig.read_config()
        
        lng = database.theConfig.get_installed_languages()
        self.cbLanguage.SetItems(lng)
        current = database.theConfig.get_current_language()
        if current in lng :
            self.cbLanguage.SetStringSelection(current)
        else:
            self.cbLanguage.SetSelection(0)
        (item_list,checked) = database.theConfig.get_survey_directory_list()
        self.lstSurveyDirs.SetItems(item_list)
        self.lstSurveyDirs.SetChecked(checked)
        S = database.theConfig.get_survey_extension_list()
        self.txtSurveyExt.SetValue(S)
        
        self.panel.SetSizerAndFit(self.prefSizer)
        self.SetClientSize((600,300))
        
        # binding
        self.Bind(wx.EVT_BUTTON, self.actionChangeDataBase, self.btChangeBase)
        self.Bind(wx.EVT_BUTTON, self.actionAddDir, self.btAddDir)
        self.Bind(wx.EVT_BUTTON, self.actionRemDir, self.btRemDir)
        self.Bind(wx.EVT_BUTTON, self.actionSavePrefs, self.btOk)
        self.Bind(wx.EVT_BUTTON, lambda x : self.Close(), self.btCancel)
    def actionChangeDataBase(self,event):
        pass
    def actionAddDir(self,event):
        dir_name = wx.DirSelector()
        if len(dir_name)>0 :  self.lstSurveyDirs.Append(dir_name)
    def actionRemDir(self,event):
        elems = list(self.lstSurveyDirs.GetSelections())
        elems.sort(reverse=True)
        for e in elems : self.lstSurveyDirs.Delete(e)
    def actionSavePrefs(self,event):
        dir_list = self.lstSurveyDirs.GetItems()
        recursiveIndex = self.lstSurveyDirs.GetChecked()
        database.theConfig.set_survey_directory_list(dir_list, recursiveIndex)
        database.theConfig.set_current_language(self.cbLanguage.GetStringSelection())
        database.theConfig.set_survey_extension_list(self.txtSurveyExt.GetValue())
        if not database.theConfig.commit_config() :
            wx.MessageBox('Problem : Unable to write the configuration file.')
        else:
            self.Close()
            