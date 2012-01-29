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
from scannerAccess import scannerOption
import logging
#import gui.utilities
#import FreeImagePy as FIPY
import data
import os

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
        fle_tmp_tuple = tempfile.mkstemp(suffix='.bmp')
        self.tmpFileName = fle_tmp_tuple[1];
        os.close(fle_tmp_tuple[0]);
        
        self.sourceName= None
    # METHODS
    def listSources(self):
        if not self.sourceManager:
            self.sourceManager = twain.SourceManager(self.imageContainer, ProductName="MALODOS")
        if not self.sourceManager:
            self.sourceName= None
            return []
        return self.sourceManager.GetSourceList()
        
    def chooseSource(self,sourceName=None):
        if not self.sourceManager:
            self.sourceManager = twain.SourceManager(self.imageContainer, ProductName="MALODOS")
        if not self.sourceManager:
            self.sourceName= None
            return "None"
        if self.sourceData:
            self.sourceData.destroy()
            self.sourceData=None
        if sourceName:
            #deviceList = self.sourceManager.GetSourceList()
            try:
                #selected = deviceList.index(sourceName)
                self.sourceData = self.sourceManager.OpenSource(sourceName)
            except:
                self.sourceData = None
            
        if not self.sourceData : self.sourceData = self.sourceManager.OpenSource()
        if self.sourceData:
            self.sourceName = self.sourceData.GetSourceName()
            self.sourceData.destroy()
            self.sourceData=None
        if self.sourceName :
            return self.sourceName
        else:
            return "None"
    def get_options(self,optName=None):
        """ Get current scanner options """
        L =list()
        try:
            if optName is None or optName.lower() == 'manual_multipage' :
                L.append(scannerOption.scannerOption(name='manual_multipage',title=_('Manual multipage'),
                 description=_('Check to manually scan a multiple page document'),
                 scan_type=scannerOption.TYPE_BOOL,value=False))
        except Exception,E:
            logging.debug('ERROR ' + str(E))
        return L
    def useOptions(self,options):
        """Use the specific options."""
        # TO BE DONE
        pass
    def openScanner(self):
        """Connect to the scanner"""
        if not self.sourceManager:
            try:
                self.chooseSource()
            except Exception,E:
                logging.exception('TWAIN : No source ' + str(E))
                return
        if not self.sourceManager or not self.sourceName:
            logging.exception('TWAIN : No source ')
            return
        self.closeScanner()
        self.sourceData = self.sourceManager.OpenSource(self.sourceName)
        self.sourceManager.SetCallback(self.onTwainEvent)
    def closeScanner(self):
        if self.sourceData:
            self.sourceData.destroy()
            self.sourceData=None

    def startAcquisition(self):
        """Begin the acquisition process. The actual acquisition will be notified by
        a callback function."""
        if not self.sourceData:
            self.openScanner()
        if not self.sourceData:
            logging.error('TWAIN : No source')
            return
        try:
            self.sourceData.SetCapability(twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, 100.0)
            self.sourceData.RequestAcquire(1, 1)
        except Exception,E:
            logging.exception('TWAIN acquisition error : '+ str(E))
            self.closeScanner()
                
#-------------------------------------------------------------------------
#
    def onTwainEvent(self, event):
        """This is an event handler for the twain event. It is called
        by the thread that set up the callback in the first place.
        """
        try:
            if event == twain.MSG_XFERREADY:
                self.startTransfer()
            elif event == twain.MSG_CLOSEDSREQ:
                self.sourceData = None
        except:
            # Display information about the exception
            import sys, traceback
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2])
    
    def startTransfer(self):
        """Get the list of images from the scanner"""
        more_to_come = True
        handle = None
        
        while more_to_come :
            try:
                (handle, more_to_come) = self.sourceData.XferImageNatively()
                S = twain.DIBToBMFile(handle)
                f=open(self.tmpFileName,'w')
                f.write(S)
                data.theData.add_image( PIL.Image.open(self.tmpFileName) )
                f.close()
#                img = FIPY.Image()
#                img.load(self.tmpFileName)
#                data.theData.add_image( img )
            except Exception,E:
                print str(E)
                break
        if handle : twain.GlobalHandleFree(handle)
        if self.dataReadyCallback :
                self.dataReadyCallback()
