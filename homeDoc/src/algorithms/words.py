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

def get_available_languages():
        return enchant.list_languages()
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
def ocr_image_file(image_name,usedOCR):
    outname = tempfile.mktemp('.txt')    
    words_dict={}
    ocrConf = database.theConfig.get_ocr_configuration()
#    usedOCR = []
#    for s in ocrConf.get_available_ocr_programs() :
#        if str_to_bool(database.theConfig.get_param('OCR', 'use'+s,'0')) :
#            usedOCR.append(s)

    nbOCR = len(usedOCR)
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

    for prg in usedOCR:
        try:
            stepToClose=False
            s= _('calling %s') %prg
            pd.add_to_current_step(0,s)
            stateNum+=1
            ocr_words =[]
            seq = ocrConf.build_call_sequence(prg, image_name, outname)
            #print  prg,image_name,outname,seq
            subprocess.call(seq,stdout=None,stderr=None)
            outfile = open(outname)
            p = outfile.readlines()
            pd.add_to_current_step(0.5/nbOCR )
            pd.new_sub_step(0.5/nbOCR, _('spellchecking'))
            stepToClose=True
            nlines = len(p)
            for line in p:
                line_words = [ w for w in [ unicode(ww).lower() for ww in line.split()] if is_accepted_ocr_word(w,dictList,knownTerms)]
                ocr_words = ocr_words + line_words
                pd.add_to_current_step(1.0/nlines)
            outfile.close()
            os.remove(outname)
            merge_words(words_dict, list_to_dict(ocr_words))
        finally:
            if stepToClose: pd.finish_current_step()
    #print words_dict
    return words_dict
    
def ocr_image(pil_image):
    words_dict={}
    usedOCR = {}
    ocrConf = database.theConfig.get_ocr_configuration()
    pd = gui.utilities.getGlobalProgressDialog()
    for s in ocrConf.get_available_ocr_programs() :
        if str_to_bool(database.theConfig.get_param('OCR', 'use'+s,'0')) :
            frm = ocrConf.get_needed_image_format(s)
            if usedOCR.has_key(frm) :
                usedOCR[frm].append(s)
            else:
                usedOCR[frm] = [s]
    nbOCR=0
    for frm in usedOCR.keys(): nbOCR += len(usedOCR[frm])
    for frm in usedOCR.keys():
        img_name = tempfile.mktemp('.'+frm)
        print 'using file %s' %img_name
        pd.new_sub_step(len(usedOCR[frm])/nbOCR, _('spellchecking'))
        try:
            s = pil_image.size
            minS = [3000 , 4000]
            if s[0]<minS[0] or s[1]<minS[1]:
                f=[s[0]/minS[0] , s[1]/minS[1]]
                f = max(f)
                s=[s[0]*f , s[1]*f]
                pil_image.resize(s,Image.ANTIALIAS)
            pil_image.save(img_name)
            frm_words = ocr_image_file(img_name,usedOCR[frm])
            os.remove(img_name)
        except:
            frm_words = {}
        pd.finish_current_step()
        words_dict = merge_words(words_dict, frm_words)
    return words_dict
    
    #tesseract image_name toto -l fra
