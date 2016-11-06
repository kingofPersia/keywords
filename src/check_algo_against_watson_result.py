# -*- coding: utf-8 -*-
from tag_extractor_v5_including_3word_phrase import get_list_of_tags

similarity=0
similarity_percentage=0
matched_tags_list=[]

def list_of_tags_from_online_tool(tag_dict_text):
    with open(tag_dict_text,'r') as inf:
        dict_from_file = eval(inf.read())
    list_of_tags=[]
    for k,v in dict_from_file.items():
        if k=="keywords":
            for item in v:
                list_of_tags.append(item['text'].lower())
    return(list_of_tags)
tags_from_online_tool=list_of_tags_from_online_tool('C:/Users/avinashchandra/workspace/PARMENIDES/text files/network_security_json.txt')
def calculate_similarity(tags_for_article_1,tags_for_article_2):
    
    length_article_1_tag_list=len(tags_for_article_1)
    length_online_tag_list=len(tags_from_online_tool)
    matching_counter=0
    print("length of our list",length_article_1_tag_list)
    if length_article_1_tag_list>=length_online_tag_list:
        print("article 1 has more tags than other article ")
        for tags in tags_for_article_2:
            if tags in tags_for_article_1:
                matching_counter+=1
                matched_tags_list.append(tags)
        similarity=matching_counter/length_online_tag_list
        similarity_percentage=round(similarity*100,3)
    else:
        print("article 2 has more tags than other article ")
        for tags in tags_for_article_1:
            if tags in tags_for_article_2:
                matching_counter+=1   
                matched_tags_list.append(tags) 
        similarity=matching_counter/length_article_1_tag_list
        similarity_percentage=round(similarity*100,3)
        
    return similarity_percentage,matched_tags_list


tags_for_article_1=get_list_of_tags("C:/Users/avinashchandra/workspace/PARMENIDES/text files/article_sample_network_security.txt")

similarity_percentage,matched_tags_list=calculate_similarity(tags_for_article_1,tags_from_online_tool)

print("the similarity percentage is", similarity_percentage)
print("the list of tags for article 1 is",tags_for_article_1)
print("the list of tags for article 2 is",tags_from_online_tool)
print("the matched tags are",matched_tags_list)
