'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI frame of the main application board
'''
import datetime
import wx
import addFileWindow
import docWindow
import database
import string
import os
import subprocess
from data import theData

import scanWindow
import survey
from gui import utilities
import hashlib
from gui import Preferences
import Resources

class MainFrame(wx.Frame):
    ID_ADD_FILE=1
    ID_ADD_SCAN=2
    ID_REMOVE_SEL=3
    ID_PRINT_DOC=4
    ID_DOCTOGO=5
    ID_SURVEY=6
    ID_PREFS=7
    ID_CREDITS=8
    #===========================================================================
    # constructor (GUI building)
    #===========================================================================
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, 'MALODOS Main panel', wx.DefaultPosition, (576, 721), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        

        self.docPart = wx.SplitterWindow(self.panel,-1,style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        self.docPart.SetSashGravity(0.5)
        
        self.docViewPanel = wx.Panel(self.docPart)
        self.docViewSizer = wx.BoxSizer(wx.VERTICAL)
        self.recordSizer =  wx.BoxSizer(wx.HORIZONTAL)

        self.docWin = docWindow.docWindow(self.docViewPanel,-1)
        self.docViewSizer.Add(self.docWin,1,wx.EXPAND)
        
        self.tbMainBar = self.CreateToolBar()
        self.tbMainBar.AddLabelTool(self.ID_ADD_FILE,'',wx.Bitmap(Resources.get_icon_filename('ADD_FILE')),shortHelp=Resources.get_message('ADD_FILE'))
        self.tbMainBar.AddLabelTool(self.ID_ADD_SCAN,'',wx.Bitmap(Resources.get_icon_filename('ADD_SCAN')),shortHelp=Resources.get_message('ADD_SCAN'))
        self.tbMainBar.AddLabelTool(self.ID_REMOVE_SEL,'',wx.Bitmap(Resources.get_icon_filename('REMOVE_SELECTION')),shortHelp=Resources.get_message('REMOVE_SELECTION'))
        self.tbMainBar.AddLabelTool(self.ID_PRINT_DOC,'',wx.Bitmap(Resources.get_icon_filename('DOC_PRINT')),shortHelp=Resources.get_message('DOC_PRINT'))
        self.tbMainBar.AddLabelTool(self.ID_DOCTOGO,'',wx.Bitmap(Resources.get_icon_filename('DOC_ZIP')),shortHelp=Resources.get_message('DOC_ZIP'))
        self.tbMainBar.AddLabelTool(self.ID_SURVEY,'',wx.Bitmap(Resources.get_icon_filename('SURVEY_WIN')),shortHelp=Resources.get_message('SURVEY_WIN'))
        self.tbMainBar.AddLabelTool(self.ID_PREFS,'',wx.Bitmap(Resources.get_icon_filename('PREFS')),shortHelp=Resources.get_message('PREFS'))
        self.tbMainBar.AddLabelTool(self.ID_CREDITS,'',wx.Bitmap(Resources.get_icon_filename('CREDITS')),shortHelp=Resources.get_message('CREDITS'))
        self.tbMainBar.Realize()
        
        self.recordPart = addFileWindow.RecordWidget(self.docViewPanel)
        self.recordPart.lbFileName.Disable()
        self.recordSizer.Add(self.recordPart,1,wx.EXPAND)
        self.btUpdateRecord = wx.Button(self.docViewPanel,-1,'Update')
        self.btShowExternal = wx.Button(self.docViewPanel,-1,'System show')
        self.btRemoveRecord = wx.Button(self.docViewPanel,-1,'Remove')
        self.docViewSizer.Add(self.recordSizer,0,wx.EXPAND)
        self.recordButtonSizer = wx.BoxSizer(wx.VERTICAL)
        self.recordButtonSizer.Add(self.btUpdateRecord,1,wx.EXPAND)
        self.recordButtonSizer.Add(self.btShowExternal,1,wx.EXPAND)
        self.recordButtonSizer.Add(self.btRemoveRecord,1,wx.EXPAND)
        self.recordSizer.Add(self.recordButtonSizer)
        self.docViewPanel.SetSizerAndFit(self.docViewSizer)

        self.lbDocuments = wx.ListBox(self.docPart, -1,size= (387, 124),style=wx.LB_SORT | wx.LB_EXTENDED )
        self.label2 = wx.StaticText(self.panel, -1, 'filter :')
        self.tbFilter = wx.TextCtrl(self.panel, -1, '',style=wx.TE_PROCESS_ENTER)
        self.btBuildFilter = wx.Button(self.panel, -1, 'advanced')
        self.btBuildFilter.Hide()
        

        # sizers
        self.totalWin = wx.BoxSizer(wx.VERTICAL)
        self.upPart = wx.BoxSizer(wx.HORIZONTAL)
        self.searchPart = wx.BoxSizer(wx.HORIZONTAL)
        self.docPart.SplitVertically(self.lbDocuments,self.docViewPanel)

        # adding widgets into sizers (--> creating layout)
        self.searchPart.Add(self.label2,0,wx.ALIGN_LEFT)
        self.searchPart.Add(self.tbFilter,1,wx.EXPAND |wx.ALIGN_CENTER_VERTICAL)
        self.searchPart.Add(self.btBuildFilter,0,wx.EXPAND)
        self.searchPart.Layout()
        
        self.upPart.Add(self.searchPart,3,wx.ALIGN_LEFT)
        self.upPart.Layout()
        
        self.totalWin.Add(self.upPart,0,wx.EXPAND)
        self.totalWin.Add(self.docPart,1,wx.EXPAND |wx.ALIGN_BOTTOM)
        self.totalWin.Layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.actionSearch, self.tbFilter)
        self.Bind(wx.EVT_LISTBOX,self.actionDocSelect,self.lbDocuments)
        self.Bind(wx.EVT_TOOL, self.actionAddFile, id=self.ID_ADD_FILE)
        self.Bind(wx.EVT_TOOL, self.actionAddScan, id=self.ID_ADD_SCAN)
        self.Bind(wx.EVT_TOOL,self.actionStartSurvey,id=self.ID_SURVEY)
        self.Bind(wx.EVT_TOOL,self.actionShowPrefs,id=self.ID_PREFS)
        self.Bind(wx.EVT_BUTTON,self.actionStartExternalApp,self.btShowExternal)
        self.Bind(wx.EVT_BUTTON,self.actionRemoveRecord,self.btRemoveRecord)
        self.Bind(wx.EVT_BUTTON,self.actionUpdateRecord,self.btUpdateRecord)

        # layout assignment
        self.panel.SetSizerAndFit(self.totalWin)
        self.totalWin.Fit(self)
        self.Maximize()
        self.actionSearch(None)
        
    #===========================================================================
    # click on add scan button
    #===========================================================================
    def actionAddScan(self,event):
        Frame = scanWindow.ScanWindow(self,"Scan a new document")
        theData.clear_all()
        Frame.ShowModal()
        theData.clear_all()
        self.actionSearch(None)

    #===========================================================================
    # click on add file button
    #===========================================================================
    def actionAddFile(self,event):
        Frame = addFileWindow.AddFileWindow(self,"Add a new document")
        Frame.ShowModal()
        self.actionSearch(None)
    #===========================================================================
    # click on search button (or press enter on the search text entry)
    #===========================================================================
    def actionSearch(self,event):
        # clear the listbox
        self.lbDocuments.Clear()
        # retrieve the keywords from the different fields
        keywords = string.strip(self.tbFilter.Value, ' ')
        keywords = string.split(keywords, ' ')
        # remove short words
        keywords = [i for i in keywords if len(i)>3]
        # treat the case where no keyword are found
        if len(keywords)<1: keywords = None
        # find the list corresponding to the selected keywords
        docList = database.theBase.find_documents(keywords)
        # return if no doc found
        if not docList: return
        # otherwise show them in the listbox
        for row in docList:
            self.lbDocuments.Append(row[0] , row)
    #===========================================================================
    # actionDocSelect : show the selected item on the doc part
    #===========================================================================
    def actionDocSelect(self,event):
        sel = self.lbDocuments.GetSelections()
        if sel == wx.NOT_FOUND or len(sel)!=1: return
        sel = sel[0]
        row = self.lbDocuments.GetClientData(sel)
        docID = row[-1]
        filename = row[2] 
        title = row[0]
        description = row[1]
        documentDate = row[5]
        try:
            file_md5 = hashlib.md5(open(row[2], "rb").read()).hexdigest()
            if row[6] !=  file_md5:
                Q = utilities.ask('The file content has changed! Do you wish to update its signature?')
                if Q==wx.ID_YES:
                    if not database.theBase.update_doc_signature(docID, file_md5):
                        wx.MessageBox('Unable to update the database')
        except:
            utilities.show_message('Unable to check the file signature...')
        
        self.recordPart.SetFields(filename, title, description, documentDate)
        #print row
        try:
            theData.load_file(filename)
            self.docWin.showCurrentImage()
        except:
            theData.clear_all()
        
    #===========================================================================
    # actionStartExternalApp : start the system default application associated with the file
    #===========================================================================
    def actionStartExternalApp(self,event):
        sel = self.lbDocuments.GetSelections()
        if sel == wx.NOT_FOUND or len(sel)!=1: return
        sel = sel[0]
        row = self.lbDocuments.GetClientData(sel)
        filename = row[2]
        if os.name == 'posix' :
            subprocess.Popen(['xdg-open', filename])
        else:
            os.startfile(filename)
    #===========================================================================
    # actionUpdateRecord : update the current record
    #===========================================================================
    def actionUpdateRecord(self,event):
        sel = self.lbDocuments.GetSelections()
        if sel == wx.NOT_FOUND or len(sel)!=1: return
        sel = sel[0]
        row = self.lbDocuments.GetClientData(sel)
        docID = row[-1]
        filename = self.recordPart.lbFileName.GetPath() 
        title = self.recordPart.lbTitle.Value
        description = self.recordPart.lbDescription.GetValue()
        documentDate = self.recordPart.lbDate.GetValue()
        documentDate=datetime.date(year=documentDate.GetYear(),month=documentDate.GetMonth()+1,day=documentDate.GetDay())
        if not database.theBase.update_doc(docID, title, description, format(documentDate,'%d-%m-%Y'), filename):
            wx.MessageBox('Unable to update the database')
        else:
            self.actionSearch(None)
        
    #===========================================================================
    # actionRemoveRecord : remove the selected items
    #===========================================================================
    def actionRemoveRecord(self,event):
        sel = self.lbDocuments.GetSelections()
        if sel == wx.NOT_FOUND : return
        docID = []
        for i in sel:
            row = self.lbDocuments.GetClientData(i)
            docID.append(row[-1])
        if len(docID)==1:
            msg = 'do you really want to delete this record (' + row[0] + ')'        
        else:
            msg = 'do you really want to delete these ' + str(len(docID)) + ' records'
        confirmation = wx.MessageDialog(self,msg,style=wx.OK|wx.CANCEL | wx.CENTRE)
        x= confirmation.ShowModal()
        if x == wx.ID_CANCEL : return
        
        #print 'must remove ' + str(docID) + ' because x is ' + str(x)
        database.theBase.remove_documents(docID)
        self.actionSearch(None)
        
    #===========================================================================
    # actionStartSurvey : show the document survey window
    #===========================================================================
    def actionStartSurvey(self,event):
        theData.clear_all()
        Frame = survey.SurveyWindow(self)
        Frame.ShowModal()
        theData.clear_all()
        self.actionSearch(None)
    #===========================================================================
    # actionShowPrefs : show the preferences window
    #===========================================================================
    def actionShowPrefs(self,event):
        Frame = Preferences.PrefGui(self)
        Frame.ShowModal()
