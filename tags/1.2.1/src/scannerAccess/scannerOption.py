'''
Created on 21 juin 2010
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
unified options for scanners, allow to specify options for both twain and sane libs
'''

TYPE_BOOL = 0
TYPE_BUTTON = 4
TYPE_FIXED = 2
TYPE_GROUP = 5
TYPE_INT = 1
TYPE_STRING = 3
class scannerOption :
    def __init__(self,name,title,scan_type,description='',constraint=None,value=None):
        self.name=name
        self.title=title
        self.type=scan_type
        self.description=description
        self.constraint=constraint
        self.value=value
        
