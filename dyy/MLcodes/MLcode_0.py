# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 10:21:49 2017

@author: Administrator
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
import sys
sys.path.append('../tools')
from tools import get_result

day_time = '_02_16_3'

train_x = pd.read_csv('../train_0/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_0/train_y'+day_time+'.csv')
test_x = pd.read_csv('../test_0/test_x'+day_time+'.csv')


#RF = RandomForestRegressor(n_estimators=1200,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=25)
#RF.fit(train_x,train_y)
#pre = (RF.predict(test_x)).round()

ET = ExtraTreesRegressor(n_estimators=1200,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=25,max_features=270)
ET.fit(train_x,train_y)
pre = (ET.predict(test_x)).round()


result = get_result(pre)

result.to_csv('../results/result'+day_time+'.csv',index=False,header=False)
