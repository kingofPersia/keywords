# -*- coding: utf-8 -*-
from __future__ import print_function
import pickle
import operator
from itertools import islice
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
from _io import open
import config

from sklearn.feature_extraction.text import TfidfVectorizer

fdist = config.fdist


def get_sorted_phrase_list(text):
    print("excecuting key extraction.... ")
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2), min_df = 0, stop_words = 'english')
    tfidf_matrix =  tf.fit_transform(text)
    feature_names = tf.get_feature_names()
    dense = tfidf_matrix.todense()

    dict_phrase={}
    for i in range(0,len(dense)):
        
        episode = dense[i].tolist()[0]
        phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
        sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
        
        for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores]:
            dict_phrase[phrase]=score
            
    sorted_dict_phrase = sorted(dict_phrase.items(), key=operator.itemgetter(1),reverse=True)
    phrase_list=[]
    
    for i in range(0,int(len(sorted_dict_phrase))):
        phrase_list.append(sorted_dict_phrase[i][0])
       
    return phrase_list

def subtitle_to_words( subtitles ):

    #  Remove HTML
    review_text = BeautifulSoup(subtitles, "lxml").get_text() 
    
    #  Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    
    #  convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   

    return( meaningful_words)

def two_words_key_extractor(words,wikiTitles):
    print("running algorithm to find key words.....")
    keyword_dict={}
    abs_occurences_dict={}
    for m in words:
        
        if m not in abs_occurences_dict.keys():
            abs_occurences_dict[m]=1
        else:
            abs_occurences_dict[m]+=1

                 
        if  fdist [m.lower()]==0 and m+'\n'  in wikiTitles and len(m.split())==2:
            
                firstWord=m.split()[0]
                secondWord=m.split()[1]
                firstWordFreqScore=fdist[firstWord.lower()]
                secondWordFreqScore=fdist[secondWord.lower()]
                keyword_dict[m]=abs_occurences_dict[m]/(firstWordFreqScore+secondWordFreqScore+1)
                
                
    sorted_two_word_tags = sorted(keyword_dict.items(), key=operator.itemgetter(1),reverse=True)
    return sorted_two_word_tags 
             
def single_word_key_extractor(words,wikiTitles):
    keyword_dict={}
    abs_occurences_dict={}
    for m in words:
        if m not in abs_occurences_dict.keys():
            abs_occurences_dict[m]=1
        else:
            abs_occurences_dict[m]+=1
        if  fdist [m.lower()]==0 and m+'\n'  in wikiTitles:
            keyword_dict[m]=1+ (abs_occurences_dict[m]/float((fdist[m.lower()]+1)))
        else:    
            keyword_dict[m]=abs_occurences_dict[m]/float((fdist[m.lower()]+1))
        
    sorted_one_word_tags = sorted(keyword_dict.items(), key=operator.itemgetter(1),reverse=True)
    return sorted_one_word_tags

print("opening text file...")

with open('text_sample_project_report.txt','r')as text:
    phrase_list=get_sorted_phrase_list(text)
    
    
with open('Wiki_titles.txt','rb')as titles:
    wikiTitles=pickle.load(titles)
    sorted_two_word_tags=two_words_key_extractor(phrase_list, wikiTitles)
    
with open('text_sample_project_report.txt','r')as text:
    single_words=subtitle_to_words(text)
    sorted_one_word_tags=single_word_key_extractor(single_words,wikiTitles)
    
lenth_phrase_list=len(phrase_list)
sorted_top_two_word_tags=islice(sorted_two_word_tags, 20)
sorted_top_one_word_tags=islice(sorted_one_word_tags,20)
word_tag=[]
for items in sorted_top_two_word_tags:
    word_tag.append(items)
    
for items in sorted_top_one_word_tags:
    word_tag.append(items)
    
word_tag.sort(key=operator.itemgetter(1),reverse=True)
for tags in word_tag:
    print(tags[0])

#===============================================================================
# final_tags=dict(sorted_top_one_word_tags.items()|sorted_top_two_word_tags.items())
# #===============================================================================
# # sorted_tags=sorted(final_tags.items(), key=operator.itemgetter(1),reverse=True)
# #===============================================================================
#  
# for i in range(0,int(len(final_tags))):
#     if len(final_tags[i][0])>2:
#         print(final_tags[i][0])
#===============================================================================
