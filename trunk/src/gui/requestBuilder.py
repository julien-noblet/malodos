'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
GUI dialog for building a search request
'''

import wx
class builder(wx.Dialog):
    '''
    GUI dialog for addition of a file into the database
    '''


    #===========================================================================
    # constructor (building gui)
    #===========================================================================
    def __init__(self,parent):
        '''
        Constructor
        '''
        wx.Dialog.__init__(self, parent, -1, _('Generation of a search request'),style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.RESIZE_BORDER | 0 | 0 | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        self.totSizer = wx.BoxSizer(wx.VERTICAL)

        
        
        self.panel.SetSizerAndFit(self.totSizer)
        self.totSizer.Fit(self)
        
