# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import pickle

def wiki_name_parser(text):
    review_text = BeautifulSoup(text, "lxml").get_text() 
    
    #  Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split() 
    
    return words
new_file=[]
with open('Wiki_raw_titles.txt', 'r',encoding='utf8')as f:
    lines=f.readlines()
    
for line in lines:    
    # remove non alphanumeric characters
    letters_only = re.sub("[^a-zA-Z0-9]", " ", line)
    letters_only=re.sub("  ", " ", line)
    new_line = letters_only.lower() 
    print(new_line)
    new_file.append(new_line)
   
with open('Clean_raw_wiki_titles.txt','w',encoding='utf8') as w:
    # go to start of file
    w.seek(0)
    # actually write the lines
    w.writelines(new_file)

with open('Clean_raw_wiki_titles.txt', 'r',encoding='utf8')as f:
    text=f.readlines()
    print("reading complete, converting it to sets......")
    listToSet=set(text)
    
# pickle raw wikititles for fast access
with open('Wiki_titles.txt','wb')as output:
    print("serialization.....")
    pickle.dump(listToSet, output)
    print("serialization complete....")