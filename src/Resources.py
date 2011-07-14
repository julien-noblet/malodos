'''
Created on 25/05/2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================

Resource constants and data retrieve
'''

import sys
import os.path
import database
import ConfigParser


resourceContent = None

def get_resource_dir():
    return os.path.join(os.path.dirname(sys.argv[0]),'../resources')
def read_resource_file():
    global resourceContent
    try:
        resource_file = database.theConfig.get_resource_filename()
    except:
        resource_file = os.path.join(get_resource_dir(),'resources.ini')
    if os.path.exists(resource_file) :
        resourceContent = ConfigParser.SafeConfigParser()
        resourceContent.read(resource_file)

def get_icon_filename(icon_id):
    if not resourceContent : read_resource_file()
    try:
        name = resourceContent.get('icons',icon_id)
        fname= os.path.join(os.path.dirname(sys.argv[0]),'../resources/icons',name)
        return fname
    except:
        return ''
def get_message(message_id,language=None):
    if not resourceContent : read_resource_file()
    if not language :
        language=database.theConfig.get_current_language()
    if not resourceContent.has_section(language) :
        language='english'
    if not resourceContent.has_section(language) :
        return '' 
    try:
        return unicode(resourceContent.get(language,message_id,'')) 
    except:
        return ''
