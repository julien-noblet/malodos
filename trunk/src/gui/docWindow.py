'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================

GUI to be embedded into a frame, that contains a canvas and buttons
for navigating between the  images managed by the data singleton

'''
import wx
#import PIL
#import FreeImagePy as FIPY
import data
class docWindow(wx.Window) :
    #===========================================================================
    # constructor (gui building)
    #===========================================================================
    def __init__(self, parent,id):
        wx.Window.__init__(self, parent, id)
        self.panel = wx.Panel(self, -1)
        self.img = None
        self.totalWin = wx.BoxSizer(wx.VERTICAL)
        self.buttonPart = wx.BoxSizer(wx.HORIZONTAL)
        self.btLeft = wx.Button(self.panel,-1,'<')
        self.btRight = wx.Button(self.panel,-1,'>')
        self.lbImage = wx.StaticText(self.panel,-1,'No image')

        self.canvas = wx.StaticBitmap(self.panel, -1)
        self.totalWin.Add(self.buttonPart,0,wx.ALIGN_TOP|wx.EXPAND)
        self.totalWin.Add(self.canvas,1,wx.GROW|wx.EXPAND|wx.ALIGN_CENTER)
        self.buttonPart.Add(self.btLeft ,0)
        self.buttonPart.Add(self.btRight,0)
        self.buttonPart.Add(self.lbImage,1,wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.actionPreviousImage, self.btLeft)
        self.Bind(wx.EVT_BUTTON, self.actionNextImage, self.btRight)
        self.Bind(wx.EVT_SIZE,self.onResize)
        
        self.canvas.SetSize(wx.Size(200,300))
        self.panel.SetSizerAndFit(self.totalWin)

        
    #===========================================================================
    # show the current image in the canvas
    #===========================================================================
    def showCurrentImage(self):
        self.panel.SetSize(self.GetSizeTuple())
        self.totalWin.Layout()
        if len(data.theData.pil_images)==0:
            self.lbImage.SetLabel('no image')
        else:
            self.lbImage.SetLabel('image ' + str(data.theData.current_image+1) + '/' + str(len(data.theData.pil_images)))
        if data.theData.image_changed or not self.img:
            pil_image = data.theData.get_image()
            self.img = wx.EmptyImage(pil_image.size[0],pil_image.size[1])
            self.img.SetData(pil_image.convert("RGB").tostring())
        if not self.img : return    
        #img = data.theData.get_image().convertToWx()

        # calculating stretching factors
        size_ini = self.canvas.GetSize()
        disp_ini = self.canvas.GetPosition()
        size = self.canvas.GetSize()
        origSize = self.img.GetSize()
        # factor to apply in each direction
        factors = [ float(size[0])/origSize[0] , float(size[1])/origSize[1] ]
        # take only the lowest factor and apply to both x and y direction
        # (thus keeping the initial aspect ratio)
        if factors[0]>factors[1] :
            size[0] = factors[1] * origSize[0]
            size[1] = factors[1] * origSize[1]
        else:
            size[0] = factors[0] * origSize[0]
            size[1] = factors[0] * origSize[1]
        if size[0]>0 and size[1]>0:
            # do stretching and drawing if sizes are ok
            displ = [ disp_ini[0] + (size_ini[0] - size[0])/2 , disp_ini[1] + (size_ini[1] - size[1])/2 ]
            self.canvas.SetPosition(displ)
            self.canvas.SetSize( [size[0],size[1] ])
            self.canvas.SetBitmap(self.img.Scale(size[0],size[1]).ConvertToBitmap())
    #===========================================================================
    # on prev button click
    #===========================================================================
    def actionPreviousImage(self,event):
        if data.theData.current_image>0 :
            data.theData.change_image(-1)
            self.showCurrentImage()
    #===========================================================================
    # on next button click
    #===========================================================================
    def actionNextImage(self,event):
        if data.theData.pil_images and data.theData.current_image+1<len(data.theData.pil_images) :
            data.theData.change_image(1)
            self.showCurrentImage()
    #===========================================================================
    # called when resizing window/pane
    #===========================================================================
    def onResize(self,event):
        self.showCurrentImage()
