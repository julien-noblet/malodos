'''
Created on 21 juin 2010
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
almost copy/paste of the source from twain module website (http://twainmodule.sourceforge.net)
'''
import twain
import tempfile
import PIL
import gui.utilities
#import FreeImagePy as FIPY
import data

class NoScannerFoundError(Exception):
    pass

class TwainAccess(object):
    # DATA MEMBERS
    sourceManager = None
    sourceData = None
    tmpFileName = None
    dataReadyCallback = None
    # CONSTRUCTOR
    def __init__(self,imageContainer,dataReadyCallback=None):
        self.imageContainer = imageContainer
        self.dataReadyCallback = dataReadyCallback
        self.tmpFileName=tempfile.NamedTemporaryFile().name
    # METHODS
    def chooseSource(self):
        if not self.sourceManager:
            self.sourceManager = twain.SourceManager(self.imageContainer, ProductName="homeDocs")
        if not self.sourceManager:
            raise NoScannerFoundError
            return
        if self.sourceData:
            self.sourceData.destroy()
            self.sourceData=None
        #self.sourceData = self.sourceManager.OpenSource()

    def OpenScanner(self):
        """Connect to the scanner"""
        if not self.sourceManager:
            try:
                self.chooseSource()
            except:
                return
        if not self.sourceManager:
            return
        if self.sourceData:
            self.sourceData.destroy()
            self.sourceData=None
        self.sourceData = self.sourceManager.OpenSource()
        self.sourceManager.SetCallback(self.OnTwainEvent)

    def startAcquisition(self):
        """Begin the acquisition process. The actual acquisition will be notified by
        a callback function."""
        if not self.sourceData:
            self.OpenScanner()
        if not self.sourceData: return
        try:
            self.sourceData.SetCapability(twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, 100.0)
        except:
            pass
        self.sourceData.RequestAcquire(1, 1)
                
#-------------------------------------------------------------------------
#
    def OnTwainEvent(self, event):
        """This is an event handler for the twain event. It is called
        by the thread that set up the callback in the first place.
        """
        try:
            if event == twain.MSG_XFERREADY:
                self.StartTransfer()
            elif event == twain.MSG_CLOSEDSREQ:
                self.sourceData = None
        except:
            # Display information about the exception
            import sys, traceback
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2])
    
    def StartTransfer(self):
        """Get the list of images from the scanner"""
        more_to_come = True
        handle = None
        
        while more_to_come :
            try:
                (handle, more_to_come) = self.sourceData.XferImageNatively()
                twain.DIBToBMFile(handle, self.tmpFileName)
                data.theData.add_image( PIL.Image.open(self.tmpFileName) )
#                img = FIPY.Image()
#                img.load(self.tmpFileName)
#                data.theData.add_image( img )
            except:
                break
        if handle : twain.GlobalHandleFree(handle)
        if self.dataReadyCallback :
                self.dataReadyCallback()
