# 단어들을 시각화 해서 보기 편하게 만드는 과정
# 나중에 추천 결과 값을 비교하기 위해서 존재
import collections
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font',family='NanumBarunGothic')

df = pd.read_csv('./crawling_data/cleaned_one_review_test_None_ETC.csv')
# words = df.iloc[0, :]
words = df.iloc[0, 1].split()
print(words)

worddict = collections.Counter(words)       # pandas의 value_counts랑 같은 것. 유니크한 값들의 횟수를 알려줌
print(worddict)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path).generate_from_frequencies(worddict)

plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear') # imshow: img show
plt.axis('off')
plt.show()