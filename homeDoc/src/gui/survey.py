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
import RecordWidget
import database
import os.path
import data

class SurveyWindow(wx.Dialog):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, -1, _('Survey directory'),style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        self.docViewSizer = wx.BoxSizer(wx.VERTICAL)
        self.upPart =  wx.BoxSizer(wx.HORIZONTAL)
        self.recordSizer =  wx.BoxSizer(wx.HORIZONTAL)

        self.docList = wx.ListBox(self.panel,-1)
        self.docWin = docWindow.docWindow(self.panel,-1)
        self.docViewSizer.Add(self.upPart,1,wx.EXPAND)
        self.upPart.Add(self.docList,1,wx.EXPAND)
        self.upPart.Add(self.docWin,1,wx.EXPAND)
        
        self.recordPart = RecordWidget.RecordWidget(self.panel)
        self.recordPart.lbFileName.Disable()
        self.recordSizer.Add(self.recordPart,1,wx.EXPAND)
        self.btAddRecord = wx.Button(self.panel,-1,_('Add'))
        self.docViewSizer.Add(self.recordSizer,0,wx.EXPAND)
        self.recordButtonSizer = wx.BoxSizer(wx.VERTICAL)
        self.recordButtonSizer.Add(self.btAddRecord,1,wx.EXPAND)
        self.recordSizer.Add(self.recordButtonSizer)
        self.panel.SetSizerAndFit(self.docViewSizer)

        self.Bind(wx.EVT_LISTBOX,self.actionDocSelect,self.docList)
        self.Bind(wx.EVT_BUTTON, self.actionDoAdd, self.btAddRecord)
        
        self.populate_list()
        self.SetSizeWH(800,600)
        
    def populate_list(self):
        accepted_ext = database.theConfig.get_survey_extension_list()
        accepted_ext = [ '.' + i for i in accepted_ext.split(' ') ]

        def append_dir(param,dr,file_list):
            cur = database.theBase.get_files_under(dr)
            presents = set( (os.path.basename(unicode(row[0])) for row in cur ) )
            file_list = set(f for f in file_list if not os.path.isdir(os.path.join(dr,f)) and os.path.splitext(f)[1] in accepted_ext)
            file_list = file_list - presents
            if len(file_list)<1 : return
            self.docList.Append("           " + _('UNDER DIRECTORY')  + dr,None)
            self.docList.Append('*'*60,None)
            for f in file_list:
                fname = os.path.join(dr,f)
                self.docList.Append(f,fname)
        
        
        self.docList.Clear()
        (dir_list,recursiveIdx) = database.theConfig.get_survey_directory_list()
        for i in range(len(dir_list)):
            if i in recursiveIdx:
                os.path.walk(dir_list[i].decode('utf8'),append_dir, None )
            else:
                append_dir(None, dir_list[i].decode('utf8'), os.listdir(dir_list[i]))


        

    def actionDocSelect(self,event):
        sel = self.docList.GetSelection()
        fname = self.docList.GetClientData(sel)
        if not fname : return
        self.recordPart.SetFields(filename = fname)
        try:
            data.theData.load_file(fname)
            self.docWin.resetView()
            self.docWin.showCurrentImage()
        except:
            data.theData.clear_all()
    #===========================================================================
    # Click on Add document button
    #===========================================================================
    def actionDoAdd(self,event):
        if not self.recordPart.do_save_record():
            wx.MessageBox(_('Unable to add the file to the database'))
        else:
            data.theData.clear_all()
            self.recordPart.clear_all()
            self.populate_list()