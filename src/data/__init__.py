'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================

'''
import imageData
import gui.utilities
import Crypto.Hash.MD5 as md5
import bcrypt
from database import theConfig

theData = imageData.imageData()
currentPassword=''
def get_current_password(msg=_('Please gives your password for data encryption/decryption.'),forceAsk=False,checkOld=True):
    global currentPassword
    cont = forceAsk or len(currentPassword)<10
    salt = theConfig.get_param('encryption','salt','')
    hashed = theConfig.set_param('encryption','hash','')
    while cont:
        currentPassword = gui.utilities.ask_password(msg)
        if len(currentPassword)==0:
            cont=False
        elif len(currentPassword)<4:
            gui.utilities.show_message(_('The password length must be at least 4  char long (at least 8 is recommended). Please gives another one..'))
        else:
            M =md5.new()
            M.update(currentPassword)
            S1 = M.digest()
            x=''
            for i in range(len(currentPassword)-1,-1,-1) : x = x+currentPassword[i]
            M.update(x)
            S2 = M.digest()
            currentPassword = S1+S2
            if checkOld and (salt!='' and hashed!='' and bcrypt.hashpw(currentPassword, salt) != hashed):
                cont = gui.utilities.ask(_('The password does not corresponds to the registered one, do you want to give it back ?..'))
            else:
                cont=False
    if currentPassword != '':
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(currentPassword, salt)
        theConfig.set_param('encryption','salt',salt)
        theConfig.set_param('encryption','hash',hashed)
        theConfig.commit_config()
        
    return currentPassword
def clear_current_password():
    global currentPassword
    currentPassword=''