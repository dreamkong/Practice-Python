import numpy as np
from math import sqrt
from collections import Counter


class KNNClassifier:

    def __init__(self, k):
        '''初始化kNN分类器'''
        assert k >= 1, 'k must be valid'
        self.k = k
        self._X_train = None
        self._y_train = None

    def fit(self, X_train, y_train):
        '''根据训练集X_train和y_train训练kNN分类器'''
        self._X_train = X_train
        self._y_train = y_train
        return self

    def predict(self, X_predict):
        y_predict = [self._predict(x) for x in X_predict]
        return y_predict

    def _predict(self, x):
        distances = [sqrt(np.sum((x_train - x) ** 2))
                     for x_train in self._X_train]
        nearest = np.argsort(distances)
        topK_y = [self._y_train[i] for i in nearest[:self.k]]
        votes = Counter(topK_y)
        return np.array(votes.most_common(1)[0][0])
