import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread        # mmwrite: 메트릭스를 저장하는 패키지
import pickle

df_reviews = pd.read_csv('./crawling_data/cleaned_one_review_test_None_ETC.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])       # reviews 안에 몇 개의 형태소를 가졌는지
print(Tfidf_matrix.shape)   # (1935, 44667) 리뷰가 1935개가 있고 그것에 유니크한 단어가 44667개를 가진다.

with open('./models/tfidf.pickle','wb') as f:
    pickle.dump(Tfidf,f)
mmwrite('./models/Tfidf_trip_review.mtx', Tfidf_matrix)

# len(df['title'].unique()) = 1935