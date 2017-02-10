# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 13:48:55 2017

@author: Administrator
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import sys
sys.path.append('../tools')
from tools import calculate_score

train_x = pd.read_csv('../train_1/train_x_02_10_2.csv')
train_y = pd.read_csv('../train_1/train_y_02_10_2.csv')
test_x = pd.read_csv('../test_1/test_x_02_10_2.csv')
test_y = pd.read_csv('../test_1/test_y_02_10_2.csv')

RF = RandomForestRegressor(n_estimators=500,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=25)
RF.fit(train_x,train_y)
pre = (RF.predict(test_x)).round()
score =calculate_score(pre,test_y.values)
print score