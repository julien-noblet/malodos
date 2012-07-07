#!/usr/bin/python 

'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
MALODOS (for MAnagement of LOcal DOcument System) is a simple but useful
software aimed to help the process of archiving and navigate between the documents presents
in your hard-drive.
It is written in python and mainly merges numerous external libraries to
give a fast and simple way to scan and numerically record your personal documents (such
as invoices, taxes declaration, etc...).
Being written in python, it is portable (works on windows and linux at least, not tested
on other systems).

The complete documentation can be found here : http://sites.google.com/site/malodospage/
The latest version can be downloaded from here : http://code.google.com/p/malodos/
If you like and use this software, please consider to donate to support its development.
'''
import gettext
import os
import locale
import sys
import logging
import algorithms
import getopt
import datetime
__version__ = '1.3.1'


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

import database
def print_query_result(sFilter,frmt='%t',date_format='%d-%m-%Y'):
    import algorithms.stringFunctions as SF
#    print "Querying with " + sFilter
    if len(sFilter)==0:
        docList = database.theBase.find_documents(None)
    else:
        [request,pars] = SF.req_to_sql(sFilter)
        docList = database.theBase.find_sql(request,pars)
    if docList is None : docList=[]
    docList=[row for row in docList]
    for row in docList:
        s = unicode(frmt)
        docID = row[database.theBase.IDX_ROWID]
        foldList = database.theBase.folders_list_for(docID)
        folderStringList=[]
        for folderID in foldList:
            folderHierarchy = '/'.join(database.theBase.folders_genealogy_of(folderID, True))
            folderStringList.append(folderHierarchy)
        strFolders=','.join(folderStringList)
        try:
            s = s.replace('%t',row[database.theBase.IDX_TITLE])
            s = s.replace('%d',row[database.theBase.IDX_DESCRIPTION])
            s = s.replace('%D',row[database.theBase.IDX_DOCUMENT_DATE].strftime(date_format))
            s = s.replace('%R',row[database.theBase.IDX_REGISTER_DATE].strftime(date_format))
            s = s.replace('%m',row[database.theBase.IDX_CHECKSUM])
            s = s.replace('%F',strFolders)
            #s = frmt.replace_all('%u',str(row[database.theBase.IDX_REGISTER_PERSON_ID]))
            s = s.replace('%f',row[database.theBase.IDX_FILENAME])
        except Exception as E:
            logging.exception('Problem in query format : ' + str(E))
            print 'Problem in query format : ' + str(E)
        print s.encode('utf8','replace')

def start_gui():
    import wx
    import gui.mainBoard as mainWindow
    #---------------------------------------------------------------------------
    class MyApp(wx.App):
        def OnInit(self):
            self.SetAppName('MALODOS')
            if not database.theBase.buildDB():
                return False
            #if len(sys.argv)>1 and os.path.exists(sys.argv[1]): database.theBase.use_base(sys.argv[1])
            frame = mainWindow.MainFrame(None, 'MALODOS')
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = MyApp(False)
    app.MainLoop()

if __name__ == "__main__":
    logfilename=os.path.join(database.theConfig.conf_dir ,'messages.log')
    logging.basicConfig(filename=logfilename, filemode='w', level=logging.DEBUG,format='%(levelname)s %(message)s at %(filename)s on line %(lineno)d function %(funcName)s ')
    logging.info('Starting MALODOS')
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvd:q:a:f:F:", ["help","version","database=","format=","add=","dateFormat=","title=",'description=','tags=','folders=','date='])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    query_format='%t'
    date_format='%d-%m-%Y'
    title='Untitled'
    description=''
    folderList=[]
    docDate=datetime.date.today()
    tagList=''
    
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        if o in ('-v','--version'):
            print __version__
            sys.exit(0)
        if o in ('-d','--database'): database.theBase.use_base(a)
        if o in ('-f','--format'): query_format=a
        if o in ('-F','--dateFormat'): date_format=a
        if o in ('--title'): title=a
        if o in ('--description'): description=a
        if o in ('--date'): docDate=datetime.datetime.strptime(a,date_format).date()
        if o in ('--folders'): folderList=a
        if o in ('--tags'): tagList=a
        if o in ('-q','--query'):
            print_query_result(a,query_format,date_format)
            sys.exit(0)
        if o in ('-a','--add'):
            keywordsGroups = database.theBase.get_keywordsGroups_from(title, description, a , tagList)
            database.theBase.add_document(a, title, description, None, docDate, keywordsGroups,tagList,folderList)
            sys.exit(0)
    start_gui()
    logging.info('Exiting MALODOS')
