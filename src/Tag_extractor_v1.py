# -*- coding: utf-8 -*-

from __future__ import print_function
import pickle
import operator
from _io import open
import config


from sklearn.feature_extraction.text import TfidfVectorizer

fdist = config.fdist

def key_extractor_using_reutersWord_feq(words,wikiTitles):
    print("running algorithm to find key words.....")
    keyword_dict={}
    abs_occurences_dict={}
    rare_wiki_word_count=0
    not_wiki_count=0
    wiki_word_count_2=0
    
    for m in words:
        
        if m not in abs_occurences_dict.keys():
            abs_occurences_dict[m]=1
        else:
            abs_occurences_dict[m]+=1

                 
        if  fdist [m.lower()]==0:
            
            if m+'\n' in wikiTitles:
    
                if (len(m.split())==2):
                    
                    firstWord=m.split()[0]
                    secondWord=m.split()[1]
                    firstWordFreqScore=fdist[firstWord.lower()]
                    secondWordFreqScore=fdist[secondWord.lower()]
                    keyword_dict[m]=abs_occurences_dict[m]/(firstWordFreqScore+secondWordFreqScore+1)
                else:
                    rare_wiki_word_count+=1
                    keyword_dict[m]=abs_occurences_dict[m]/rare_wiki_word_count
                    
                
            else:
                not_wiki_count+=lenth_phrase_list
                keyword_dict[m]=abs_occurences_dict[m]/(not_wiki_count)
                
        else:   
            keyword_dict[m]=abs_occurences_dict[m]/float((fdist[m.lower()]))
    sorted_dict = sorted(keyword_dict.items(), key=operator.itemgetter(1),reverse=True)
    print("printing SORTED dict")
    for i in range(0,int(len(sorted_dict))):
        if len(sorted_dict[i][0])>2:
            print('{0:10}     {1}'.format(sorted_dict[i][0],round((sorted_dict[i][1]),5)))  
             

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



print("opening text file...")
text=open('Sample_text.txt','r')    

phrase_list=get_sorted_phrase_list(text)

lenth_phrase_list=len(phrase_list)
with open('Wiki_titles.txt','rb')as titles:
    wikiTitles=pickle.load(titles)
    key_extractor_using_reutersWord_feq(phrase_list, wikiTitles)
