#!/usr/bin/python 

'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
main application
'''
import wx
import gui.mainBoard as mainWindow
import database
#---------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        if not database.theBase.buildDB():
            return
        frame = mainWindow.MainFrame(None, 'HomeDocs')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(False)

app.MainLoop()
