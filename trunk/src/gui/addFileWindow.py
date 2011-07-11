'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI dialog for addition of a file into the database
'''
import wx
import os
import database


class RecordWidget(wx.Window):
    def __init__(self,parent,filename='',file_style = wx.FLP_OPEN | wx.FLP_FILE_MUST_EXIST | wx.FLP_USE_TEXTCTRL):
        '''
        Constructor
        '''
        wx.Window.__init__(self, parent)
        self.panel = wx.Panel(self, -1)

        self.totSizer = wx.FlexGridSizer(cols=2,vgap=2,hgap=2)
        self.totSizer.SetFlexibleDirection(wx.HORIZONTAL)
        self.totSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.totSizer.AddGrowableCol(1)
        
        self.txtFileName = wx.StaticText(self.panel , -1 , 'Filename')
        self.lbFileName = wx.FilePickerCtrl(self.panel,-1,path=filename,style=file_style)
        self.totSizer.Add(self.txtFileName,0)
        self.totSizer.Add(self.lbFileName,1,wx.EXPAND)
        
        self.txtTitle = wx.StaticText(self.panel , -1 , 'Title')
        self.lbTitle = wx.TextCtrl(self.panel , -1 , '')
        self.totSizer.Add(self.txtTitle,0)
        self.totSizer.Add(self.lbTitle,1,wx.EXPAND)
        
        self.txtDescription = wx.StaticText(self.panel , -1 , 'Description')
        self.lbDescription = wx.TextCtrl(self.panel , -1 , '')
        self.totSizer.Add(self.txtDescription,0)
        self.totSizer.Add(self.lbDescription,1,wx.EXPAND)
        self.txtDate = wx.StaticText(self.panel , -1 , 'document date')
        self.lbDate = wx.DatePickerCtrl(self.panel , -1)
        self.totSizer.Add(self.txtDate,0)
        self.totSizer.Add(self.lbDate,1)
        
        self.panel.SetSizerAndFit(self.totSizer)
        self.Bind(wx.EVT_SIZE,self.onResize)
        
    def SetFields(self,filename=None,title=None,description=None,date=None):
        if filename : self.lbFileName.SetPath(filename) 
        if title : self.lbTitle.SetValue(title)
        if description : self.lbDescription.SetValue(description)
        #if date : self.lbDate.SetValue(wx.Date)
    def onResize(self,event):
        self.panel.Size = self.Size


        
class AddFileWindow(wx.Dialog):
    '''
    GUI dialog for addition of a file into the database
    '''


    #===========================================================================
    # constructor (building gui)
    #===========================================================================
    def __init__(self,parent, title,filename=None):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, -1, 'Adding a documents to the database',style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        if not filename:
            dlg = wx.FileDialog(self,style=wx.FD_OPEN,message=u'filename of the document to add')
            
            if dlg.ShowModal():
                filename = os.path.join(dlg.Directory,dlg.Filename)
        if not filename : return
        
        self.totSizer = wx.BoxSizer(wx.VERTICAL)
        self.recordPart = RecordWidget(self.panel,filename)
        self.btSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btOk = wx.Button(self.panel,-1,'Ok')
        self.btCancel = wx.Button(self.panel,-1,'Cancel')

        self.btSizer.Add(self.btOk,1,wx.EXPAND)
        self.btSizer.Add(self.btCancel,1,wx.EXPAND)
        
        self.totSizer.Add(self.recordPart,1,wx.EXPAND)
        self.totSizer.Add(self.btSizer,0,wx.EXPAND)

        self.panel.SetSizerAndFit(self.totSizer)
        self.totSizer.Fit(self)
        
        self.Bind(wx.EVT_BUTTON, self.actionDoAdd, self.btOk)
        self.Bind(wx.EVT_BUTTON, self.actionClose, self.btCancel)
    #===========================================================================
    # when closing the window
    #===========================================================================
    def actionClose(self,event):
        self.Close()
    #===========================================================================
    # Click on Add document button
    #===========================================================================
    def actionDoAdd(self,event):
        filename = self.recordPart.lbFileName.GetPath()
        if len(filename) == 0:
            return
        title = self.recordPart.lbTitle.Value
        description = self.recordPart.lbDescription.Value
        documentDate = self.recordPart.lbDate.Value
        keywords = database.theBase.get_keywords_from(title, description, filename)
        # add the document to the database
        if not database.theBase.add_document(filename, title, description, None, documentDate, keywords):
            wx.MessageBox('Unable to add the file to the database')
        else:
            # close the dialog
            self.Close()