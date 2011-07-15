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
def ask_string(message,caption=_('String expected'),defaultValue=''):
    return wx.GetTextFromUser(message,caption,defaultValue)

class ProgressDialog:
    def __init__(self,title='Progression',message=None):
        self.NMAX=100000
        self.stepSize=[1.0]
        self.donePerStep=[0.0]
        self.pd = wx.ProgressDialog(title,message='',maximum=self.NMAX,style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)
        if not message is None : self.pd.Update(1,message)
    def new_sub_step(self,stepSize,newMessage=None):
        self.stepSize.append(stepSize)
        self.donePerStep.append(0.0)
        if newMessage is not None :
            progression = round(self.calculate_total_done() * (self.NMAX-1))
            if progression>=self.NMAX : progression=self.NMAX-1
            self.pd.Update(progression,newMessage)
    def finish_current_step(self):
        v=self.stepSize.pop()
        self.donePerStep.pop()
        self.donePerStep[-1] += v
    def calculate_total_done(self):
        total=0.0
        s=1.0
        for i in range(len(self.stepSize)) :
            #print '(i=%d , s=%g , t=%g)' % (i,s,total)
            s *= self.stepSize[i]
            total += self.donePerStep[i]*s
        return total
    def set_current_step_to(self,stepProgression,message=None):
        self.donePerStep[-1] = stepProgression
        if self.donePerStep[-1]>=1 : self.donePerStep[-1]=1.0
        progression = round(self.calculate_total_done() * (self.NMAX-1))
#        print self.stepSize
#        print self.donePerStep
#        print self.calculate_total_done()
#        print '*'*10
        if progression>=self.NMAX : progression=self.NMAX-1
        if message is None:
            self.pd.Update(progression)
        else:
            self.pd.Update(progression,message)
    def add_to_current_step(self,stepIncrement,message=None):
        self.set_current_step_to(self.donePerStep[-1] + stepIncrement, message)
    def clear(self):
        self.stepSize=[1.0]
        self.donePerStep=[0.0]        
    def destroy(self):
        self.pd.Destroy()

gProgressDialog = None

def getGlobalProgressDialog(title='Progression',message=None):
    global gProgressDialog
    if gProgressDialog is None :
        try:
            gProgressDialog = ProgressDialog(title,message)
        except:
            gProgressDialog = None
    if gProgressDialog is None:
        raise "Unable to create progress dialog"
    return gProgressDialog
def closeGlobalProgressDialog():
    global gProgressDialog
    if gProgressDialog is not None :
        gProgressDialog.destroy()
        gProgressDialog = None