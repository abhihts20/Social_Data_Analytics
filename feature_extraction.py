texts = [
    "blue car and blue window",
    "black crow in the window",
    "i see my reflection in the window"
]
vocab = sorted(set(word for sentence in texts for word in sentence.split()))
print(len(vocab), vocab)

import numpy as np
def binary_transform(text):
    # create a vector with all entries as 0
    output = np.zeros(len(vocab))
    # tokenize the input
    words = set(text.split())
    # for every word in vocab check if the doc contains it
    for i, v in enumerate(vocab):
        output[i] = v in words
    return output

print(binary_transform("i saw crow"))

from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer(binary=True)
vec.fit(texts)
print([w for w in sorted(vec.vocabulary_.keys())])

import pandas as pd
print(pd.DataFrame(vec.transform(texts).toarray(), columns=sorted(vec.vocabulary_.keys())))
print("-"*100)
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer(binary=False) # we cound ignore binary=False argument since it is default
vec.fit(texts)

import pandas as pd
print(pd.DataFrame(vec.transform(texts).toarray(), columns=sorted(vec.vocabulary_.keys())))
print("-"*100)
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer()
vec.fit(texts)
import pandas as pd
print(pd.DataFrame(vec.transform(texts).toarray(), columns=sorted(vec.vocabulary_.keys())))