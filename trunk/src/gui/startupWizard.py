'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
class related to the document to go wizard
'''

import wx.wizard
import dbGui
import utilities
class StartupWizard(wx.wizard.Wizard):
    '''
    wizard helping user to configure the preferences
    '''


    def __init__(self,parent,params=None):
        '''
        Constructor
        '''
        wx.wizard.Wizard.__init__(self,parent,-1,_('Startup wizard'))
        self.pageDatabase = PageDatabaseChoice(self)
        self.pageScanner  = PageScannerChoice(self)
        self.pageOCR      = PageOCRChoice(self)
        self.pageSurvey   = PageSurveyChoice(self)
        self.pageFolders  = PageFoldersChoice(self)
        self.Bind(wx.wizard.EVT_WIZARD_FINISHED, self.on_finished)
        self.Bind(wx.wizard.EVT_WIZARD_CANCEL, self.on_cancel)
        self.GetPageAreaSizer().Add(self.pageDatabase)
        self.params=params
    def on_cancel(self,event):
        if not utilities.ask(_('Are you sure you want to cancel the startup wizard ?')) : event.Veto()
    def on_finished(self,event):
        pass
 
class PageDatabaseChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        s=_('Please choose a name for your database.\n Check the box if you want to define an encryption password for the database.')
        self.dbFrame = dbGui.CreatorFrame(self)
        self.sizer.Add(wx.StaticText(self,-1,s),wx.EXPAND)
        self.sizer.Add(self.dbFrame,0,flag=wx.EXPAND)        
        self.SetSizer(self.sizer)
    def GetNext(self):
        return self.Parent.pageScanner
    def GetPrev(self):
        return None

class PageScannerChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def GetNext(self):
        return self.Parent.pageOCR
    def GetPrev(self):
        return self.Parent.pageDatabase


class PageOCRChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def GetNext(self):
        return self.Parent.pageSurvey
    def GetPrev(self):
        return self.Parent.pageScanner

class PageSurveyChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def GetNext(self):
        return self.Parent.pageFolders
    def GetPrev(self):
        return self.Parent.pageOCR

class PageFoldersChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def GetNext(self):
        return None
    def GetPrev(self):
        return self.Parent.pageFolders