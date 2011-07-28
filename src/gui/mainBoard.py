'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI frame of the main application board
'''
import wx
import addFileWindow
import RecordWidget
import docWindow
import database
import os
import subprocess
import docPrinter
from data import theData

import scanWindow
import survey
from gui import utilities
import hashlib
from gui import Preferences
import Resources
import algorithms.stringFunctions
import data
import documentToGo

class FlatView(wx.NotebookPage):
    ID_ALPHABETICAL=(1,_('Alphabetical'))
    ID_CHRONO_DOC=(2,_('Chronological (document)'))
    ID_CHRONO_REG=(3,_('Chronological (registering date)'))
    ID_PERTINENCE=(4,_('Relevance'))
    CHOICES=[ID_ALPHABETICAL,ID_CHRONO_DOC,ID_CHRONO_REG,]#ID_PERTINENCE]#
    def __init__(self,parent,id,name,board):
        wx.NotebookPage.__init__(self,parent,id,name=name)
        self.board = board
        self.totSizer = wx.GridBagSizer()
        self.panel = wx.Panel(self, -1)
        self.lbDocuments = wx.ListBox(self.panel, -1,style=wx.LB_EXTENDED )
        listChoices = [c[1] for c in self.CHOICES]
        self.cbOrder = wx.ComboBox(self.panel,-1,choices=listChoices)
        self.cbOrder.SetSelection(0)
        self.totSizer.Add(wx.StaticText(self.panel,label=_('Classification')),(0,0),flag=wx.EXPAND)
        self.totSizer.Add(self.cbOrder,(0,1),flag=wx.EXPAND)
        self.totSizer.Add(self.lbDocuments,(1,0),span=(1,2),flag=wx.EXPAND)
        self.totSizer.AddGrowableRow(1)
        self.totSizer.AddGrowableCol(1)
        self.panel.SetSizerAndFit(self.totSizer)
        self.Bind(wx.EVT_LISTBOX,self.action_select,self.lbDocuments)
        self.Bind(wx.EVT_COMBOBOX,self.show_content,self.cbOrder)
        self.docList=None
    def fillWith(self,docList):
        self.docList = docList
        self.show_content()
    def show_content(self,event=None):
        self.lbDocuments.Clear()
        if self.docList is None or len(self.docList)==0: return
        sel = self.cbOrder.GetSelection()
        if sel is None : return
        sel = self.CHOICES[sel][0]
        if sel == self.ID_ALPHABETICAL[0]:
            self.docList.sort(key=lambda row:row[database.theBase.IDX_TITLE].lower())
        elif sel == self.ID_CHRONO_DOC[0]:
            self.docList.sort(key=lambda row:row[database.theBase.IDX_DOCUMENT_DATE])
        elif sel == self.ID_CHRONO_REG[0]:
            self.docList.sort(key=lambda row:row[database.theBase.IDX_REGISTER_DATE])
        elif sel == self.ID_PERTINENCE[0] and database.theBase.IDX_COUNT<len(self.docList[0]):
            self.docList.sort(key=lambda row:row[database.theBase.IDX_COUNT])
        for row in self.docList:
            self.lbDocuments.Append(row[database.theBase.IDX_TITLE] , row)
    def action_select(self,event):
        sel = self.lbDocuments.GetSelections()
        if sel == wx.NOT_FOUND: return
        row = [self.lbDocuments.GetClientData(s) for s in sel]
        self.board.actionDocSelect(row)
class FolderView(wx.NotebookPage):
    def __init__(self,parent,id,name,board):
        wx.NotebookPage.__init__(self,parent,id,name=name)
        self.board = board
        self.totSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self, -1)
        self.trFolders = wx.TreeCtrl(self.panel, -1,style=wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT|wx.TR_MULTIPLE )
        self.totSizer.Add(self.trFolders,1,wx.EXPAND)
        self.panel.SetSizerAndFit(self.totSizer)
        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.action_select,self.trFolders)
    def fillWith(self,docList):
        self.trFolders.DeleteAllItems()
        if docList is None : return
        rootItem=self.trFolders.AddRoot(_('ROOT'),data=wx.TreeItemData(0))
        unclassified = self.trFolders.AppendItem(rootItem,_('Unclassified'))
        itemDict={}
        for row in docList:
            title=row[database.theBase.IDX_TITLE]
            docID = row[database.theBase.IDX_ROWID]
            folderID_list = database.theBase.folders_list_for(docID)
            if len(folderID_list)<1:
                self.trFolders.AppendItem(unclassified,title,data=wx.TreeItemData(row))
            for folderID in folderID_list:
                genealogy = database.theBase.folders_genealogy_of(folderID, False)
                item = self.trFolders.GetRootItem()
                for (fID,fName) in genealogy:
                    if itemDict.has_key(fID):
                        item = itemDict[fID]
                    else:
                        item = self.trFolders.AppendItem(item,fName)
                        itemDict[fID] = item
                self.trFolders.AppendItem(item,title,data=wx.TreeItemData(row))
        #self.trFolders.Expand(rootItem)
    def action_select(self,event):
        items = self.trFolders.GetSelections()
        row  = [self.trFolders.GetPyData(item) for item in items]
        self.board.actionDocSelect(row)



class TagFolderView(FolderView):
    def __init__(self,parent,id,name,board):
        FolderView.__init__(self,parent,id,name,board)
    def recursiveFill(self,baseItem,docList,refusedKeys,onlyTags):
        usedDoc=[]
        while len(docList)>0:
            currentKeys = refusedKeys[:]
            tags = database.theBase.get_list_of_tags_for(docList,currentKeys,onlyTags)
            if tags is not None:
                tag=tag=tags.fetchone()
            else:
                tag=None
            docList2 = docList[:]
            toShow = docList[:]
            item = baseItem
            if tag is not None:
                title=tag[0]
                nb   =tag[1]
                key  =tag[2]
                if nb>5:
                    #item = self.trFolders.AppendItem(baseItem,'{0} ({1} occurences)'.format(title,nb))
                    item = self.trFolders.AppendItem(baseItem,title)
                    currentKeys.append(key)
                    #print title,currentKeys
                    docList2 = database.theBase.get_list_of_docs_with_all_keys(currentKeys,onlyTags)
                    docList2 = list(set.intersection(set(docList),set(docList2)))
                    if docList2 is None : docList2=[]
                    if len(docList2)>5:
                        docListUnder = self.recursiveFill(item, docList2, currentKeys, onlyTags)
                        toShow = list(set.difference(set(docList2),set(docListUnder)))
                    else:
                        toShow = docList2[:]
            cur = database.theBase.get_by_doc_id(toShow)
            if cur is None : cur=[]
            for row in cur:
                self.trFolders.AppendItem(item,row[database.theBase.IDX_TITLE],data=wx.TreeItemData(row))
                usedDoc.append(row[database.theBase.IDX_ROWID])
            docList3 = list(set.difference(set(docList),set(docList2)))
            if len(docList3)==len(docList) :
                return usedDoc
            docList=docList3[:]
        return usedDoc
    def fillWith(self,docList):
        self.trFolders.DeleteAllItems()
        if docList is None : return
        rootItem=self.trFolders.AddRoot(_('ROOT'),data=wx.TreeItemData(0))
        self.recursiveFill(rootItem, [row[database.theBase.IDX_ROWID] for row in docList],[],True)


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
        wx.Frame.__init__(self, parent, -1, _('MALODOS Main panel'), wx.DefaultPosition, (576, 721), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        fname = Resources.get_icon_filename('APPLICATION')
        appIcon = wx.Icon(fname,wx.BITMAP_TYPE_ANY)
        #appIcon.LoadFile(Resources.get_icon_filename('APPLICATION'),wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)
        self.panel = wx.Panel(self, -1)
        
        self.docPart = wx.SplitterWindow(self.panel,-1,style=wx.SP_3D | wx.SP_LIVE_UPDATE)
        self.docPart.SetSashGravity(0.5)
        
        self.docViewPanel = wx.Panel(self.docPart)
        self.docViewSizer = wx.BoxSizer(wx.VERTICAL)
        self.recordSizer =  wx.BoxSizer(wx.HORIZONTAL)

        self.docWin = docWindow.docWindow(self.docViewPanel,-1)
        self.docViewSizer.Add(self.docWin,1,wx.EXPAND)
        
        self.tbMainBar = self.CreateToolBar()
        self.tbMainBar.AddLabelTool(self.ID_ADD_FILE,'',wx.Bitmap(Resources.get_icon_filename('ADD_FILE')),shortHelp=_('Add an existing file'))
        self.tbMainBar.AddLabelTool(self.ID_ADD_SCAN,'',wx.Bitmap(Resources.get_icon_filename('ADD_SCAN')),shortHelp=_('Scanning a new document'))
        self.tbMainBar.AddLabelTool(self.ID_REMOVE_SEL,'',wx.Bitmap(Resources.get_icon_filename('REMOVE_SELECTION')),shortHelp=_('Remove the current selection from the database'))
        self.tbMainBar.AddLabelTool(self.ID_PRINT_DOC,'',wx.Bitmap(Resources.get_icon_filename('DOC_PRINT')),shortHelp=_('Print the selected document'))
        self.tbMainBar.AddLabelTool(self.ID_DOCTOGO,'',wx.Bitmap(Resources.get_icon_filename('DOC_ZIP')),shortHelp=Resources.get_message('DOC_ZIP'))
        self.tbMainBar.AddLabelTool(self.ID_SURVEY,'',wx.Bitmap(Resources.get_icon_filename('SURVEY_WIN')),shortHelp=_('Open the directory survey window'))
        self.tbMainBar.AddLabelTool(self.ID_PREFS,'',wx.Bitmap(Resources.get_icon_filename('PREFS')),shortHelp=_('Set preferences'))
        self.tbMainBar.AddLabelTool(self.ID_CREDITS,'',wx.Bitmap(Resources.get_icon_filename('CREDITS')),shortHelp=_('Credits'))
        self.tbMainBar.Realize()
        
        self.recordPart = RecordWidget.RecordWidget(self.docViewPanel)
        self.recordPart.lbFileName.Disable()
        self.recordSizer.Add(self.recordPart,1,wx.EXPAND)
        self.btUpdateRecord = wx.BitmapButton(self.docViewPanel,-1,wx.Bitmap(Resources.get_icon_filename('REFRESH')))
        self.btUpdateRecord.SetToolTipString(_('Update'))
        self.btShowExternal = wx.BitmapButton(self.docViewPanel,-1,wx.Bitmap(Resources.get_icon_filename('SYSTEM_SHOW')))
        self.btShowExternal.SetToolTipString(_('System show'))

        #self.btDoOCR = wx.BitmapButton(self.docViewPanel,-1,wx.Bitmap(Resources.get_icon_filename('SYSTEM_SHOW')))
        #self.btDoOCR.SetToolTipString(_('Do OCR'))

        self.docViewSizer.Add(self.recordSizer,0,wx.EXPAND)
        self.recordButtonSizer = wx.BoxSizer(wx.VERTICAL)
        self.recordButtonSizer.Add(self.btUpdateRecord,1,wx.EXPAND)
        self.recordButtonSizer.Add(self.btShowExternal,1,wx.EXPAND)
        #self.recordButtonSizer.Add(self.btDoOCR,1,wx.EXPAND)
        self.recordSizer.Add(self.recordButtonSizer)
        self.docViewPanel.SetSizerAndFit(self.docViewSizer)

        #self.lbDocuments = wx.ListBox(self.docPart, -1,size= (387, 124),style=wx.LB_SORT | wx.LB_EXTENDED )
        self.leftPane = wx.Notebook(self.docPart,-1)
        self.flatViewFrame = FlatView(self.leftPane,-1,_("Flat view"),self)       
        self.leftPane.AddPage(self.flatViewFrame,self.flatViewFrame.GetName())
        self.folderViewFrame = FolderView(self.leftPane,-1,_("Folder view"),self)       
        self.leftPane.AddPage(self.folderViewFrame,self.folderViewFrame.GetName())
        self.tagFolderViewFrame = TagFolderView(self.leftPane,-1,_("Tag Folder view"),self)       
        self.leftPane.AddPage(self.tagFolderViewFrame,self.tagFolderViewFrame.GetName())
        
        self.label2 = wx.StaticText(self.panel, -1, _('filter :'))
        self.tbFilter = wx.TextCtrl(self.panel, -1, '',style=wx.TE_PROCESS_ENTER)
        self.btBuildFilter = wx.Button(self.panel, -1, _('advanced'))
        self.btBuildFilter.Hide()
        

        # sizers
        self.totalWin = wx.BoxSizer(wx.VERTICAL)
        self.upPart = wx.BoxSizer(wx.HORIZONTAL)
        self.searchPart = wx.BoxSizer(wx.HORIZONTAL)
        self.docPart.SplitVertically(self.leftPane,self.docViewPanel)

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
        self.Bind(wx.EVT_TOOL, self.actionAddFile, id=self.ID_ADD_FILE)
        self.Bind(wx.EVT_TOOL, self.actionAddScan, id=self.ID_ADD_SCAN)
        self.Bind(wx.EVT_TOOL, self.actionDoPrint, id=self.ID_PRINT_DOC)
        self.Bind(wx.EVT_TOOL,self.actionStartSurvey,id=self.ID_SURVEY)
        self.Bind(wx.EVT_TOOL,self.actionShowPrefs,id=self.ID_PREFS)
        self.Bind(wx.EVT_TOOL,self.actionDocToGo,id=self.ID_DOCTOGO)
        self.Bind(wx.EVT_TOOL,self.actionRemoveRecord,id=self.ID_REMOVE_SEL)
        self.Bind(wx.EVT_TOOL,self.actionAbout,id=self.ID_CREDITS)
        self.Bind(wx.EVT_BUTTON,self.actionStartExternalApp,self.btShowExternal)
        self.Bind(wx.EVT_BUTTON,self.actionUpdateRecord,self.btUpdateRecord)
        #self.Bind(wx.EVT_BUTTON,self.actionTestOCR,self.btDoOCR)

        # layout assignment
        self.panel.SetSizerAndFit(self.totalWin)
        self.totalWin.Fit(self)
        self.Maximize()
        self.actionSearch(None)
        
    def actionTestOCR(self,event):
        words_dict = data.theData.get_content()
        for w,n in words_dict.items() : print w + '(' + str(n) + ' fois)'
    #===========================================================================
    # click on add scan button
    #===========================================================================
    def actionAddScan(self,event):
        Frame = scanWindow.ScanWindow(self,_("Scan a new document"))
        theData.clear_all()
        Frame.ShowModal()
        theData.clear_all()
        self.actionSearch(None)

    #===========================================================================
    # click on add file button
    #===========================================================================
    def actionAddFile(self,event):
        Frame = addFileWindow.AddFileWindow(self,_("Add a new document"))
        Frame.ShowModal()
        self.actionSearch(None)
    #===========================================================================
    # click on search button (or press enter on the search text entry)
    #===========================================================================
    def actionSearch(self,event):
        # clear the listbox
        #self.flatViewFrame.lbDocuments.Clear()
        sFilter = self.tbFilter.Value
        if len(sFilter)==0:
            docList = database.theBase.find_documents(None)
        else:
            [request,pars] = algorithms.stringFunctions.req_to_sql(self.tbFilter.Value)
            docList = database.theBase.find_sql(request,pars)
        if docList is None : docList=[]
        #if not docList: return
        # otherwise show them in the listbox
        self.docList=[row for row in docList]
        self.flatViewFrame.fillWith(self.docList)
        self.folderViewFrame.fillWith(self.docList)
        self.tagFolderViewFrame.fillWith(self.docList)
#        for row in docList:
#            self.flatViewFrame.lbDocuments.Append(row[database.theBase.IDX_TITLE] , row)
    #===========================================================================
    # actionDocSelect : show the selected item on the doc part
    #===========================================================================
    def actionDocSelect(self,row):
        self.recordPart.setRow(row)
        if len(row)!=1  or row[0] is None: return
        row=row[0]
        docID = row[database.theBase.IDX_ROWID]
        filename = row[database.theBase.IDX_FILENAME]
        title = row[database.theBase.IDX_TITLE]
        description = row[database.theBase.IDX_DESCRIPTION]
        documentDate = row[database.theBase.IDX_DOCUMENT_DATE]
        tags = row[database.theBase.IDX_TAGS]
        folderID_list = database.theBase.folders_list_for(docID)
        try:
            file_md5 = hashlib.md5(open(row[database.theBase.IDX_FILENAME], "rb").read()).hexdigest()
            if row[database.theBase.IDX_CHECKSUM] !=  file_md5:
                Q = utilities.ask(_('The file content has changed! Do you wish to update its signature ?'))
                if Q==wx.ID_YES:
                    if not database.theBase.update_doc_signature(docID, file_md5):
                        wx.MessageBox(_('Unable to update the database'))
        except:
            utilities.show_message(_('Unable to check the file signature...'))
        self.recordPart.SetFields(filename, title, description, documentDate,tags,False,folderID_list)
        #print row
        try:
            theData.load_file(filename)
            self.docWin.resetView()
            self.docWin.showCurrentImage()
        except:
            theData.clear_all()
        
    #===========================================================================
    # actionStartExternalApp : start the system default application associated with the file
    #===========================================================================
    def actionStartExternalApp(self,event):
#        sel = self.flatViewFrame.lbDocuments.GetSelections()
#        if sel == wx.NOT_FOUND or len(sel)!=1: return
#        sel = sel[0]
#        row = self.flatViewFrame.lbDocuments.GetClientData(sel)
        row = self.recordPart.getRow()
        if row is None or len(row)!=1 or row[0] is None: return
        row=row[0]
        filename = row[database.theBase.IDX_FILENAME]
        if os.name == 'posix' :
            subprocess.Popen(['xdg-open', filename])
        else:
            os.startfile(filename)
    #===========================================================================
    # actionUpdateRecord : update the current record
    #===========================================================================
    def actionUpdateRecord(self,event):
        row = self.recordPart.getRow()
        if row is None  or len(row)!=1 or row[0] is None: return
        row=row[0]
        docID = row[database.theBase.IDX_ROWID]
        if self.recordPart.update_record(docID) : self.actionSearch(event)
    #===========================================================================
    # actionRemoveRecord : remove the selected items
    #===========================================================================
    def actionRemoveRecord(self,event):
        rows = self.recordPart.getRow()
#        sel = self.flatViewFrame.lbDocuments.GetSelections()
#        if sel == wx.NOT_FOUND : return
        docID = [row[database.theBase.IDX_ROWID] for row in rows if row is not None]
#        for i in sel:
#            row = self.flatViewFrame.lbDocuments.GetClientData(i)
#            docID.append(row[database.theBase.IDX_ROWID])
        if len(docID)==1:
            msg = _('do you really want to delete this record (') + rows[0][database.theBase.IDX_TITLE] + ')'        
        else:
            msg = _('do you really want to delete these ') + str(len(docID)) + _(' records')
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
        self.actionSearch(event)
    #===========================================================================
    # actionDoPrint : print the current document
    #===========================================================================
    def actionDoPrint(self,event):
        printData = wx.PrintData()
        printData.SetPaperId(wx.PAPER_A4)
        printData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        pdd = wx.PrintDialogData(printData)
        pdd.SetToPage(theData.nb_pages)
        P = wx.Printer(pdd)
        pr = docPrinter.docPrinter()
        if not P.Print(self , pr) :
            wx.MessageBox(_("Unable to print the document"))
    #===========================================================================
    # actionDocToGo :start the doc to go wizard
    #===========================================================================
    def actionDocToGo(self,event):
        rows = self.recordPart.getRow()
        if rows is None or len(rows)<1 :
            rows = self.docList
        docToGo = documentToGo.DocToGoWizard(self,rows)
        docToGo.RunWizard(docToGo.page_chooser)
        self.actionSearch(None)
    #===========================================================================
    # actionAbout : show the about dialog box
    #===========================================================================
    def actionAbout(self,event):
        description = """MALODOS (for MAnagement of LOcal DOcument System) is a simple but useful \
software aimed to help the process of archiving and navigate between the documents presents \
in your hard-drive.
It is written in python and mainly merges numerous external libraries to \
give a fast and simple way to scan and numerically record your personal documents (such \
as invoices, taxes declaration, etc...).
Being written in python, it is portable (works on windows and linux at least, not tested \
on other systems).

The complete documentation can be found here : http://sites.google.com/site/malodospage/
The last version can be downloaded from here : http://code.google.com/p/malodos/
If you like and use this software, please consider to donate to support its development.
"""

        licence = """MALODOS is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free Software Foundation; 
either version 3 of the License, or (at your option) any later version.

MALODOS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have received a copy of 
the GNU General Public License along with File Hunter; if not, write to 
the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA"""


        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon(Resources.get_icon_filename('APPLICATION'), wx.BITMAP_TYPE_PNG))
        info.SetName('MALODOS')
        info.SetVersion('1.2')
        info.SetDescription(description)
        info.SetCopyright('(C) 2010 David GUEZ')
        info.SetWebSite('http://sites.google.com/site/malodospage')
        info.AddArtist('http://icones.pro')
        info.SetLicence(licence)
        wx.AboutBox(info)
        