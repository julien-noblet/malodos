'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
    general purpose algorithms
'''

def str_to_bool(s):
    s=s.lower()
    return s=='1' or s=='on' or s=='true' or s=='yes' or s=='+'