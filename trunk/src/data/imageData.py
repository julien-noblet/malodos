'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================

singleton class for memory bitmap data management and sharing 

'''


from PIL import Image , ImageSequence
import gfx
import wx
from fpdf import FPDF
import os

class imageData(object):
    val = None
    pil_images = []
    current_image = 0
    image_changed = True
    def __init__(self):
        self.image_void = Image.open('no_preview.png')
    def change_image(self,delta):
        self.current_image += delta
        if self.current_image<0 or self.current_image>len(self.pil_images):
            self.current_image -= delta
        else:
            self.image_changed = True
            
    def get_image(self,image_num=None):
        self.image_changed = False
        if len(self.pil_images)<1 : return self.image_void
        if not image_num : image_num = self.current_image
        if image_num>=0 and image_num<len(self.pil_images) :
            return self.pil_images[image_num]
        else:
            return self.image_void

    def clear_all(self):
        self.pil_images=[]
        self.image_changed = True
            
    def add_image(self,img):
        if img: self.pil_images.append(img)
    def save_file(self,filename):
        if len(self.pil_images)<1 : return False
        try:
            doc = FPDF()
            list_files=[]
            for i in range(len(self.pil_images)):
                fle_tmp = os.tmpnam() + '.png'
                list_files.append(fle_tmp)
                self.pil_images[i].save(fle_tmp)
                doc.AddPage()
                doc.Image(fle_tmp, 0, 0)
            doc.Output(filename)
            for f in list_files : os.remove(f)
        
        except:
            return False
    def load_file(self,filename):
        
        self.clear_all()
        
        try_pdf = filename.lower().endswith('.pdf')
        old_log_level = wx.Log.GetLogLevel()
        wx.Log.SetLogLevel(0)
        if wx.Image.CanRead(filename):
            nmax = wx.Image.GetImageCount(filename)
            for idx in range(nmax):
                try:
                    wxi = wx.Image(filename,index=idx)
                    img = Image.new('RGB', (wxi.GetWidth(), wxi.GetHeight()))
                    img.fromstring(wxi.GetData())
                    self.add_image(img)
                    try_pdf=False
                except:
                    pass
        
        wx.Log.SetLogLevel(old_log_level)
        
        if not try_pdf:
            self.current_image=0
            return
        # This is executed only is try_pdf is TRUE --> loading file was not possible via wx
        try:
            doc = gfx.open("pdf", filename)
            for pagenr in range(1,doc.pages+1):
                page = doc.getPage(pagenr)
                bm = page.asImage(page.width,page.height)
                I = Image.fromstring("RGB",(page.width,page.height),bm)
                self.add_image(I)
            self.current_image=0
        except:
            pass
