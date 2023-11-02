import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import  mmread
import pickle
from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType('./trip_recomendation.ui')[0]
class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Tfidf_matrix = mmread('./models/Tfidf_trip_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_trip_review.model')

        self.df_reviews = pd.read_csv('./crawling_data/cleaned_one_review_test_None_ETC.csv')
        self.locations = list(self.df_reviews['locations'])
        self.locations.sort()
        for location in self.locations:
            self.comboBox.addItem(location)

        model = QStringListModel()      # 자동 완성 기능을 위해
        model.setStringList(self.locations)
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)

        self.comboBox.currentIndexChanged.connect(self.combox_slot)
        self.btn_recommendation.clicked.connect(self.btn_slot)

    def btn_slot(self):
        keyword = self.le_keyword.text()
        self.le_keyword.setText('')
        if keyword:
            if keyword in self.locations:
                # 영화 제목을 정확하게 똑같이 써야만 작동되는 문제 발생 -> 자동완성 기능 추가
                recommendation = self.recommendation_by_trip_locations(keyword)
                self.lbl_recommendation.setText(recommendation)
            else:
                recommendation = self.recommendation_by_keyword(keyword)
                print(recommendation)
                self.lbl_recommendation.setText(recommendation)

    def recommendation_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
            words = [keyword]
            for word, _ in sim_word:
                words.append(word)

            sentence = []
            count = len(words)
            for word in words:
                sentence = sentence + [word] * count
                count -= 1
            sentence = ' '.join(sentence)

            sentence_vec = self.Tfidf.transform([sentence])
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
            recommendation = self.getRecommendation(cosine_sim)
            return recommendation

        except:
           return '추천 장소가 없습니다.'

    def combox_slot(self):
        location = self.comboBox.currentText()     # 현재 콤보 박스에 있는 텍스트(영화제목)
        recommendation = self.recommendation_by_trip_locations(location)
        self.lbl_recommendation.setText(recommendation)

    def recommendation_by_trip_locations(self,location):
        trip_idx = self.df_reviews[self.df_reviews['locations']==location].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[trip_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)

        return recommendation

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]    # 10번까지 슬라이싱
        moviIdx = [i[0] for i in simScore]      # 추천 영화 0위부터 10위까지 11개 인덱스 저장
        recTriplist = self.df_reviews.iloc[moviIdx, 0]
        recTriplist = '\n'.join(recTriplist[1:])      # 문자열로 return하기 위해서, 0번은 자기자신이니까 제외하고 프린트
        # print(recTriplist)
        return recTriplist

if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())