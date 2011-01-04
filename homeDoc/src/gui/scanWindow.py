'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI dialog for addition of a scanned document to the database
'''

import wx
import os
from gui import utilities
if os.name == 'posix' :
	from scannerAccess import saneAccess
else:
	from scannerAccess import twainAccess
import gui.docWindow as docWindow
import data
import RecordWidget
import database

class ScanWindow(wx.Dialog):
	scanner = None
	#==============================================================================
	# constructor (gui building)
	#==============================================================================
	def __init__(self, parent, title):
		wx.Dialog.__init__(self, parent, -1, 'Scanning a new document', wx.DefaultPosition, (372, 700), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER  | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
		self.panel = wx.Panel(self, -1)

		self.totalWin = wx.BoxSizer(wx.VERTICAL)
		self.upPart = wx.GridSizer(3,2)

		self.stSource = wx.StaticText(self.panel,-1,"Source :")
		self.btSource = wx.Button(self.panel, -1, 'Select Scanner')
		self.btScan = wx.Button(self.panel, -1, 'Scan')
		self.cbMultiplePage = wx.CheckBox(self.panel, -1, 'Manual MultiPage')
		self.btSave = wx.Button(self.panel, -1, 'Record')
		
		self.docWin = docWindow.docWindow(self.panel,-1)
		self.recordPart = RecordWidget.RecordWidget(self.panel,file_style=wx.FLP_SAVE | wx.FLP_OVERWRITE_PROMPT | wx.FLP_USE_TEXTCTRL)
		self.upPart.Add(wx.StaticText(self.panel,-1,"Source :"),0,wx.ALL | wx.ALIGN_CENTRE_VERTICAL)
		self.upPart.Add(self.stSource,0,wx.ALL| wx.ALIGN_CENTRE_VERTICAL)
		self.upPart.Add(self.btSource,0,wx.EXPAND | wx.CENTER)
		self.upPart.Add(self.btScan,0,wx.EXPAND | wx.CENTER)
		self.upPart.Add(self.btSave,0,wx.EXPAND | wx.CENTER)
		self.upPart.Add(self.cbMultiplePage,0,wx.EXPAND | wx.CENTER)
	
		self.totalWin.Add(self.upPart,0,wx.ALIGN_TOP|wx.EXPAND)
		self.totalWin.Add(self.recordPart,0,wx.EXPAND)
		self.totalWin.Add(self.docWin,1,wx.ALIGN_BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)
		# BINDING EVENTS
		self.Bind(wx.EVT_BUTTON, self.actionChooseSource, self.btSource)
		self.Bind(wx.EVT_BUTTON, self.actionPerformScan, self.btScan)
		self.Bind(wx.EVT_BUTTON, self.actionSaveRecord, self.btSave)
		# OTHER INITIALISATIIONS
		if os.name == 'posix' :
			self.scanner = saneAccess.SaneAccess(self.GetHandle(),self.onNewScannerData)
		else:
			self.scanner = twainAccess.TwainAccess(self.GetHandle(),self.onNewScannerData)
		self.panel.SetSizerAndFit(self.totalWin)
		self.SetSize(self.GetSize())
		self.stSource.Label = self.scanner.chooseSource(database.theConfig.get_current_scanner())
		self.SetSizeWH(400,600)
	def actionChooseSource(self,event):
		self.stSource.Label = self.scanner.chooseSource()
	def actionPerformScan(self,event):
		auto_cont=self.cbMultiplePage.GetValue()
		cont=True
		data.theData.clear_all()
		while cont:
			self.scanner.startAcquisition()
			if auto_cont:
				x = utilities.ask('Do you want to add new page(s) ?')
				if x != wx.ID_YES:
					cont=False
			else:
				cont=False
			
	def actionSaveRecord(self,event):
		fname = self.recordPart.lbFileName.GetPath()
		if fname == '' :
			wx.MessageBox('You must give a valid filename to record the document')
			return
		try:
			if not data.theData.save_file(fname) : raise Exception
		except:
			wx.MessageBox('Unable to add the file to the disk')
			return
		if not self.recordPart.do_save_record():
			wx.MessageBox('Unable to add the file to the database')
		else:
			# close the dialog
			self.Close()
	def onNewScannerData(self):
		data.theData.current_image=0
		self.docWin.showCurrentImage()
	