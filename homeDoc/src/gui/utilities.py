'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
'''

import wx

def multichoice(choices, message=_('choose in the following :') ):
    return wx.GetSingleChoiceIndex(message,_('selection'),choices)
def show_message(message):
    return wx.MessageBox(message,_('alert'))
def ask(message):
    dlg =  wx.MessageDialog(None,message,_('Question'),wx.YES_NO)
    return dlg.ShowModal()

class ProgressDialog:
    def __init__(self,title='Progression',maxProgress=100.0,message=None):
        self.pd = wx.ProgressDialog(title,message='',maximum=maxProgress,style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)
        if not message is None : self.pd.Update(1,message)
        #self.pd.ShowModal()
    def set_state(self,progression,message=None):
        if message is None:
            self.pd.Update(progression)
        else:
            self.pd.Update(progression,message)
    def Destroy(self):
        self.pd.Destroy()