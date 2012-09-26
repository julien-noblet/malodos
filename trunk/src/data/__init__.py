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
theData = imageData.imageData()
currentPassword=''
def get_current_password():
    if currentPassword=='':
        currentPassword = gui.utilities.ask_string(_('No password defined, please give one'), "", "")
    return currentPassword