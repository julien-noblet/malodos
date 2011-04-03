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
