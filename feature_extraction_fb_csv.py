from textblob import TextBlob
import pandas as pd
import numpy as np

train = pd.read_csv('posts.csv', sep=";")

# Word Count
train['word_count'] = train['message'].apply(lambda x: len(str(x).split(" ")))
print(train[['message', 'word_count']].head())
print("--"*100)

# Char Count
train['char_count'] = train['message'].str.len()  ## this also includes spaces
print(train[['message', 'char_count']].head())
print("--"*100)


def avg_word(sentence):
    words = sentence.split()
    return sum(len(word) for word in words) / len(words)


train['avg_word'] = train['message'].astype(str).apply(lambda x: avg_word(x))
print(train[['message', 'avg_word']].head())
print("--"*100)


from nltk.corpus import stopwords
# import nltk
# nltk.download('stopwords')
stop = stopwords.words('english')
train['stopwords'] = train['message'].astype(str).apply(lambda x: len([x for x in x.split() if x in stop]))
print(train[['message', 'stopwords']].head())
print("--"*100)

train['hastags'] = train['message'].astype(str).apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
print(train[['message','hastags']].head())
print("--"*100)


train['numerics'] = train['message'].astype(str).apply(lambda x: len([x for x in x.split() if x.isdigit()]))
print(train[['message','numerics']].head())
print("--"*100)

train['message'] = train['message'].astype(str).apply(lambda x: " ".join(x.lower() for x in x.split()))
print(train['message'].head())
print("--"*100)

train['message'] = train['message'].str.replace('[^\w\s]','')
print(train['message'].head())
print("--"*100)

from nltk.corpus import stopwords
stop = stopwords.words('english')
train['message'] = train['message'].astype(str).apply(lambda x: " ".join(x for x in x.split() if x not in stop))
print(train['message'].head())
print("--"*100)


freq = pd.Series(' '.join(train['message']).split()).value_counts()[:10]
freq = list(freq.index)
train['message'] = train['message'].astype(str).apply(lambda x: " ".join(x for x in x.split() if x not in freq))
print(train['message'].head())
print("--"*100)

freq = pd.Series(' '.join(train['message']).split()).value_counts()[-10:]
freq = list(freq.index)
train['message'] = train['message'].astype(str).apply(lambda x: " ".join(x for x in x.split() if x not in freq))
print(train['message'].head())
print("--"*100)


print(train['message'][:5].astype(str).apply(lambda x: str(TextBlob(x).correct())))
print("--"*100)


print("Toeknization")
print(TextBlob(train['message'][1]).words)
print("--"*100)

print("Stemming")
from nltk.stem import PorterStemmer
st = PorterStemmer()
print(train['message'][:5].astype(str).apply(lambda x: " ".join([st.stem(word) for word in x.split()])))
print("--"*100)

print("Lemmatization")
from textblob import Word
train['message'] = train['message'].astype(str).apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
print(train['message'].head())
print("--"*100)

# -----------------------Advance Preprocessing---------------------------
print("N-grams")
print(TextBlob(train['message'][0]).ngrams(2))
print("--"*100)

print("Term frequency")
tf1 = (train['message'][1:2]).astype(str).apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()
tf1.columns = ['words','tf']
print(tf1)
print("--"*100)

for i,word in enumerate(tf1['words']):
  tf1.loc[i, 'idf'] = np.log(train.shape[0]/(len(train[train['message'].str.contains(word)])))
print(tf1)
print("--"*100)

tf1['tfidf'] = tf1['tf'] * tf1['idf']

print(tf1)
print("--"*100)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=1000, lowercase=True, analyzer='word',
 stop_words= 'english',ngram_range=(1,1))
train_vect = tfidf.fit_transform(train['message'])
print(train_vect)
print("--"*100)

print("Bag of words")
from sklearn.feature_extraction.text import CountVectorizer
bow = CountVectorizer(max_features=1000, lowercase=True, ngram_range=(1,1),analyzer = "word")
train_bow = bow.fit_transform(train['message'])
print(train_bow)



