'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI part to show/modify a record data
'''
import wx
import database
import datetime
#import pyPdf

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

        self.txtTags = wx.StaticText(self.panel , -1 , 'Tags')
        self.lbTags = wx.TextCtrl(self.panel , -1 , '')
        self.totSizer.Add(self.txtTags,0)
        self.totSizer.Add(self.lbTags,1,wx.EXPAND)
        
        self.txtDate = wx.StaticText(self.panel , -1 , 'document date')
        self.lbDate = wx.DatePickerCtrl(self.panel , -1,style=wx.DP_DROPDOWN)
        self.totSizer.Add(self.txtDate,0)
        self.totSizer.Add(self.lbDate,1)
        
        self.panel.SetSizerAndFit(self.totSizer)
        self.Bind(wx.EVT_SIZE,self.onResize)
    
    def clear_all(self):
        self.lbFileName.SetPath('')
        self.lbTitle.SetValue('')
        self.lbDescription.SetValue('')
        self.lbTags.SetValue('')
    def SetFields(self,filename=None,title=None,description=None,date=None,tags=None):
        if filename : self.lbFileName.SetPath(filename) 
        if title : self.lbTitle.SetValue(title)
        if description : self.lbDescription.SetValue(description)
        if tags : self.lbTags.SetValue(tags)
        if date :
            dt = wx.DateTime.Today()
            dt.SetDay(date.day)
            dt.SetMonth(date.month-1)
            dt.SetYear(date.year)
            self.lbDate.SetValue(dt)
    def onResize(self,event):
        self.panel.Size = self.Size
    def do_save_record(self):
        filename = self.lbFileName.GetPath()
        if len(filename) == 0:
            return
#        if filename[-4:].lower()=='.pdf':
#            content=""
#            pdf = pyPdf.PdfFileReader(file(filename, "rb"))
#            # Iterate pages
#            for i in range(0, pdf.getNumPages()):
#                # Extract text from page and add to content
#                content += pdf.getPage(i).extractText() + "\n"
#                # Collapse whitespace
#                #content = " ".join(content.replace("\xa0", " ").strip().split())
#            print "file content:"
#            print content
        title = self.lbTitle.Value
        tags = self.lbTags.Value
        description = self.lbDescription.Value
        documentDate = self.lbDate.Value
        documentDate=datetime.date(year=documentDate.GetYear(),month=documentDate.GetMonth()+1,day=documentDate.GetDay())
        keywordsGroups = database.theBase.get_keywordsGroups_from(title, description, filename , tags)
        # add the document to the database
        return database.theBase.add_document(filename, title, description, None, documentDate, keywordsGroups,tags)
