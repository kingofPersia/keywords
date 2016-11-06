# -*- coding: utf-8 -*-
import gensim
import os, glob
import smart_open
import multiprocessing
import logging
import time
import pickle


cores = multiprocessing.cpu_count()
start_time = time.time()

def read_corpus(fname, tokens_only=False):
    with smart_open.smart_open(fname, encoding='iso-8859-1') as f:
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

path='../Wiki'
model = gensim.models.doc2vec.Doc2Vec(alpha=0.025, min_alpha=0.025,workers=cores)

print("making pickle file")
for file in (f for f in glob.glob(os.path.join(path, '*.txt'))):
    
    with open('../Wiki/train_file.pkl', 'ab') as pickle_file:
        pickle.dump(list(read_corpus(file)), pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
        
print("making vocab")
model.build_vocab(pickle.load(open('../Wiki/train_file.pkl','rb')))
    
print("training model") 
for file in (f for f in glob.glob(os.path.join(path, '*.txt'))):
    for epoch in range(10):
        model.train(list(read_corpus(file)))
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
        level=logging.INFO)
        
print("saving model")        
model_name = "model_wiki_dm_1"
model.save(model_name)    
print("--- %s minutes ---" % round((time.time() - start_time)/60,3)) 


#===============================================================================
