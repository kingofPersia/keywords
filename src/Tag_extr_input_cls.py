# -*- coding: utf-8 -*-
import os
import glob
import ntpath
from tag_extr_v_6 import get_list_of_tags
input_file_path='../Transcripts'
tags_dict={}
output_file_path='../Transcripts/final_tags_dict_2.txt'
for f in glob.glob(os.path.join(input_file_path, '*.txt')):
    
    tags=get_list_of_tags(f)
    tags_dict[ntpath.basename(f)]=tags

with open(output_file_path,'w')as file:
    file.write(str(tags_dict))
