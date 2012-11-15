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
def get_password(msg=_('Please gives your password for data encryption/decryption.'),checker=lambda pss:False):
    cont = True
    while cont:
        password = gui.utilities.ask_password(msg)
        if len(password)==0:
            cont=False
        elif len(password)<4:
            gui.utilities.show_message(_('The password length must be at least 4  char long (at least 8 is recommended). Please gives another one..'))
        else:
            M =md5.new()
            M.update(password)
            S1 = M.digest()
            x=''
            for i in range(len(password)-1,-1,-1) : x = x+password[i]
            M.update(x)
            S2 = M.digest()
            password = S1+S2
            cont=checker(password)       
    return password
    
def get_current_password(msg=_('Please gives your password for data encryption/decryption.'),forceAsk=False,checkOld=True):
    global currentPassword
    if not forceAsk and len(currentPassword)>=10 : return currentPassword
    salt = theConfig.get_param('encryption','salt','')
    hashed = theConfig.get_param('encryption','hash','')
    def checker(pss):
        if checkOld and (salt!='' and hashed!='' and bcrypt.hashpw(pss, salt) != hashed):
            cont = gui.utilities.ask(_('The password does not corresponds to the registered one, do you want to give it back ?..'))
        else:
            cont=False
        return cont
    currentPassword = get_password(msg, checker)
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