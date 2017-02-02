# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:52:26 2017

@author: 邓旸旸
"""

import pandas as pd
from pandas import DataFrame
from datetime import *
from sklearn.ensemble import RandomForestRegressor
import sys
sys.path.append('../tools')
from tools import *

RF = RandomForestRegressor(n_estimators=100,criterion='mse',max_depth=None,\
    min_samples_split=5,min_samples_leaf=1,min_weight_fraction_leaf=0.0,\
    max_features='log2',max_leaf_nodes=None,bootstrap=True,oob_score=False,n_jobs=-1,\
    random_state=1,verbose=0,warm_start=False)
    
count_user_pay = pd.read_csv('../csv/count_user_pay.csv')
count_user_pay = transform_count_user_pay_datetime(count_user_pay)
train_x = count_user_pay.ix[:,datetime(2016,10,8):datetime(2016,10,14)]
train_y = count_user_pay.ix[:,datetime(2016,10,15)]

test_x = count_user_pay.ix[:,datetime(2016,10,9):datetime(2016,10,15)]

RF.fit(train_x,train_y)
pre = (RF.predict(test_x)).round()
real = (count_user_pay.ix[:,datetime(2016,10,16)]).values

pre = DataFrame(pre,columns=['count'])
real = DataFrame(real,columns=['count'])

calculate_score(pre,real)
