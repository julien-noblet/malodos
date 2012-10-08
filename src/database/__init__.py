'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
'''
import db
import logging
theConfig = db.Configuration()
try:
    theBase = db.Base(theConfig.get_database_name())
except Exception as E:
    logging.exception( "Unable to connect to database->"+str(E))