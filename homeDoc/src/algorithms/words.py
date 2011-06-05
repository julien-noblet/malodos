# -*- coding: utf-8 -*-
'''
Created on 21 juin 2010. Copyright 2010, David GUEZ
@author: david guez (guezdav@gmail.com)
This file is a part of the source code of the MALODOS project.
You can use and distribute it freely, but have to conform to the license
attached to this project (LICENSE.txt file)
=====================================================================
    algorithms operating on strings and words
'''

import re
import subprocess
import tempfile
import os
import codecs
from PIL import Image
import database
import enchant
import gui.utilities
from general import str_to_bool
#===========================================================================
# phonex : simplify the word so that phonetic comparison can be made between
# words not spelled identically
# note : this function must be re-implemented to be adapted to the current language
#===========================================================================
def phonex(word):
    word = word.lower()
    # remove eventual trailing ent, t, s  
    word = re.sub(u'ents$', '',word)
    word = re.sub(u'ent$', '',word)
    word = re.sub(u's$', '',word)
    word = re.sub(u't$', '',word)
    word = re.sub(u'x$', '',word)
    word = re.sub(u'es$', '',word)
    word = re.sub(u'e$', '',word)
    # replace eu eux by 1
    word = word.replace(u'eux', '1')
    word = word.replace(u'eu', '1')
    # replace an en by 2
    word = word.replace(u'ant', '2')
    word = word.replace(u'ent', '2')
    word = word.replace(u'an', '2')
    word = word.replace(u'en', '2')
    # replace ou oo by 3
    word = word.replace(u'ou', '3')
    word = word.replace(u'oo', '3')
    # replace ch sh by 4
    word = word.replace(u'ch', '4')
    word = word.replace(u'sh', '4')
    # replace û ü, u by "un" sound
    word = word.replace(u'u', '5')
    word = word.replace(u'û', '5')
    word = word.replace(u'ü', '5')
    word = word.replace(u'ù', '5')
    # replace ein ain by 5
    word = word.replace(u'ain', '5')
    word = word.replace(u'ein', '5')
    word = word.replace(u'eim', '5')
    word = word.replace(u'aim', '5')
    word = word.replace(u'in', '5')
    word = word.replace(u'un', '5')
    # replace à â by a
    word = word.replace(u'â', 'a')
    word = word.replace(u'à', 'a')
    # replace é, è, er, ez, et, by e
    word = word.replace(u'é', 'e')
    word = word.replace(u'è', 'e')
    word = word.replace(u'ê', 'e')
    word = word.replace(u'ë', 'e')
    word = word.replace(u'er', 'e')
    word = word.replace(u'ez', 'e')
    word = word.replace(u'et', 'e')
    # replace ï î by i
    word = word.replace(u'ï', 'i')
    word = word.replace(u'î', 'i')
    # replace ö ô by o
    word = word.replace(u'eau', 'o')
    word = word.replace(u'au', 'o')
    word = word.replace(u'ö', 'o')
    word = word.replace(u'ô', 'o')
    # replace y by i
    word = word.replace(u'y', 'i')
    # replace ç by s
    word = word.replace(u'ç', 'c')
    # replace ca ce ci cy by sa se si sy
    word = word.replace(u'ca', 'sa')
    word = word.replace(u'ce', 'se')
    word = word.replace(u'ci', 'si')
    # replace c q qu by k
    word = word.replace(u'c', 'k')
    word = word.replace(u'que', 'k')
    word = word.replace(u'qu', 'k')
    word = word.replace(u'q', 'k')
    # replace cc xs ks kc by x
    word = word.replace(u'cc', 'x')
    word = word.replace(u'xs', 'x')
    word = word.replace(u'xc', 'x')
    word = word.replace(u'ks', 'x')
    word = word.replace(u'kc', 'x')
    #replace ph by f
    word = word.replace(u'ph', 'f')
    #replace gn by n
    word = word.replace(u'gn', 'n')
    #replace j by g
    word = word.replace(u'j', 'g')
    #remove any leaving h
    word = word.replace(u'h', '')
    # replace doubled letters by single ones
    oldc = '#'
    newr = ''
    for c in word:
        if oldc != c: newr = newr + c
        oldc = c
    word = newr
    return word

def get_available_ocr_languages():
    return enchant.list_languages()
def get_available_ocr_programs():
    return ['Tesseract','HOCR','GOCR']
def is_accepted_ocr_word(word,dictList,knownTerms):
    try:
        i = knownTerms.index(word)
        return True
    except:
        pass
    if not word.isalpha() : return False
    if len(word)<=3 : return False
    for d in dictList :
        if d.check(word) :
            return True
    return False
def list_to_dict(lst):
    D={}
    for i in lst :
        if not D.has_key(i) : D[i] =  lst.count(i)
    return D
def merge_words(init_dict,added_dict):
    for w,n in added_dict.items():
        if not init_dict.has_key(w) or init_dict[w]<n : init_dict[w] = n
    return init_dict
