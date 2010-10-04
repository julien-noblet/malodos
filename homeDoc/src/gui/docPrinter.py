'''
Created on 3 oct. 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
printing a document

'''


import wx
from data import theData

class docPrinter(wx.Printout):
    '''
    class for printing the image present in data singleton 
    '''
    def __init__(self):
        "Prepares the Printing object."
        wx.Printout.__init__(self)
        self.printer_config = wx.PrintData()
        self.printer_config.SetPaperId(wx.PAPER_LETTER)
    def HasPage(self, page_num):
        "Does the page exists."
        return theData.nb_pages>=page_num

    def OnPrintPage(self, page_num):
        img = theData.get_image(page_num)
        if not img : return False
        dc = self.GetDC()
        if not dc : return False
        bm = img.ConvertToBitmap()
        
        dc.DrawBitmap(bm)
#        imgDC = wx.MemoryDC()
#        imgDC.SelectObject(bm)
#        dc.Blit(0,0,imgDC.GetWidth(),imgDC.GetHeight(),imgDC)
        return True
    