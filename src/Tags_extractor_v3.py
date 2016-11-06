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
# word fequency count from reuters list
fdist = config.fdist

def get_sorted_phrase_list(text):
    print("getting key words and phrases....")
    # tokenizing text
    # using ngram_range to generate 2 word phrase
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,2), min_df = 0, stop_words = 'english')
    # training tf-idf model
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

def text_to_words( subtitles ):
    print("cleaning text....")
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
    print("extracting two words tag")
    keyword_dict={}
    abs_occurences_dict={}
    for m in words:
        
        if m not in abs_occurences_dict.keys():
            abs_occurences_dict[m]=1
        else:
            abs_occurences_dict[m]+=1

        # if two words phrase is not present in reuter's list but have wikipedia title.          
        if  fdist [m.lower()]==0 and m+'\n'  in wikiTitles and len(m.split())==2:
            
                first_word=m.split()[0]
                second_word=m.split()[1]
                first_word_freq_score=fdist[first_word.lower()]
                second_word_freq_score=fdist[second_word.lower()]
                # score for keyword m
                keyword_dict[m]=abs_occurences_dict[m]/(first_word_freq_score+second_word_freq_score+1)
                
    # sorting based on score            
    sorted_two_word_tags = sorted(keyword_dict.items(), key=operator.itemgetter(1),reverse=True)
    return sorted_two_word_tags 
             
def single_word_key_extractor(words):
    print("extracting single word tag")
    
    keyword_dict={}
    abs_occurences_dict={}
    for m in words:
        if m not in abs_occurences_dict.keys():
            abs_occurences_dict[m]=1
        else:
            abs_occurences_dict[m]+=1
        keyword_dict[m]=abs_occurences_dict[m]/float((fdist[m.lower()]+1))
    #sorting based on score     
    sorted_one_word_tags = sorted(keyword_dict.items(), key=operator.itemgetter(1),reverse=True)
    return sorted_one_word_tags

def combine_two_tag_dict(sorted_two_word_tags,sorted_one_word_tags):
    print("Combining two tag list")
    
    # combining single word tags dict and two words tag dict 
    
    sorted_top_two_word_tags=islice(sorted_two_word_tags, 20)
    sorted_top_one_word_tags=islice(sorted_one_word_tags,20)
    word_tag=[]
    final_tags_list=[]
    for items in sorted_top_two_word_tags:
        word_tag.append(items)
        
    for items in sorted_top_one_word_tags:
        word_tag.append(items)
        
    # sorting    
    
    word_tag.sort(key=operator.itemgetter(1),reverse=True)
    for tags in word_tag:
        final_tags_list.append(tags[0])
    return final_tags_list


def get_list_of_tags(text_file):
    
    print("opening text file...")
    with open(text_file,'r')as text:
        phrase_list=get_sorted_phrase_list(text)
        
    with open(text_file,'r')as text:
        single_words=text_to_words(text)
        sorted_one_word_tags=single_word_key_extractor(single_words)
        
    # opening text file containing wikipedia titles   
     
    with open('Wiki_titles.txt','rb')as titles:
    
        wikiTitles=pickle.load(titles)
        sorted_two_word_tags=two_words_key_extractor(phrase_list, wikiTitles)
        
    return  combine_two_tag_dict(sorted_two_word_tags,sorted_one_word_tags)  
    