def ocr_image_file(image_name):
    outname = tempfile.mktemp('.txt')    
    words_dict={}
## ------------ Tesseract
    useTesseract = str_to_bool(database.theConfig.get_param('OCR', 'useTesseract','0'))
    useHOCR = str_to_bool(database.theConfig.get_param('OCR', 'useHOCR','0'))
    useGOCR = str_to_bool(database.theConfig.get_param('OCR', 'useGOCR','0'))
    
    nbOCR = [useTesseract,useHOCR,useGOCR ].count(True)
    if nbOCR==0 : return words_dict
    stateNum=0
    pd = gui.utilities.getGlobalProgressDialog()
    
    test_langs = database.theConfig.get_param('OCR', 'languages','').split(',')
    dictList=[]
    knownTerms = database.theBase.get_all_keywords()
    for l in test_langs :
        try:
            d = enchant.Dict(l)
            dictList.append(d)
        except:
            pass
    if useTesseract:
        try:
            stepToClose=False
            pd.add_to_current_step(0, _('calling tesseract'))
            stateNum+=1
            words =[]
            subprocess.call(['tesseract',image_name,outname,'-l','fra'],stdout=None,stderr=None)
            outname2=outname+'.txt'
            outfile = open(outname2)
            p = outfile.readlines()
            os.remove(outname2)
            pd.add_to_current_step(0.5 / nbOCR)
            pd.new_sub_step(0.5/nbOCR, _('spellchecking'))
            stepToClose=True
            nlines = len(p)
            for line in p:
                line_words = [ w for w in [ unicode(ww).lower() for ww in line.split()] if is_accepted_ocr_word(w,dictList,knownTerms)]
                words = words + line_words
                pd.add_to_current_step(1.0/nlines)
            outfile.close()
            merge_words(words_dict, list_to_dict(words))
            pd.finish_current_step()
        except:
            if stepToClose :
                pd.finish_current_step()
            else:  
                pd.set_current_step_to(1.0/nbOCR)
## ------------ HOCR

    
    if useHOCR:
        try:    
            stepToClose=False
            pd.add_to_current_step(0, _('calling hOCR'))
            stateNum+=1
            words =[]
            subprocess.call(['hocr','-o',outname,'-e','utf-8','-i',image_name])
            outfile = codecs.open(outname,mode='r',encoding='utf-8')
            p = outfile.readlines()
            os.remove(outname)
            #print outname
            pd.add_to_current_step(0.5 / nbOCR)
            pd.new_sub_step(0.5/nbOCR, _('spellchecking'))
            stepToClose=True
            nlines = len(p)
            for line in p:
                line_words = [ w for w in [ unicode(ww).lower() for ww in line.split()] if is_accepted_ocr_word(w,dictList,knownTerms)]
                words = words + line_words
                pd.add_to_current_step(1.0/nlines)
            outfile.close()
            merge_words(words_dict, list_to_dict(words))
            pd.finish_current_step()
        except:
            if stepToClose :
                pd.finish_current_step()
            else:  
                pd.set_current_step_to(1.0/nbOCR)
## ------------ GOCR
    
    if useGOCR:
        try:    
            stepToClose=False
            pd.add_to_current_step(0, _('calling gOCR'))
            stateNum+=1
            words =[]
            subprocess.call(['hocr','-o',outname,'-e','utf-8','-i',image_name])
            outfile = codecs.open(outname,mode='r',encoding='utf-8')
            p = outfile.readlines()
            os.remove(outname)
            #print outname
            pd.add_to_current_step(0.5 / nbOCR)
            pd.new_sub_step(0.5/nbOCR, _('spellchecking'))
            stepToClose=True
            nlines = len(p)
            for line in p:
                line_words = [ w for w in [ unicode(ww).lower() for ww in line.split()] if is_accepted_ocr_word(w,dictList,knownTerms)]
                words = words + line_words
                pd.add_to_current_step(1.0/nlines)
            outfile.close()
            merge_words(words_dict, list_to_dict(words))
            pd.finish_current_step()
        except:
            if stepToClose :
                pd.finish_current_step()
            else:  
                pd.set_current_step_to(1.0/nbOCR)

## ------------ Cuneiform
## ------------ CLARA
## ------------ OCROpus
    
    return words_dict
def ocr_image(pil_image):
    img_name = tempfile.mktemp('.tif')
    try:
        s = pil_image.size
        minS = [3000 , 4000]
        if s[0]<minS[0] or s[1]<minS[1]:
            f=[s[0]/minS[0] , s[1]/minS[1]]
            f = max(f)
            s=[s[0]*f , s[1]*f]
            pil_image.resize(s,Image.ANTIALIAS)
        pil_image.save(img_name)
        words = ocr_image_file(img_name)
        os.remove(img_name)
    except:
        words = []
    return words
    
    #tesseract image_name toto -l fra
