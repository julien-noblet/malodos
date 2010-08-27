#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================

interface between the application and the database engine
'''
import sqlite3
import datetime
import hashlib
import string
import gui.utilities
import os.path
import ConfigParser
import algorithms.words

class Configuration(object):
    def __init__(self):
        self.config = None
        if os.name=='nt':
            self.conf_dir = os.path.join(os.path.expanduser('~'),'malodos')
        else:
            self.conf_dir = os.path.join(os.path.expanduser('~'),'.malodos')
        if not os.path.isdir(self.conf_dir) :
            try:
                os.mkdir(self.conf_dir)
            except:
                return
        if not os.path.exists(self.conf_dir) : return
        self.conf_file = os.path.join(self.conf_dir,'malodos.ini')
        if not os.path.exists(self.conf_file) :
            try:
                theFile = open(self.conf_file,'w')
            except:
                return
            self.config = ConfigParser.SafeConfigParser()
            self.config.add_section('database')
            self.set_database_name( os.path.join(self.conf_dir,'malodos.db'))
            self.config.add_section('language')
            #self.set_installed_languages(u'english,français,עברית')
            self.set_installed_languages(u'english')
            self.set_current_language('english')
            self.config.add_section('survey')
            self.set_survey_directory_list( (os.path.join(self.conf_dir,'documents'),) , (0,))
            self.set_survey_extension_list( 'png tif tiff pdf jpg jpeg gif bmp doc txt odt' )
            self.commit_config()
            theFile.close()
        self.read_config()

    def get_survey_extension_list(self):
        if not self.config : raise "Configuration not found"
        return self.config.get('survey','extension_list')
    def set_survey_extension_list(self,S):
        if not self.config : raise "Configuration not found"
        self.config.set('survey','extension_list',S)
    def get_survey_directory_list(self):
        if not self.config : raise "Configuration not found"
        S = self.config.get('survey','directory_list')
        return self.decode_dir_list(S)
    def set_survey_directory_list(self,dir_list,recursiveIndex):
        if not self.config : raise "Configuration not found"
        S = self.encode_dir_list(dir_list, recursiveIndex)
        self.config.set('survey','directory_list',S)
    def get_installed_languages(self):
        if not self.config : raise "Configuration not found"
        return self.config.get('language','installed').split(',')
    def set_installed_languages(self,S):
        if not self.config : raise "Configuration not found"
        if hasattr(S, '__iter__') : S = ','.join(S)
        self.config.set('language','installed',S)
    def get_current_language(self):
        if not self.config : raise "Configuration not found"
        return self.config.get('language','current')
    def set_current_language(self,S):
        if not self.config : raise "Configuration not found"
        self.config.set('language','current',S)
    def get_database_name(self):
        if not self.config : raise "Configuration not found"
        return self.config.get('database', 'filename')
    def set_database_name(self,S):
        if not self.config : raise "Configuration not found"
        return self.config.set('database', 'filename',S)
    def get_resource_filename(self):
        if not self.config : raise "Configuration not found"
        return self.config.get('general', 'resourceFile')
    def read_config(self):
        if os.path.exists(self.conf_file) :
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(self.conf_file)
    def commit_config(self):
            try:
                theFile = open(self.conf_file,'w')
                self.config.write(theFile)
                theFile.close()
                return True
            except:
                return False
    def encode_dir_list(self , dir_list , checked):
        answer = ""
        for i in range(len(dir_list)) :
            if i in checked : answer = answer + '*'
            answer = answer + dir_list[i] + '|'
        return answer
    def decode_dir_list(self,S):
        items_list = S.split('|')
        checked = []
        dir_list = []
        
        for item in items_list :
            item = item.strip()
            if len(item)<1 : continue
            if item[0] == '*' :
                checked.append(len(dir_list))
                item=item[1:]
            dir_list.append(item)
        return (dir_list , checked)
    
class Base(object):
    '''(
    this class is the interface between the application and the database engine
    )'''
    #===========================================================================
    # constants
    #===========================================================================
    documents_tableName = 'documents'
    keywords_tableName = 'keywords'
    docWords_tableName = 'docWords'
    persons_tableName = 'persons'
    params_tableName = 'parameters'
    param_DB_VERSION='DB_VERSION'
    DB_VERSION=1.0    
        
    #===========================================================================
    # constructor
    #===========================================================================
    def __init__(self,base_name):
        '''
        Constructor
        '''
        self.base_name = base_name
        try:
            self.connexion = sqlite3.connect(self.base_name)
            #Q = 'PRAGMA foreign_keys = ON'
            #self.connexion.execute(Q)
        except:
            print("Unable to connect to database")

    #===========================================================================
    # test if a table exists
    #===========================================================================
    def exist_table(self, table_name):
        '''(
        Test if a given table exists
        )'''
        try:
            cur = self.connexion.execute("SELECT name FROM sqlite_master WHERE name = '" + table_name + "' AND type='table' ;")
            return (cur and cur.arraysize>0)
        except:
            return False
    #===========================================================================
    # create the table
    #===========================================================================
    def create_table(self, table_name, structure):
        '''(
        Automatically create the asked table, if not already exists in the database
        )'''
        sql_statement = "CREATE TABLE IF NOT EXISTS " + table_name + "(" + structure + ")"
        try:
            self.connexion.execute(sql_statement)
            return True
        except:
            return False
    def win32_samefile(self,p1,p2):
        return os.path.abspath(p1).lower() == os.path.abspath(p2).lower()
    #===========================================================================
    # build the database
    #===========================================================================
    def buildDB(self):
        '''( 
        create the database (all the tables)
        )'''
        self.create_table(self.documents_tableName, 'title TEXT(64), description TEXT(256), filename TEXT(256), registerDate INTEGER, registeringPersonID INTEGER, documentDate INTEGER,checksum TEXT')
        self.create_table(self.keywords_tableName, 'keyword TEXT PRIMARY KEY , soundex_word TEXT ')
        sql_statement = "CREATE INDEX IF NOT EXISTS SOUNDEX ON " + self.keywords_tableName + "(soundex_word)"
        try:
            self.connexion.execute(sql_statement)
        except:
            pass
        #self.create_table(self.docWords_tableName, 'keyID INTEGER references ' + self.keywords_tableName + '(ROWID) ,docID INTEGER references ' + self.documents_tableName + '(ROWID)')
        self.create_table(self.docWords_tableName, 'keyID INTEGER  ,docID INTEGER ')
        self.create_table(self.persons_tableName, 'name TEXT')
        self.create_table(self.params_tableName, 'name TEXT , value TEXT')
        if os.name == 'nt' or os.name == 'win32' :
            self.connexion.create_function("IS_IN_DIR", 2, lambda fname,dirname : self.win32_samefile(os.path.dirname(fname), dirname))
        else:
            self.connexion.create_function("IS_IN_DIR", 2, lambda fname,dirname : os.path.samefile(os.path.dirname(fname), dirname))
        self.connexion.create_function("EXTENSION", 1, lambda fname : os.path.splitext(fname)[1])
        self.connexion.create_function("PHONEX", 1, lambda word : algorithms.words.phonex(word))
        db_version = self.get_parameter(self.param_DB_VERSION)
        if not db_version:
            self.set_parameter(self.param_DB_VERSION, self.DB_VERSION)
            db_version = self.get_parameter(self.param_DB_VERSION)
        db_version = float(db_version)
        if db_version > self.DB_VERSION:
            gui.utilities.show_message('Unstable state: Your database version is newer than the program itself...')
            return False
        return True
    #===========================================================================
    # set a parameter
    #===========================================================================
    def set_parameter(self,parameter_name,parameter_value):
        Q = 'SELECT value FROM ' + self.params_tableName +' WHERE name=?'
        try:
            cur = self.connexion.execute(Q,(parameter_name,))
            if not cur or not cur.fetchone():
                Q = 'INSERT INTO ' + self.params_tableName +' VALUES (?,?)'
                cur = self.connexion.execute(Q,(parameter_name,str(parameter_value)))
            else:
                Q = 'UPDATE ' + self.params_tableName +' SET value=? WHERE name=?'
                cur = self.connexion.execute(Q,(str(parameter_value),parameter_name))
            self.connexion.commit()
            return True
        except:
            return False
    #===========================================================================
    # get a parameter
    #===========================================================================
    def get_parameter(self,parameter_name):
        Q = 'SELECT value FROM ' + self.params_tableName +' WHERE name=?'
        try:
            cur = self.connexion.execute(Q,(parameter_name,))
            row = cur.fetchone()
            if row :
                return row[0]
            else:
                return None
        except :
            return None
         
    #===============================================================================
    # add a new document to the database
    #===============================================================================
    def add_document(self, fileName, title = 'untitled', description = '', registeringPerson = None, documentDate = None, keywords = None):
        '''(
        Add a new document to the database
        only the filename is mandatory
        the registering date is automatically taken from the system
        )'''
        docID = None
        registeringDate = format(datetime.date.today(),'%d-%m-%y')
        cur = self.connexion.cursor()
        if not documentDate : documentDate = registeringDate
        personID = 0
        file_md5 = hashlib.md5(open(fileName, "rb").read()).hexdigest()

        # try to find the given person (if a value is given)
        if registeringPerson:
            sql_statement = 'SELECT ROWID FROM ' + self.persons_tableName + " WHERE name=?"
            try:
                cur = self.connexion.execute(sql_statement,(registeringPerson,))
                row = cur.fetchone()
                # if not found --> create the person in the database
                if not row:
                    sql_statement = "INSERT INTO " + self.persons_tableName + " VALUES (?)"
                    cur = self.connexion.execute(sql_statement,(registeringPerson,))
                    personID = cur.lastrowid
                else:
                    personID = row[0]
            except:
                pass
        try:
            # add the document entry in the database
            #sql_statement = 'INSERT INTO ' + self.documents_tableName + " VALUES ('" + title + "','" + description + "','" + fileName + "','" + str(registeringDate) + "'," + str(personID) + ",'" + str(documentDate) + "','" + str(file_md5) + "')"
            sql_statement = 'INSERT INTO ' + self.documents_tableName + " VALUES (?,?,?,?,?,?,?)"
            cur = self.connexion.execute(sql_statement,(title,description,fileName,registeringDate,personID,documentDate,str(file_md5)))
            docID = cur.lastrowid
        except:
            return False
        self.connexion.commit()
        if not keywords :
            return True # finishes if no keyword to register

        
        # find the list of keyword not yet registered
        keywords =  map(lambda s:s.lower() , keywords)
        self.update_keywords_for(docID,keywords)
        return True
    #===============================================================================
    # finding keywords rows
    #===============================================================================
    def find_keywords(self, keywords):
        '''(
        find all the rows of the keywords table corresponding to the given input
        keyword is a list of list of words
        ((word11,word12,...word1N1),(word21,word22,...word2N2),...,(wordM1,wordM2,...,wordMNM))
        means (word11 AND word12 AND ... AND word1N1) OR ... OR  (wordM1 AND wordM2 AND ... AND wordMNM)
        )'''
        cur = None
        if not keywords : return None
        keywords =  map(lambda s:algorithms.words.phonex(s) , keywords)
        # first : find the keyword in the keywords table
        if isinstance(keywords,list):
            Q = "SELECT ROWID FROM " + self.keywords_tableName + " WHERE soundex_word IN " + self.make_placeholder_list(len(keywords))
        else:
            Q = "SELECT ROWID FROM " + self.keywords_tableName + " WHERE soundex_word = ?"
                
        try:
            #print "finding keys via " + Q
            cur = self.connexion.execute(Q , keywords)
            return cur
        except:
            return None

    #===============================================================================
    # find documents corresponding to keywords
    #===============================================================================
    def find_documents(self, keywords = None):
        '''(
        find all the document of the database that contain any of the given keywords
        keyword is a list of list of words
        ((word11,word12,...word1N1),(word21,word22,...word2N2),...,(wordM1,wordM2,...,wordMNM))
        means (word11 AND word12 AND ... AND word1N1) OR ... OR  (wordM1 AND wordM2 AND ... AND wordMNM)
        )'''
       
        cur = None
        sql_statement = 'SELECT *,ROWID FROM ' + self.documents_tableName
        if keywords:
            # first : find the keyword in the keyword table
            cur = self.find_keywords(keywords)
            if not cur or cur.arraysize<1: return None
            # if some keywords are found, find the corresponding doc lines
            lst = self.rows_to_str(cur)
            Q = "SELECT docID FROM " + self.docWords_tableName + " WHERE keyID IN " + lst
            #print Q
            try:
                cur = self.connexion.execute(Q)
            except:
                return None
            # cur now contain the docID to take
            if cur:
                rowIDList = self.rows_to_str(cur)
                sql_statement += ' WHERE ROWID IN ' + str(rowIDList)
        try:
            cur = self.connexion.execute(sql_statement)
        except:
            return None
        return cur
    #===========================================================================
    # create a list with n placeholder (?,?,...?) 
    #===========================================================================
    def make_placeholder_list(self,n):
        if n<1 : return '()'
        if n<2 : return '(?)'
        return '(' + '?,' * (n-1) + '?)'
    #===========================================================================
    # utility function transform the content of a python list into an (e1,e2,...) string format
    #===========================================================================
    def iterable_to_sqlStrList(self,iterable,stringChar='"'):
        if len(iterable)<1: return '()'
        sql_list = [ stringChar + str(i) + stringChar for i in iterable]
        sql_list = '(' + ','.join(sql_list) + ')'
        return sql_list
    #===========================================================================
    # utility function transform the content of a column from cur into a (e1,e2,...) string format
    #===========================================================================
    def rows_to_str(self,cur,idx=0):
        return self.iterable_to_sqlStrList([x[idx] for x in cur])
    #===========================================================================
    # return the list of keywords absent from the database
    #===========================================================================
    def find_absent_keywords(self,keywords):
#        keywords_str = [ '"' + i + '"' for i in keywords]
#        keywords_str = '(' + ','.join(keywords_str) + ')'
        
        Q = 'SELECT keyword FROM ' + self.keywords_tableName + ' WHERE keyword IN ' + self.make_placeholder_list(len(keywords))
        cur = self.connexion.execute(Q,keywords)
        already_present = [ i[0] for i in cur]
        return [ s for s in keywords if s not in already_present]
    #===========================================================================
    # remove_document : remove the selected documents (docID must be a list of ids)
    # and all the keys referencing it
    #===========================================================================
    def remove_documents(self,docID):
        # first find and delete all the corresponding lines in keyword index
        Q = 'DELETE FROM ' + self.docWords_tableName + ' WHERE docID IN ' + self.make_placeholder_list(len(docID))
        try:
            self.connexion.execute(Q,docID)
        except:
            return
        # then delete the documents entries themselves
        Q = 'DELETE FROM ' + self.documents_tableName + ' WHERE ROWID IN ' + self.make_placeholder_list(len(docID))
        try:
            self.connexion.execute(Q,docID)
            self.connexion.commit()
        except:
            return
    #===========================================================================
    # update_keywords_for : remove all the keyword reference to docID
    # and  replace by a new list
    #===========================================================================
    def update_keywords_for(self,docID,keywords):
        # first : delete all the keyword references to docID
        if not hasattr(docID,'__iter__') : docID = (docID,)

        Q = 'DELETE FROM ' + self.docWords_tableName + ' WHERE docID IN ' + self.make_placeholder_list(len(docID))
        try:
            self.connexion.execute(Q,docID)
        except Exception as E:
            print E.message
            return False
        # add all absent keywords to the keywords table
        absents = self.find_absent_keywords(keywords)
        absents = map(lambda x:(x,algorithms.words.phonex(x)) , absents)
        Q = 'INSERT INTO ' + self.keywords_tableName + ' VALUES (?,?)'
        try:
            self.connexion.executemany(Q,absents )
        except:
            return False
        # get back all the keyword IDs
        Q = 'SELECT ROWID FROM ' + self.keywords_tableName + ' WHERE keyword IN ' + self.make_placeholder_list(len(keywords))
        addedKeys = []
        try:
            cur = self.connexion.execute(Q,keywords)
            addedKeys = [ (row[0],) for row in cur]
        except:
            return False
        
        # add the new keyID to the table
        for adoc_i in docID:
            Q = 'INSERT INTO ' + self.docWords_tableName + ' VALUES (?,' +  str(adoc_i) + ')'
            try:
                self.connexion.executemany(Q , addedKeys)
            except:
                return False
        try:
            self.connexion.commit()
        except:
            return False
        return True
    
    #===========================================================================
    # update_doc : replace the values for a given doc
    #===========================================================================
    def update_doc(self,docID,title,description,documentDate,filename):
        Q = 'UPDATE ' + self.documents_tableName + ' SET title=? , description=?, documentDate=? WHERE ROWID=?'
        try:
            self.connexion.execute(Q,(title,description,documentDate,docID))
            self.connexion.commit()
        except:
            return False
        keywords = self.get_keywords_from(title, description, filename)
        return self.update_keywords_for(docID,keywords)
    #===========================================================================
    # update_doc : replace the values for a given doc
    #===========================================================================
    def update_doc_signature(self,docID,file_md5):
        Q = 'UPDATE ' + self.documents_tableName + ' SET checksum=? WHERE ROWID=?'
        try:
            self.connexion.execute(Q,(file_md5,docID))
            self.connexion.commit()
        except:
            return False
        return True
    #===========================================================================
    # get_keywords_from : find the keywords from a document
    #===========================================================================
    def get_keywords_from(self,title,description,filename):  
        keywords_title = string.split(title, ' ')
        keywords_title = [i for i in keywords_title if len(i)>3]
        
        keywords_descr = string.split(description, ' ')
        keywords_descr = [i for i in keywords_descr if len(i)>3]
        
        keywords = set(keywords_title+keywords_descr)
        keywords =  map(lambda s:s.lower() , keywords)
        return keywords
    #===========================================================================
    # get_files_under : retrieve all the documents of the database whose filename
    # are on the directory <directory> (directly and not under subdir)
    #===========================================================================
    def get_files_under(self,directory,acceptedExt=None):
        if acceptedExt:
            Q = "SELECT filename FROM " + self.documents_tableName + " WHERE IS_IN_DIR(filename,?) AND EXTENSION(filename) IN " + self.make_placeholder_list(len(acceptedExt))
        else:
            Q = "SELECT filename FROM " + self.documents_tableName + " WHERE IS_IN_DIR(filename,?) "
        try:
            if acceptedExt:
                acceptedExt = [ i for i in acceptedExt];
                acceptedExt.insert(0, directory)
                cur = self.connexion.execute(Q,acceptedExt)
            else:
                cur = self.connexion.execute(Q,(directory,))
            return cur
        except:
            return ()
        
