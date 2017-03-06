# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 15:03:58 2017

@author: Administrator
"""

day_time = '_02_22_3'

import pandas as pd
from pandas import DataFrame
from sklearn.neighbors import KNeighborsRegressor
import sys
sys.path.append('../tools')
from tools import calculate_score
from sklearn import preprocessing
from sklearn.ensemble import BaggingRegressor,AdaBoostRegressor

train_x = pd.read_csv('../train_knn_1/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_knn_1/train_y'+day_time+'.csv')
test_x = pd.read_csv('../test_knn_1/test_x'+day_time+'.csv')
test_y = pd.read_csv('../test_knn_1/test_y'+day_time+'.csv')

scaler = preprocessing.MinMaxScaler()

train_x = scaler.fit_transform(train_x)
test_x = scaler.transform(test_x)

KNN = KNeighborsRegressor(n_neighbors=5,weights='distance',algorithm='auto',p=1)

Bagging_KNN = BaggingRegressor(base_estimator=KNN,n_estimators=100,random_state=1,max_features=0.2)
#Boosting_KNN = AdaBoostRegressor(base_estimator=KNN,n_estimators=100,random_state=1)

pre = DataFrame()

for i in range(7):
    Bagging_KNN.fit(train_x,list(train_y.icol(i).values))
    pre['col_'+str(i)] = (Bagging_KNN.predict(test_x)).round()
    tmp_score = calculate_score(pre.icol(i).values,test_y.icol(i).values)
    print str(i)+': ',tmp_score



score = calculate_score(pre.values,test_y.values)
print score

