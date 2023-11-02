import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_review_test_231102Nov43.csv')
df.dropna(inplace=True)     # 공백문자 제거
# df.info()
# print(df.head(10))  # 공백문자를 NaN값으로 읽어들인 것을 확인
print(len(df['location'].unique()))

one_sentences = []
for title in df['location'].unique():
    temp = df[df['location'] == title]     # 조건 인덱싱: []안에 조건식을 넣어도 된다
    one_sentence = ' '.join(temp['cleaned_sentences'])
    # print(one_sentence)
    # exit()
    one_sentences.append(one_sentence)  # location,country,address,cleaned_sentences

df_one = pd.DataFrame({'locations':df['location'].unique(), 'reviews':one_sentences})
print(df_one.head())
df_one.info()
df_one.to_csv('./crawling_data/cleaned_one_review_test_None_ETC.csv', index=False)
