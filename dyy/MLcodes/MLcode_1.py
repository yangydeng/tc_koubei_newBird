# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 13:48:55 2017

@author: Administrator
"""
day_time = '_02_27_2'

import pandas as pd
from pandas import DataFrame
#from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
import sys
sys.path.append('../tools')
from tools import calculate_score,draw_feature_importance

train_x = pd.read_csv('../train_1/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_1/train_y'+day_time+'.csv')
test_x = pd.read_csv('../test_1/test_x'+day_time+'.csv')
test_y = pd.read_csv('../test_1/test_y'+day_time+'.csv')

#RF = RandomForestRegressor(n_estimators=1200,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=25,max_features=30,bootstrap=1)
#RF.fit(train_x,train_y)
#pre = (RF.predict(test_x)).round()

ET = ExtraTreesRegressor(n_estimators=1200,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=20,max_features='sqrt',bootstrap=0)

#ET.fit(train_x,train_y)
#pre = (ET.predict(test_x)).round()

pre = DataFrame()
for i in range(7):
    ET.fit(train_x,list(train_y.icol(i).values))
    pre['col_'+str(i)] = (ET.predict(test_x)).round()
    tmp_score = calculate_score(pre.icol(i).values,test_y.icol(i).values)
    print str(i)+': ',tmp_score

score = calculate_score(pre.values,test_y.values)
print score

draw_feature_importance(train_x,ET)