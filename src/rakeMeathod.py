# -*- coding: utf-8 -*-
import nltk
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()

# change this to read in your data
finder = BigramCollocationFinder.from_words(
   nltk.corpus.genesis.words('text.txt'))

# only bigrams that appear 3+ times
finder.apply_freq_filter(2) 

# return the 5 n-grams with the highest PMI
print (finder.nbest(bigram_measures.pmi, 5))