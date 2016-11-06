# -*- coding: utf-8 -*-
# this version include brown adn reuters corpus both 
from __future__ import print_function
from nltk.stem import WordNetLemmatizer
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
fdist_brown = config.fdist_brown
fdist_reuters = config.fdist_reuters


def get_sorted_phrase_list(text):
    print("getting key words and phrases....")
    # tokenizing text
    # using ngram_range to generate 2 word phrase
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
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
    wnl = WordNetLemmatizer()
    #  Remove HTML
    review_text = BeautifulSoup(subtitles, "lxml").get_text() 
    
    #  Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    
    #  convert the stop words to a set
    stops = set(stopwords.words("english"))

    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops and len(w)>2]  
    # change plural form of a word to singular form.
    new_words=[]                  
    for w in meaningful_words:
        new_words.append(wnl.lemmatize(w)) 
    return( new_words)

def two_words_key_extractor(words,wikiTitles):
    print("extracting two words tag")
    keyword_dict_two_words={}
    abs_occurences_dict={}
    for m in words:
        
        if m not in abs_occurences_dict.keys():
            abs_occurences_dict[m]=1
        else:
            abs_occurences_dict[m]+=1

        # if two words phrase is not present in reuter's list but have wikipedia title.          
        if  fdist_brown [m.lower()]==0 and m+'\n'  in wikiTitles and len(m.split())in [2,3]:
            
            if len(m.split())==2:
                first_word=m.split()[0]
                second_word=m.split()[1]
                first_word_freq_score=(fdist_brown[first_word.lower()]+fdist_reuters[first_word.lower()])/2
                second_word_freq_score=(fdist_brown[second_word.lower()]+fdist_reuters[second_word.lower()])/2
                # score for keyword m
                keyword_dict_two_words[m]=abs_occurences_dict[m]*1.5/(abs((first_word_freq_score-second_word_freq_score)/(first_word_freq_score+second_word_freq_score+1))+1)
            else:
                #===============================================================
                # first_word=m.split()[0]
                # second_word=m.split()[1]
                # #===============================================================
                # # third_word=m.split()[2]
                # #===============================================================
                # first_word_freq_score=fdist[first_word.lower()]
                # second_word_freq_score=fdist[second_word.lower()]
                # #===============================================================
                # # third_word_freq_score=fdist[third_word.lower()]
                # #===============================================================
                # # score for keyword m
                #===============================================================
                print("three words",m)
                keyword_dict_two_words[m]=abs_occurences_dict[m]/(1)   
    # sorting based on score            
    #===========================================================================
    # sorted_two_word_tags = sorted(keyword_dict_two_words.items(), key=operator.itemgetter(1),reverse=True)
    #===========================================================================
    print(keyword_dict_two_words)
    return keyword_dict_two_words 
             
def single_word_key_extractor(words):
    print("extracting single word tag")
    
    keyword_dict_single_word={}
    abs_occurences_dict={}
    for m in words:
        if m not in abs_occurences_dict.keys():
            abs_occurences_dict[m]=1
        else:
            abs_occurences_dict[m]+=1
        keyword_dict_single_word[m]=abs_occurences_dict[m]/float((fdist_brown[m.lower()]+fdist_reuters[m.lower()])/2+1)
    #sorting based on score     
    #===========================================================================
    # sorted_one_word_tags = sorted(keyword_dict_single_word.items(), key=operator.itemgetter(1),reverse=True)
    #===========================================================================
    print(keyword_dict_single_word)
    return keyword_dict_single_word

def combine_two_tag_dict(sorted_two_word_tags_dict,sorted_one_word_tags_dict,tag_to_text_ratio):
    print("Combining two tag list")
    
    # combining single word tags dict and two words tag dict 
    final_dict=dict(sorted_two_word_tags_dict.items() | sorted_one_word_tags_dict.items())
    print("tag_to_text_ratio",tag_to_text_ratio)
    sorted_tags_dict=sorted(final_dict.items(), key=operator.itemgetter(1),reverse=True)
    print("sorted_tags_dict",sorted_tags_dict)
    tags_dict=islice(sorted_tags_dict, tag_to_text_ratio)
    
    
 
    #===========================================================================
    # sorted_top_one_word_tags=islice(sorted_one_word_tags,tag_to_text_ratio)
    #===========================================================================
    word_tag=[]
    final_tags_list=[]
    for items in tags_dict:
        word_tag.append(items)
        
    #===========================================================================
    # for items in sorted_top_one_word_tags:
    #     word_tag.append(items)
    #===========================================================================
        
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
        sorted_one_word_tags_dict=single_word_key_extractor(single_words)
        length_one_word_tag_list=len(sorted_one_word_tags_dict)
        
    # opening text file containing wikipedia titles   
     
    with open('../Wiki_titles/Wiki_titles.txt','rb')as titles:
    
        wikiTitles=pickle.load(titles)
        sorted_two_word_tags_dict=two_words_key_extractor(phrase_list, wikiTitles)
        length_two_word_tag_list=len(sorted_two_word_tags_dict)
        tag_to_text_ratio=int((length_one_word_tag_list+length_two_word_tag_list)*0.10)
        
    return  combine_two_tag_dict(sorted_two_word_tags_dict,sorted_one_word_tags_dict,tag_to_text_ratio)  
    


