
from nltk.corpus import stopwords
from bs4 import BeautifulSoup 
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer



def subtitle_to_words( subtitles ):

    #  Remove HTML
    review_text = BeautifulSoup(subtitles).get_text() 
    
    #  Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    #  convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words )) 

print(subtitle_to_words(" ha i am going to PLACE . MACHINE LEARNING"))

def countOccurancy(raw_subtitle):
    clean_subtitle=[];
    clean_subtitle.append( subtitle_to_words( raw_subtitle ) )
    total_count=0
    vectorizer = CountVectorizer();
    train_data_features = vectorizer.fit_transform(clean_subtitle);
    train_data_features = train_data_features.toarray()
    vocab = vectorizer.get_feature_names()
    
    dist = np.sum(train_data_features, axis=0)
    for count in dist:
        total_count+=count;
    print("total count is: %d" % (total_count))
    for tag, count in zip(vocab, dist):
        print ((count), tag)
        
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(train_data_features)
    #===========================================================================
    # feature_name=X_train_tfidf.get_feature_names()
    #===========================================================================
    #print(X_train_tfidf)
    
def tfidfValue(raw_subtitle):
    tfidf_vectorizer = TfidfVectorizer(
    min_df=1,  # min count for relevant vocabulary
    max_features=4000,  # maximum number of features
    strip_accents='unicode',  # replace all accented unicode char
    # by their corresponding  ASCII char
    analyzer='word',  #`     features made of words
    token_pattern=r'\w{4,}',  # tokenize only words of 4+ chars
    ngram_range=(1, 1),  # features made of a single tokens
    use_idf=True,  # enable inverse-document-frequency reweighting
    smooth_idf=True,  # prevents zero division for unseen words
    sublinear_tf=False)

    desc_vect = tfidf_vectorizer.fit_transform([raw_subtitle]) 
    print(desc_vect.data)  
    d = dict(zip(tfidf_vectorizer.get_feature_names(), (desc_vect.data)))
    print(d)
    
def keywordExtractionUsingRake():
    return ("")
raw_subtitle="One of the advantages of being an American citizen living abroad is that you can register to vote using an absentee ballot and send it in by e-mail. On Tuesday I cast my vote in the U.S. general election for Democrats Hillary Clinton and Tim Kaine. This is not a statement of patriotic duty. In fact my nationality has never been a defining factor when it comes to my own sense of identity. Yet more than ever before I felt an obligation to take part in the U.S. election not because Im an American but because I believe that civic responsibilities extend beyond the borders of any one country.";
countOccurancy(raw_subtitle)
tfidfValue(raw_subtitle)