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
    word = re.sub(r'ents$', '',word)
    word = re.sub(r'ent$', '',word)
    word = re.sub(r's$', '',word)
    word = re.sub(r't$', '',word)
    word = re.sub(r'x$', '',word)
    word = re.sub(r'es$', '',word)
    word = re.sub(r'e$', '',word)
    # replace eu eux by 1
    word = word.replace(r'eux', '1')
    word = word.replace(r'eu', '1')
    # replace an en by 2
    word = word.replace(r'ant', '2')
    word = word.replace(r'ent', '2')
    word = word.replace(r'an', '2')
    word = word.replace(r'en', '2')
    # replace ou oo by 3
    word = word.replace(r'ou', '3')
    word = word.replace(r'oo', '3')
    # replace ch sh by 4
    word = word.replace(r'ch', '4')
    word = word.replace(r'sh', '4')
    # replace ein ain by 5
    word = word.replace(r'ain', '5')
    word = word.replace(r'ein', '5')
    word = word.replace(r'eim', '5')
    word = word.replace(r'aim', '5')
    # replace à â by a
    word = word.replace('â', 'a')
    word = word.replace('à', 'a')
    # replace é, è, er, ez, et, by e
    word = word.replace('é', 'e')
    word = word.replace('è', 'e')
    word = word.replace('ê', 'e')
    word = word.replace('ë', 'e')
    word = word.replace('er', 'e')
    word = word.replace('ez', 'e')
    word = word.replace('et', 'e')
    # replace ï î by i
    word = word.replace('ï', 'i')
    word = word.replace('î', 'i')
    # replace ö ô by o
    word = word.replace(r'au', 'o')
    word = word.replace(r'eau', 'o')
    word = word.replace('ö', 'o')
    word = word.replace('ô', 'o')
    # replace û ü by u
    word = word.replace('û', 'u')
    word = word.replace('ü', 'u')
    word = word.replace('ù', 'u')
    # replace y by i
    word = word.replace('y', 'i')
    # replace ç by s
    word = word.replace('ç', 'c')
    # replace ca ce ci cy by sa se si sy
    word = word.replace(r'ca', 'sa')
    word = word.replace(r'ce', 'se')
    word = word.replace(r'ci', 'si')
    # replace c q qu by k
    word = word.replace(r'c', 'k')
    word = word.replace(r'que', 'k')
    word = word.replace(r'qu', 'k')
    word = word.replace(r'q', 'k')
    # replace cc xs ks kc by x
    word = word.replace(r'cc', 'x')
    word = word.replace(r'xs', 'x')
    word = word.replace(r'xc', 'x')
    word = word.replace(r'ks', 'x')
    word = word.replace(r'kc', 'x')
    #replace ph by f
    word = word.replace(r'ph', 'f')
    #replace j by g
    word = word.replace(r'j', 'g')
    #remove any leaving h
    word = word.replace(r'h', '')
    # replace ll mm nn pp rr tt oo ss dd ff gg bb by single copy
    oldc = '#'
    newr = ''
    for c in word:
        if oldc != c: newr = newr + c
        oldc = c
    word = newr
    return word
