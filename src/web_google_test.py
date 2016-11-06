# -*- coding: utf-8 -*-
import os
import gensim
from pyemd import emd
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cosine
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.cross_validation import train_test_split

if not os.path.exists("/home/avinash/PycharmProjects/data_local_model/embed.dat"):
    print("Caching word embeddings in memmapped format...")
    from gensim.models.word2vec import Word2Vec
    wv = Word2Vec.load(
        "/home/caniz/Devel/cognostics/difficulty_measure/Shared/word2vec_models/size600_min50_window5_bigram/size600_min50_window5_bigram")
    fp = np.memmap("/home/avinash/PycharmProjects/data_local_model/embed.dat", dtype=np.double, mode='w+', shape=wv.syn0.shape)
    fp[:] = wv.syn0[:]
    with open("/home/avinash/PycharmProjects/data_local_model/embed.vocab", "w") as f:
        for _, w in sorted((voc.index, word) for word, voc in wv.vocab.items()):
            print(w, file=f)
    del fp, wv

W = np.memmap("/home/avinash/PycharmProjects/data_local_model/embed.dat", dtype=np.double, mode="r", shape=(300000, 300))
with open("/home/avinash/PycharmProjects/data_local_model/embed.vocab") as f:
    vocab_list = map(str.strip, f.readlines())

vocab_dict = {w: k for k, w in enumerate(vocab_list)}

with open('/home/avinash/Downloads/text1.txt') as f:

    d1 = f.read().replace('\n', '')

with open('/home/avinash/Downloads/text2.txt') as f:

    d2 = f.read().replace('\n', '')
#d2 = "The President addresses the press in Chicago"

vect = CountVectorizer(stop_words="english").fit([d1, d2])
print("Features:",  ", ".join(vect.get_feature_names()))

v_1, v_2 = vect.transform([d1, d2])
v_1 = v_1.toarray().ravel()
v_2 = v_2.toarray().ravel()

print("cosine(doc_1, doc_2) = {:.2f}".format(cosine(v_1, v_2)))

common=[]
not_in_list=[]
for w in vect.get_feature_names():
    if w in vocab_dict.keys():
        common.append(w)
    else:
        not_in_list.append(w)


W_common = W[[vocab_dict[w] for w in common]]
D_=euclidean_distances(W_common)

#print("d(addresses, speaks) = {:.2f}".format(D_[0, 7]))
#print("d(addresses, chicago) = {:.2f}".format(D_[2, 1]))

# pyemd needs double precision input
v_1 = v_1.astype(np.double)
v_2 = v_2.astype(np.double)
v_1 /= v_1.sum()
v_2 /= v_2.sum()
D_ = D_.astype(np.double)
D_ /= D_.max()  # just for comparison purposes

print("d(doc_1, doc_2) = {:.2f}".format(emd(v_1, v_2,D_)))
