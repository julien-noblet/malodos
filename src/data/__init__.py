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

theData = imageData.imageData()
currentPassword=''
def get_current_password(msg=_('No password defined, please give one')):
    global currentPassword
    cont = len(currentPassword)<10
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
            cont=False
    return currentPassword
def clear_current_password():
    global currentPassword
    currentPassword=''