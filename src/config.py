import nltk
from nltk.corpus import reuters,brown

reuters_word_list = reuters.words()
fdist_reuters = nltk.FreqDist(w.lower() for w in reuters_word_list)
brown_word_list = brown.words()
fdist_brown = nltk.FreqDist(w.lower() for w in brown_word_list)


