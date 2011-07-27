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
import database
import utilities
class DocToGoWizard (wx.wizard.Wizard):
    def __init__(self,parent,row_list):
        wx.wizard.Wizard.__init__(self,parent,-1,_('Document to go wizard'))
        self.page_chooser = PageActionChooser(self)
        self.page_database_export = PageActionDatabaseExport(self)
        self.page_archive_export = PageActionArchiveCreation(self)
        self.page_archive_import = PageActionArchiveOpening(self)
        self.row_list=row_list
        self.Bind(wx.wizard.EVT_WIZARD_FINISHED, self.on_finished)
        self.Bind(wx.wizard.EVT_WIZARD_CANCEL, self.on_cancel)
        self.GetPageAreaSizer().Add(self.page_chooser)
    def on_cancel(self,event):
        if utilities.ask(_('Are you sure you want to cancel to document to go wizard ?')) != wx.ID_YES : event.Veto()
    def on_finished(self,event):
        sel = self.page_chooser.rbContent.GetSelection()
        sel = self.page_chooser.choice_list.keys()[sel]
        if sel == self.page_chooser.EXPORT_DATABASE:
            filename = self.page_database_export.fcFileChooser.GetPath()
            if filename=='' : 
                utilities.show_message(_("The filename can't be empty"))
                event.Veto()
            else:
                database.theBase.export_database(filename, self.row_list)
        elif sel==self.page_chooser.EXPORT_ARCHIVE:
            filename = self.page_archive_export.fcFileChooser.GetPath()
            if filename=='' : 
                utilities.show_message(_("The filename can't be empty"))
                event.Veto()
            else:
                database.theBase.export_archive(filename, self.row_list)
        elif sel==self.page_chooser.IMPORT_ARCHIVE :
            filename = self.page_archive_import.fcFileChooser.GetPath()
            dirname = self.page_archive_import.dcDirChooser.GetPath()
            if filename=='' or dirname=='': 
                utilities.show_message(_("The filename and dirname can't be empty"))
                event.Veto()
            else:
                database.theBase.import_archive(filename, dirname)

class PageActionChooser (wx.wizard.PyWizardPage):
    EXPORT_DATABASE=1
    EXPORT_ARCHIVE=2
    IMPORT_ARCHIVE=3
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.choice_list = { self.EXPORT_DATABASE:_('Export all of part of the database.') ,
                             self.EXPORT_ARCHIVE :_('Create an archive with some or all of your documents, along with a database to browse into.'),
                             self.IMPORT_ARCHIVE :_('Open an existing archive.')   }
        self.rbContent =  wx.RadioBox(self,label=_('What action do you want to take'),choices=self.choice_list.values(),style=wx.RA_VERTICAL)
        self.sizer.Add(self.rbContent,0,flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(self.sizer)
    def GetNext(self):
        sel = self.rbContent.GetSelection()
        sel = self.choice_list.keys()[sel]
        if sel == self.EXPORT_DATABASE:
            return self.Parent.page_database_export
        elif sel==self.EXPORT_ARCHIVE:
            return self.Parent.page_archive_export
        elif sel==self.IMPORT_ARCHIVE :
            return self.Parent.page_archive_import
    def GetPrev(self):
        return None


class PageActionDatabaseExport (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        s = _('Path of exported database')
        self.sizer.Add(wx.StaticText(self,label=s))
        self.fcFileChooser =  wx.FilePickerCtrl(self,message=s,wildcard='*.db',style=wx.FLP_SAVE|wx.FLP_OVERWRITE_PROMPT|wx.FLP_USE_TEXTCTRL)
        self.sizer.Add(self.fcFileChooser,0,flag=wx.EXPAND|wx.CENTER|wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(self.sizer)
    def GetNext(self):
        return None
    def GetPrev(self):
        return self.Parent.page_chooser

class PageActionArchiveCreation (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        s = _('Path of exported archive')
        self.sizer.Add(wx.StaticText(self,label=s))
        self.fcFileChooser =  wx.FilePickerCtrl(self,message=s,wildcard='*.zip',style=wx.FLP_SAVE|wx.FLP_OVERWRITE_PROMPT|wx.FLP_USE_TEXTCTRL)
        self.sizer.Add(self.fcFileChooser,0,flag=wx.EXPAND|wx.CENTER|wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(self.sizer)
    def GetNext(self):
        return None
    def GetPrev(self):
        return self.Parent.page_chooser
class PageActionArchiveOpening (wx.wizard.PyWizardPage):
    def __init__(self,parent):
        wx.wizard.PyWizardPage.__init__(self,parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        s = _('Path of archive to import')
        self.sizer.Add(wx.StaticText(self,label=s))
        self.fcFileChooser =  wx.FilePickerCtrl(self,message=s,wildcard='*.zip',style=wx.FLP_OPEN|wx.FLP_FILE_MUST_EXIST|wx.FLP_USE_TEXTCTRL)
        self.sizer.Add(self.fcFileChooser,0,flag=wx.EXPAND|wx.CENTER|wx.ALIGN_CENTER_VERTICAL)
        s = _('Path of directory into which the archive will be extracted')
        self.sizer.Add(wx.StaticText(self,label=s))
        self.dcDirChooser =  wx.DirPickerCtrl(self,message=s,style=wx.DIRP_DIR_MUST_EXIST|wx.DIRP_USE_TEXTCTRL)
        self.sizer.Add(self.dcDirChooser,0,flag=wx.EXPAND|wx.CENTER|wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(self.sizer)
    def GetNext(self):
        return None
    def GetPrev(self):
        return self.Parent.page_chooser