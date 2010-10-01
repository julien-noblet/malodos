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
import Resources
import wx.lib.mixins.rubberband

class docWindow(wx.Window) :
    center=[0.5,0.5]
    window=[1.0,1.0]
    dragLastPos = None
    #===========================================================================
    # constructor (gui building)
    #===========================================================================
    def __init__(self, parent,id):
        wx.Window.__init__(self, parent, id)
        self.panel = wx.Panel(self, -1)
        self.img = None
        self.totalWin = wx.BoxSizer(wx.VERTICAL)
        self.buttonPart = wx.BoxSizer(wx.HORIZONTAL)
        self.btLeft = wx.BitmapButton(self.panel,-1,wx.Bitmap(Resources.get_icon_filename('PREVIOUS_PAGE')))
        self.btRight = wx.BitmapButton(self.panel,-1,wx.Bitmap(Resources.get_icon_filename('NEXT_PAGE')))
        #self.btZoom = wx.BitmapButton(self.panel,-1,wx.Bitmap(Resources.get_icon_filename('ZOOM_PAGE')))
        #self.btPan = wx.BitmapButton(self.panel,-1,wx.Bitmap(Resources.get_icon_filename('PAN_PAGE')))
        self.lbImage = wx.StaticText(self.panel,-1,'No image')

        self.canvas = wx.StaticBitmap(self.panel, -1)
        self.totalWin.Add(self.buttonPart,0,wx.ALIGN_TOP|wx.EXPAND)
        self.totalWin.Add(self.canvas,1,wx.GROW|wx.EXPAND|wx.ALIGN_CENTER)
        self.buttonPart.Add(self.btLeft ,0)
        self.buttonPart.Add(self.btRight,0)
        #self.buttonPart.Add(self.btZoom,0)
        #self.buttonPart.Add(self.btPan,0)
        self.buttonPart.Add(self.lbImage,1,wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.actionPreviousImage, self.btLeft)
        self.Bind(wx.EVT_BUTTON, self.actionNextImage, self.btRight)
        #self.Bind(wx.EVT_BUTTON, self.actionGetZoom, self.btZoom)
        self.Bind(wx.EVT_SIZE,self.onResize)
        self.Bind(wx.EVT_MOUSEWHEEL,self.onMouseWheelEvent)
        self.Bind(wx.EVT_MOTION,self.onMouseMotion)
        self.Bind(wx.EVT_LEFT_UP,self.onMouseLeftUp)
        
        self.canvas.SetSize(wx.Size(200,300))
        self.panel.SetSizerAndFit(self.totalWin)

    def onMouseLeftUp(self,event):
        self.dragLastPos = None
    def onMouseWheelEvent(self,event):
        rot = -float(event.GetWheelRotation()) / event.GetWheelDelta() * 0.05
        self.window[0] += rot;
        self.window[1] += rot;
        if self.window[0]<0 : self.window[0]=0;
        if self.window[1]<0 : self.window[1]=0;
        if self.window[0]>1 : self.window[0]=1;
        if self.window[1]>1 : self.window[1]=1;
        self.showCurrentImage()
    def onMouseMotion(self,event):
        #if not event.Dragging() : return
        if not self.dragLastPos : self.dragLastPos = event.GetPosition();
        delta  = event.GetPosition() - self.dragLastPos
        print delta
    def actionGetZoom(self,event):
        pass
        #R = wx.lib.mixins.rubberband.RubberBand(self.canvas)
        
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
        
        # build and test the viewing rect
        viewRect = wx.Rect((self.center[0]-self.window[0]/2)*self.img.GetWidth() \
                          ,(self.center[1]-self.window[1]/2)*self.img.GetHeight() \
                          ,self.window[0]*self.img.GetWidth() ,self.window[1]*self.img.GetHeight())
        if viewRect.x<0 : viewRect.x=0;
        if viewRect.y<0 : viewRect.y=0;
        if viewRect.x>= self.img.GetWidth() : viewRect.x = self.img.GetWidth() -1
        if viewRect.y>= self.img.GetHeight() : viewRect.y = self.img.GetWidth() -1
        if viewRect.width<1 : viewRect.width = 1
        if viewRect.height<1 : viewRect.height = 1
        if viewRect.width > self.img.GetWidth() : viewRect.width = self.img.GetWidth()
        if viewRect.height > self.img.GetHeight() : viewRect.height = self.img.GetHeight()
        if viewRect.x + viewRect.width > self.img.GetWidth() : viewRect.x = self.img.GetWidth() - viewRect.width
        if viewRect.y + viewRect.height > self.img.GetHeight() : viewRect.y = self.img.GetHeight() - viewRect.height
        
        theImage = self.img.ConvertToBitmap()
        theImage = theImage.GetSubBitmap(viewRect)
        theImage = theImage.ConvertToImage()

        # calculating stretching factors
        size_ini = self.canvas.GetSize()
        disp_ini = self.canvas.GetPosition()
        size = self.canvas.GetSize()
        origSize = theImage.GetSize()
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
            self.canvas.SetBitmap(theImage.Scale(size[0],size[1]).ConvertToBitmap())
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
