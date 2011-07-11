'''
Created on 21 juin 2010
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
sane scanner access
'''
import sane
import gui.utilities as GUI
import data

class SaneAccess(object):
    # DATA MEMBERS
    sourceData = None
    dataReadyCallback = None
     
    # CONSTRUCTOR
    def __init__(self,imageContainer,dataReadyCallback=None):
        self.imageContainer = imageContainer
        self.dataReadyCallback = dataReadyCallback
        #self.tmpFileName=tempfile.NamedTemporaryFile().name
        sane.init()
        self.selected = None
        self.sourceData = None
 
    # METHODS
    def chooseSource(self):
        self.devices = sane.get_devices()
        names = [D[2] for D in self.devices]
        self.selected = GUI.multichoice(names)
        if self.selected<0 : self.selected=None
        
    def OpenScanner(self):
        """Connect to the scanner"""
        if not self.selected: self.chooseSource()
        if not self.selected : return
        try:
            scn = self.devices[self.selected][0]
            self.sourceData = sane.open(scn)
        except:
            self.sourceData = None

    def startAcquisition(self):
        """Begin the acquisition process."""
        if not self.sourceData:
            self.OpenScanner()
        if not self.sourceData: return
        
        try:
            img = self.sourceData.scan()
            data.theData.add_image(img)
        except:
            pass
        
        if self.dataReadyCallback:
                self.dataReadyCallback()

