# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re

import operator
from _io import open
import config

fdist = config.fdist

def subtitle_to_words( subtitles ):

    #  Remove HTML
    review_text = BeautifulSoup(subtitles, "lxml").get_text() 
    
    #  Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    #  convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    
    return( meaningful_words) 


text=open('Sample_text.txt','r')
withoutStopWords=subtitle_to_words(text)

def key_extractor_using_brown_word_feq(words):
    keyword_dict={}
    abs_occurences_dict={}
    for m in words:
        if m not in abs_occurences_dict.keys():
            abs_occurences_dict[m]=1
        else:
            abs_occurences_dict[m]+=1
        keyword_dict[m]=abs_occurences_dict[m]/float((fdist[m.lower()]+1))
        
    sorted_dict = sorted(keyword_dict.items(), key=operator.itemgetter(1),reverse=True)
    for i in range(0,int(len(sorted_dict))):
        if len(sorted_dict[i][0])>2:
            print(sorted_dict[i][0])
key_extractor_using_brown_word_feq(withoutStopWords)