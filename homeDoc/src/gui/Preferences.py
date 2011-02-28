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
import os
import utilities
if os.name == 'posix' :
    from scannerAccess import saneAccess
else:
    from scannerAccess import twainAccess


class PrefScanner(wx.NotebookPage):
    def __init__(self,parent,id,name):
        wx.NotebookPage.__init__(self,parent,id,name=name)
        self.panel = wx.Panel(self, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.stScanner = wx.StaticText(self.panel,-1,_("None"))
        self.btChangeScanner = wx.Button(self.panel,-1,_("Change"))

        self.sizer.Add(wx.StaticText(self.panel,-1,_("Scanner source : ")),flag=wx.ALL)
        self.sizer.Add(self.stScanner,flag=wx.ALL|wx.EXPAND)
        self.sizer.Add(self.btChangeScanner,flag=wx.ALL)
        
        self.panel.SetSizerAndFit(self.sizer)
        
        # OTHER INITIALISATIIONS
        if os.name == 'posix' :
            self.scanner = saneAccess.SaneAccess(self.GetHandle())
        else:
            self.scanner = twainAccess.TwainAccess(self.GetHandle())
        currentScanner = database.theConfig.get_current_scanner()
        self.stScanner.Label = currentScanner
        # BINDING
        self.Bind(wx.EVT_BUTTON, self.actionChangeScanner, self.btChangeScanner)
    def actionChangeScanner(self,event):
        self.stScanner.Label = self.scanner.chooseSource()
    def actionSave(self):
        database.theConfig.set_current_scanner(self.stScanner.Label)

class PrefSurveyDir(wx.NotebookPage):
    def __init__(self,parent,id,name):
        wx.NotebookPage.__init__(self,parent,id,name=name)
        self.panel = wx.Panel(self, -1)
        self.dirSurveySizer = wx.GridBagSizer(1,1)
        self.lstSurveyDirs = wx.CheckListBox(self.panel,-1,style=wx.LB_EXTENDED)
        self.txtSurveyExt = wx.TextCtrl(self.panel,-1)
        self.btAddDir = wx.Button(self.panel,-1,_("Add"))
        self.btRemDir = wx.Button(self.panel,-1,_("Remove"))

        self.dirSurveySizer.Add(wx.StaticText(self.panel,-1,_("Survey directories")) , (0,0),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL )
        self.dirSurveySizer.Add(self.btAddDir,(0,1),flag=wx.ALL)
        self.dirSurveySizer.Add(self.btRemDir,(0,2),flag=wx.ALL)
        self.dirSurveySizer.Add(wx.StaticText(self.panel,-1,_("(check directories which have to be recursively surveyed)")) , (1,0),span=(1,3),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL )
        self.dirSurveySizer.Add(self.lstSurveyDirs,(2,0),span=(1,4),flag=wx.ALL | wx.EXPAND | wx.ALIGN_BOTTOM)
        self.dirSurveySizer.Add(wx.StaticText(self.panel,-1,_("Survey extensions") ),(3,0),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.dirSurveySizer.Add(self.txtSurveyExt,(3,1),span=(1,3),flag=wx.EXPAND|wx.ALL)

        self.dirSurveySizer.AddGrowableCol(3)
        self.dirSurveySizer.AddGrowableRow(2)
        
        
        (item_list,checked) = database.theConfig.get_survey_directory_list()
        self.lstSurveyDirs.SetItems(item_list)
        self.lstSurveyDirs.SetChecked(checked)
        S = database.theConfig.get_survey_extension_list()
        self.txtSurveyExt.SetValue(S)
        self.panel.SetSizerAndFit(self.dirSurveySizer)
        # BINDING
        self.Bind(wx.EVT_BUTTON, self.actionAddDir, self.btAddDir)
        self.Bind(wx.EVT_BUTTON, self.actionRemDir, self.btRemDir)
    def actionAddDir(self,event):
        dir_name = wx.DirSelector()
        if len(dir_name)>0 :  self.lstSurveyDirs.Append(dir_name)
    def actionRemDir(self,event):
        elems = list(self.lstSurveyDirs.GetSelections())
        elems.sort(reverse=True)
        for e in elems : self.lstSurveyDirs.Delete(e)
    def actionSave(self):
        dir_list = self.lstSurveyDirs.GetItems()
        recursiveIndex = self.lstSurveyDirs.GetChecked()
        database.theConfig.set_survey_directory_list(dir_list, recursiveIndex)
        database.theConfig.set_survey_extension_list(self.txtSurveyExt.GetValue())
        
class PrefGui(wx.Dialog):
    '''
    classdocs
    '''


    def __init__(self,parent):
        wx.Dialog.__init__(self, parent, -1, _('Preference window'), wx.DefaultPosition, style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        '''
        Constructor
        '''
               
        self.panel = wx.Panel(self, -1)
        self.txtDatabaseName = wx.StaticText(self.panel,-1,database.theBase.base_name);
        self.btChangeBase = wx.Button(self.panel,-1,_("Change"))
        #self.cbLanguage = wx.Choice(self.panel,-1)
        #self.cbLanguage.SetSelection(0)
        self.btOk = wx.Button(self.panel,-1,_("Ok"))
        self.btCancel = wx.Button(self.panel,-1,_("Cancel"))

        self.prefSizer = wx.GridBagSizer(1,1)

        self.prefSizer.Add(wx.StaticText(self.panel,-1,_("Database name :") ),(0,0),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        self.prefSizer.Add(self.btChangeBase,(0,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        self.prefSizer.Add(self.txtDatabaseName,(0,2),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        #self.prefSizer.Add(wx.StaticText(self.panel,-1,_("Language")),(1,0),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        #self.prefSizer.Add(self.cbLanguage,(1,1),flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL)

        self.tabFrame = wx.Notebook(self.panel,-1)
        self.dirSurveyFrame = PrefSurveyDir(self.tabFrame,-1,name=_("Dir. survey"))
        self.scannerFrame = PrefScanner(self.tabFrame,-1,name=_("Scanner"))
        
        self.tabFrame.AddPage(self.dirSurveyFrame,self.dirSurveyFrame.GetName())
        self.tabFrame.AddPage(self.scannerFrame,self.scannerFrame.GetName())
        
        self.prefSizer.Add(self.tabFrame,(1,0),span=(1,3),flag=wx.EXPAND|wx.ALL)
        self.prefSizer.Add(self.btOk,(2,0),flag=wx.EXPAND|wx.ALL)
        self.prefSizer.Add(self.btCancel,(2,1),flag=wx.EXPAND|wx.ALL)
        
        self.prefSizer.AddGrowableCol(2)
        self.prefSizer.AddGrowableRow(1)

        database.theConfig.read_config()
        
#        lng = database.theConfig.get_installed_languages()
#        self.cbLanguage.SetItems(lng)
#        current = database.theConfig.get_current_language()
#        if current in lng :
#            self.cbLanguage.SetStringSelection(current)
#        else:
#            self.cbLanguage.SetSelection(0)
        
        self.panel.SetSizerAndFit(self.prefSizer)
        self.SetClientSize((600,300))
        
        # binding
        self.Bind(wx.EVT_BUTTON, self.actionChangeDataBase, self.btChangeBase)
        self.Bind(wx.EVT_BUTTON, self.actionSavePrefs, self.btOk)
        self.Bind(wx.EVT_BUTTON, lambda x : self.Close(), self.btCancel)
    def actionChangeDataBase(self,event):        
        filename=None
        dlg = wx.FileDialog(self,style=wx.FD_OPEN,message=_('choose the database file'))
        if dlg.ShowModal():
            filename = os.path.join(dlg.Directory,dlg.Filename)
        if not filename : return
        self.txtDatabaseName.SetLabel(filename)
        database.theConfig.set_database_name(filename)
        database.theBase.use_base(filename)
        
    def actionSavePrefs(self,event):
        #database.theConfig.set_current_language(self.cbLanguage.GetStringSelection())
        self.dirSurveyFrame.actionSave()
        self.scannerFrame.actionSave()
        if not database.theConfig.commit_config() :
            wx.MessageBox(_('Problem : Unable to write the configuration file.'))
        else:
            self.Close()
            