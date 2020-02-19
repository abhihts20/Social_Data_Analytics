from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd

data = pd.read_csv("posts.csv", sep=";")

tfidf = TfidfVectorizer(min_df=.5, max_df=0.95, ngram_range=(0, 1))

features = tfidf.fit_transform(data)

pd.DataFrame(

    features.todense(),

    columns=tfidf.get_feature_names()

)

# from sklearn.feature_extraction.text import TfidfVectorizer
# import pandas as pd
# dataset=pd.read_csv("posts.csv",sep=";")
# v = TfidfVectorizer()
# x = v.fit_transform(dataset.iloc[:,1])
#
# df1 = pd.DataFrame(x.toarray(), columns=v.get_feature_names())
# print(df1)