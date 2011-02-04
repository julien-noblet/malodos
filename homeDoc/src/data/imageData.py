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
import tempfile
import sys
import os.path

class imageData(object):
    val = None
    pil_images = []
    current_image = 0
    image_changed = True
    current_file=None
    nb_pages=0
    def __init__(self):
        void_file = os.path.join(os.path.dirname(sys.argv[0]),'../resources','no_preview.png')
        self.image_void = Image.open(void_file)
    def change_image(self,delta):
        " change the current page by delta"
        self.current_image += delta
        if self.current_image<0 or self.current_image>len(self.pil_images):
            self.current_image -= delta
        else:
            self.image_changed = True
            
    def get_image(self,image_num=None):
        "get a given image (current image if not specified)"
        self.image_changed = False
        if len(self.pil_images)<1 : return self.image_void
        if not image_num : image_num = self.current_image
        if image_num>=0 and image_num<len(self.pil_images) :
            return self.pil_images[image_num]
        else:
            return self.image_void
    def apply_transposition(self,image_num,mode):
        "apply the mode transposition to asked image or all if not image specified"
        if image_num is None:
            for image_num in range(len(self.pil_images)):
                self.pil_images[image_num] = self.pil_images[image_num].transpose(mode)
        else:
            if image_num>=0 and image_num<len(self.pil_images):
                self.pil_images[image_num] = self.pil_images[image_num].transpose(mode)
        self.image_changed = True                
    def swap_x(self,image_num=None):
        "swap the image along the x axis (or all images is image_num is not given)"
        self.apply_transposition(image_num,Image.FLIP_LEFT_RIGHT )
    def swap_y(self,image_num=None):
        "swap the image along the y axis (or all images is image_num is not given)"
        self.apply_transposition(image_num,Image.FLIP_TOP_BOTTOM )
    def rotate(self,image_num=None , nbRot=1):
        "swap the image along the y axis (or all images is image_num is not given)"
        mode = None
        if nbRot==1 : 
            mode = Image.ROTATE_90
        elif nbRot==2 :
            mode = Image.ROTATE_180
        elif nbRot==3 :
            mode = Image.ROTATE_270
        else :
            return
        self.apply_transposition(image_num, mode)

    def clear_all(self):
        "clear the image data"
        self.pil_images=[]
        self.image_changed = True
        self.current_file=None
    def add_image(self,img):
        "add an image to the cache"
        if img: self.pil_images.append(img)
    def save_file(self,filename):
        "save the image data to a PDF file"
        if len(self.pil_images)<1 : return False
        try:
            doc = FPDF()
            list_files=[]
            for i in range(len(self.pil_images)):
                fle_tmp_tuple = tempfile.mkstemp(suffix='.png')
                fle_tmp = fle_tmp_tuple[1];
                list_files.append(fle_tmp)
                self.pil_images[i].save(fle_tmp)
                doc.AddPage()
                doc.Image(fle_tmp, 0, 0)
            doc.Output(filename)
            for f in list_files : os.remove(f)
            return True
        except:
            return False
    def load_file(self,filename,page=None):
        "Load a given file into memory (only the asked page if given, all the pages otherwise)"
        
        self.clear_all()
        
        try_pdf = filename.lower().endswith('.pdf')
        old_log_level = wx.Log.GetLogLevel()
        wx.Log.SetLogLevel(0)
        if wx.Image.CanRead(filename):
            nmax = wx.Image.GetImageCount(filename)
            if page:
                if page>=nmax: return
                R = [page]
            else :
                R = range(nmax)
            for idx in R:
                try:
                    wxi = wx.Image(filename,index=idx)
                    img = Image.new('RGB', (wxi.GetWidth(), wxi.GetHeight()))
                    img.fromstring(wxi.GetData())
                    self.current_file=filename
                    self.nb_pages = nmax
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
            nmax = doc.pages
            if page:
                if page>=nmax: return
                R = [page]
            else :
                R = range(nmax)
            for pagenr in range(nmax):
                page = doc.getPage(pagenr+1)
                bm = page.asImage(page.width,page.height)
                I = Image.fromstring("RGB",(page.width,page.height),bm)
                self.current_file=filename
                self.nb_pages = nmax
                self.add_image(I)
            self.current_image=0
        except:
            pass
