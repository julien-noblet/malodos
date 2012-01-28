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
class StartupWizard(wx.wizard.Wizard):
    '''
    wizard helping user to configure the preferences
    '''


    def __init__(self,params):
        '''
        Constructor
        '''
 
class PageScannerChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def GetNext(self):
        return None
    def GetPrev(self):
        return None


class PageOCRChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def GetNext(self):
        return None
    def GetPrev(self):
        return None

class PageSurveyChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def GetNext(self):
        return None
    def GetPrev(self):
        return None

class PageFoldersChoice (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        
    def GetNext(self):
        return None
    def GetPrev(self):
        return None