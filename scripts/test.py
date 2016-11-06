# -*- coding: utf-8 -*-
# from nltk.stem import *
# from nltk.stem.porter import *
# stemmer = PorterStemmer()
# plurals = ['caresses', 'caress', 'flies', 'dies', 'mules', 'denied',
# 			'died', 'agreed', 'owned', 'humbled', 'sized',
# 			'meeting', 'stating', 'siezing', 'itemization',
# 			'sensational', 'traditional', 'reference', 'colonizer',
# 			'plotted']
# singles = [stemmer.stem(plural) for plural in plurals]

# print singles

# print ord('-')
# print ord('a')
# print ord('.')
import re, string
s ='adfa®.adf,'
table = string.maketrans("","")
s = s.translate(table, string.punctuation)
s =  re.sub(r'[^\x00-\x7f]',r'', s) 
print s
