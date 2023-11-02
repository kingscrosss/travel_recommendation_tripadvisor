import pandas as pd
from gensim.models import Word2Vec

df_review = pd.read_csv('./crawling_data/cleaned_one_review_test_None_ETC.csv')
df_review.info()

reviews = df_review['reviews']
print(reviews[0])

tokens = []
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(tokens[0])

embedding_model = Word2Vec(tokens, vector_size=100,     # 차원의 저주를 막기 위해서 100차원으로 줄임
                           window=4, min_count=20,      # min_count: 출연 빈도가 20번 이하인건 안 반영할래
                           workers=10, epochs=100, sg=1)       # workers: 코어 몇개 쓸래?
# epochs가 있다? 딥러닝 모델이다
embedding_model.save('./models/word2vec_trip_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))




