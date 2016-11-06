# -*- coding: utf-8 -*-
import gensim
import os
import random
import pickle
from doc2vec_v_1 import read_corpus


test_data_dir = '{}'.format(os.sep).join([gensim.__path__[0], 'test', 'test_data'])
lee_test_file = test_data_dir + os.sep + 'lee.cor'
test_corpus = list(read_corpus(lee_test_file, tokens_only=True))


model=gensim.models.doc2vec.Doc2Vec.load("model_wiki_dm_1")
# Pick a random document from the test corpus and infer a vector from the model
doc_id = random.randint(0, len(test_corpus))
inferred_vector = model.infer_vector(test_corpus[doc_id])
sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

# Compare and print the most/median/least similar documents from the train corpus
print('Test Document ({}): {}\n'.format(doc_id, ' '.join(test_corpus[doc_id])))
print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
for label, index in [('MOST', 0), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
    print(u'%s %s: %s\n' % (label, sims[index], ' '.join(pickle.load(open('../Wiki/train_file.pkl','rb'))[sims[index][0]].words)))


