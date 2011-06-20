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
from algorithms.general import str_to_bool

class SurveyWindow(wx.Dialog):
    '''
    classdocs
    '''

    class SurveyContent(wx.NotebookPage):
        def __init__(self,parent,baseWin):
            wx.NotebookPage.__init__(self,parent,-1,name="Survey")
            self.baseWin=baseWin
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.panel = wx.Panel(self, -1)
            self.docList = wx.TreeCtrl(self.panel,-1,style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT)
            self.sizer.Add(self.docList,1,flag=wx.ALL|wx.EXPAND|wx.GROW)
            self.panel.SetSizerAndFit(self.sizer)
            self.Bind(wx.EVT_TREE_SEL_CHANGED,self.actionDocSelect,self.docList)
        def populate(self):
            accepted_ext = database.theConfig.get_survey_extension_list()
            accepted_ext = [ '.' + i.lower() for i in accepted_ext.split(' ') ]
            rootItem = None
            def append_dir(rootDir,dr,file_list):
                cur = database.theBase.get_files_under(dr)
                presents = set( (os.path.basename(unicode(row[0])) for row in cur ) )
                dir_list = set(f for f in file_list if os.path.isdir(os.path.join(dr,f)))
                file_list = set(f for f in file_list if not os.path.isdir(os.path.join(dr,f)) and os.path.splitext(f)[1].lower() in accepted_ext)
                file_list = file_list - presents
                #if len(file_list)<1 : return
                relPath = os.path.relpath(dr, rootDir)
                if relPath == '.' :
                    currentItem = self.docList.AppendItem(self.docList.GetRootItem() , rootDir ,data=wx.TreeItemData(rootDir))
                else:
                    dir_comp = relPath.split(os.path.sep)
                    currentItem = rootItem
                    (currentItem,cookie) = self.docList.GetFirstChild(currentItem)
                    while currentItem and (self.docList.GetPyData(currentItem) != rootDir) :
                            currentItem = self.docList.GetNextSibling(currentItem)
                    for depth in range(len(dir_comp)):
                        searchedItem = dir_comp[depth]
                        if currentItem : (currentItem,cookie) = self.docList.GetFirstChild(currentItem)
                        while currentItem and (self.docList.GetPyData(currentItem) != searchedItem) :
                            currentItem = self.docList.GetNextSibling(currentItem)
                        if not currentItem : break
                    
                if not currentItem :
                    print 'problem for ' , relPath
                    return
                for f in dir_list:
                    fname = os.path.join(dr,f)
                    self.docList.AppendItem(currentItem,f,data=wx.TreeItemData(f))
                for f in file_list:
                    fname = os.path.join(dr,f)
                    self.docList.AppendItem(currentItem,f,data=wx.TreeItemData('*'+fname))
            
            
            
            self.docList.DeleteAllItems() #self.docList.Clear()# 
            rootItem = self.docList.AddRoot(_('Files not in database'),data=wx.TreeItemData("root"))
            (dir_list,recursiveIdx) = database.theConfig.get_survey_directory_list()
            for i in range(len(dir_list)):
                dname = dir_list[i].decode('utf8')
                if i in recursiveIdx:
                    os.path.walk(dname,append_dir, dname )
                else:
                    append_dir(dname, dir_list[i].decode('utf8'), os.listdir(dir_list[i]))
        def actionDocSelect(self,event):
            sel = self.docList.GetSelection()
            if sel :
                fname = self.docList.GetPyData(sel)
                if fname[0]=='*' :
                    fname=fname[1:]
                else:
                    return
            else:
                return
                
            #fname = self.docList.GetClientData(sel)
            #if not fname : return
            self.baseWin.recordPart.SetFields(filename = fname,doOCR=str_to_bool( database.theConfig.get_param('OCR', 'autoStart','1') ))
            try:
                data.theData.load_file(fname)
                self.baseWin.docWin.resetView()
                self.baseWin.docWin.showCurrentImage()
            except:
                data.theData.clear_all()

    class MissOCRContent(wx.NotebookPage):
        def __init__(self,parent,baseWin):
            wx.NotebookPage.__init__(self,parent,-1,name="MissOCR")
            self.baseWin=baseWin
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.panel = wx.Panel(self, -1)
            self.docList = wx.ListBox(self.panel,-1,style=wx.LB_SORT)
            self.sizer.Add(self.docList,1,flag=wx.ALL|wx.EXPAND|wx.GROW)
            self.panel.SetSizerAndFit(self.sizer)
            self.Bind(wx.EVT_LISTBOX,self.actionDocSelect,self.docList)
        def actionDocSelect(self,event):
            sel = self.docList.GetSelection()
            if sel is None : return
            row = self.docList.GetClientData(sel)
            
            docID = row[database.theBase.IDX_ROWID]
            filename = row[database.theBase.IDX_FILENAME]
            title = row[database.theBase.IDX_TITLE]
            description = row[database.theBase.IDX_DESCRIPTION]
            documentDate = row[database.theBase.IDX_DOCUMENT_DATE]
            tags = row[database.theBase.IDX_TAGS]
            self.baseWin.recordPart.SetFields(filename, title, description, documentDate,tags,True)
            try:
                data.theData.load_file(filename)
                self.baseWin.docWin.resetView()
                self.baseWin.docWin.showCurrentImage()
            except:
                data.theData.clear_all()
        def populate(self):
            docIDs = database.theBase.doc_without_ocr()
            for row in docIDs:
                self.docList.Append(row[database.theBase.IDX_TITLE] , row)
    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, -1, _('Survey directory'),style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        self.docViewSizer = wx.BoxSizer(wx.VERTICAL)
        self.upPart =  wx.BoxSizer(wx.HORIZONTAL)
        self.recordSizer =  wx.BoxSizer(wx.HORIZONTAL)

        #self.docList = wx.TreeCtrl(self.panel,-1,style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT) #wx.ListBox(self.panel,-1)# 
        self.tabFrame = wx.Notebook(self.panel,-1)
        self.dirSurveyFrame = self.SurveyContent(self.tabFrame,self)
        self.missOCRFrame = self.MissOCRContent(self.tabFrame,self)
        self.tabFrame.AddPage(self.dirSurveyFrame,_("Directory survey"))
        self.tabFrame.AddPage(self.missOCRFrame,_("Missing OCR"))
        #self.prefSizer.Add(self.tabFrame,(1,0),span=(1,3),flag=wx.EXPAND|wx.ALL)
        self.upPart.Add(self.tabFrame,1,wx.EXPAND)
        
        self.docWin = docWindow.docWindow(self.panel,-1)
        self.docViewSizer.Add(self.upPart,1,wx.EXPAND)
        #self.upPart.Add(self.docList,1,wx.EXPAND)
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

        #self.Bind(wx.EVT_TREE_SEL_CHANGED,self.actionDocSelect,self.docList)
        #self.docList.Bin(wx.EVT_TREE_SEL_CHANGED, handler)
        self.Bind(wx.EVT_BUTTON, self.actionDoAdd, self.btAddRecord)
        
        self.dirSurveyFrame.populate()
        self.missOCRFrame.populate()
        self.SetSizeWH(1000,600)
        
                        

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