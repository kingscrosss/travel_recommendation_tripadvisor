import pandas as pd
import datetime

df = pd.read_csv('./result/cleaned_review_231103.csv')
df.dropna(inplace=True)     # 공백문자 제거
# df.info()
# print(df.head(10))  # 공백문자를 NaN값으로 읽어들인 것을 확인
# print(len(df['location'].unique()))

one_sentences = []
for location in df['location'].unique():
    temp = df[df['location'] == location]     # 조건 인덱싱: []안에 조건식을 넣어도 된다
    one_sentence = ' '.join(temp['cleaned_sentences'])
    # print(one_sentence)
    # exit()
    one_sentences.append(one_sentence)  # location,country,address,cleaned_sentences

print(len(one_sentences))
df.drop_duplicates(['location'],inplace=True)
print(len(df))
df.drop(['cleaned_sentences'], axis=1, inplace=True)
print(df.head(10))
df['reviews'] = one_sentences
df_one = df.rename(columns={'location':'locations'})
print(df_one.head())
df_one.info()
df_one.to_csv('./result/cleaned_one_review_2{}.csv'.format(datetime.datetime.now().strftime('%y%m%d')), index=False)
