from tag_extractor_v5_including_3word_phrase import get_list_of_tags

tags_for_article_1=get_list_of_tags("C:/Users/avinashchandra/workspace/PARMENIDES/text files/Soft_robots_ mimic_human.txt")
print("completed for article 1")

tags_for_article_2=get_list_of_tags("C:/Users/avinashchandra/workspace/PARMENIDES/text files/autonomous_soft_robot.txt")
print("completed for article 2")

similarity=0
similarity_percentage=0
matched_tags_list=[]

def calculate_similarity(tags_for_article_1,tags_for_article_2):
    
    length_article_1_tag_list=len(tags_for_article_1)
    length_article_2_tag_list=len(tags_for_article_2)
    matching_counter=0
    
    if length_article_1_tag_list>=length_article_2_tag_list:
        print("article 1 has more tags than other article ")
        for tags in tags_for_article_2:
            if tags in tags_for_article_1:
                matching_counter+=1
                matched_tags_list.append(tags)
        similarity=matching_counter/length_article_2_tag_list
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

similarity_percentage,matched_tags_list=calculate_similarity(tags_for_article_1,tags_for_article_2)

print("the similarity percentage is", similarity_percentage)
print("the list of tags for article 1 is",tags_for_article_1)
print("the list of tags for article 2 is",tags_for_article_2)
print("the matched tags are",matched_tags_list)