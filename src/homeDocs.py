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
import gettext
import os
import locale
import sys
import logging
import algorithms

exe_name = os.path.dirname(os.path.abspath(os.path.join(algorithms.__file__,'..')))
if not exe_name:
    try:
        exe_name = os.getcwd()
    except:
        pass
if not exe_name :
    try:
        exe_name = os.path.dirname(os.path.realpath(sys.executable))
    except:
        pass
if not exe_name :
    try:
        exe_name = os.path.dirname(__file__)
    except:
        pass
if not exe_name: exe_name = '.'
ld = os.path.join(exe_name ,'locale')
# code bellow copied from http://www.journaldunet.com/developpeur/tutoriel/pyt/070607-python-traduction/2.shtml 
if os.name == 'nt':
    lang = locale.getdefaultlocale()[0][:2]
    try:
        cur_lang = gettext.translation('malodos', localedir=ld, languages=[lang])
        cur_lang.install(unicode=True)
    except IOError:
        gettext.install('malodos', localedir = ld, unicode=True)
else :
    gettext.install('malodos', localedir = ld, unicode=True)
# end of copy part
import wx
import gui.mainBoard as mainWindow
import database
logfilename=os.path.join(database.theConfig.conf_dir ,'messages.log')
logging.basicConfig(filename=logfilename, filemode='w', level=logging.DEBUG,format='%(levelname)s %(message)s at %(filename)s on line %(lineno)d function %(funcName)s ')
logging.info('Starting MALODOS')
#---------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        self.SetAppName('MALODOS')
        if not database.theBase.buildDB():
            return False
        if len(sys.argv)>1 and os.path.exists(sys.argv[1]): database.theBase.use_base(sys.argv[1])
        frame = mainWindow.MainFrame(None, 'MALODOS')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


app = MyApp(False)

app.MainLoop()
logging.info('Exiting MALODOS')