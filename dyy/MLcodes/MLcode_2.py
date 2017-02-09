# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 10:21:49 2017

@author: Administrator
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import sys
from sklearn.preprocessing import PolynomialFeatures
sys.path.append('../tools')
from tools import *


weekA = pd.read_csv('../train/weekABCD/weekA.csv'); weekA.index=weekA.shop_id
weekB = pd.read_csv('../train/weekABCD/weekB.csv'); weekB.index=weekB.shop_id
weekC = pd.read_csv('../train/weekABCD/weekC.csv'); weekC.index=weekC.shop_id
weekD = pd.read_csv('../train/weekABCD/weekD.csv'); weekD.index=weekD.shop_id

poly = PolynomialFeatures(3,interaction_only=True)
train_x = (pd.merge(weekB,weekC,on='shop_id')).drop('shop_id',axis=1)    #train = weekB + weekC
train_sum = train_x.sum(axis=1)
train_open_ratio = every_shop_open_ratio(start_day=468,end_day=481)
train_weekend = ['2016-10-15 00:00:00','2016-10-15 00:00:00','2016-10-22 00:00:00','2016-10-23 00:00:00']
train_ratio_wk = (train_x[train_weekend]).sum(axis=1)/(train_sum.replace(0,1))

train_x = transfrom_Arr_DF(poly.fit_transform(train_x))
train_x['sumABCD'] = train_sum
train_x['open_ratio'] = train_open_ratio.open_ratio
train_x['ratio_wk'] = train_ratio_wk

train_y = weekD.drop('shop_id',axis=1)


test_x = (pd.merge(weekC,weekD,on='shop_id')).drop('shop_id',axis=1)     #test = weekC + weekD 
test_sum = test_x.sum(axis=1)
test_open_ratio = every_shop_open_ratio(start_day=475)
test_weekend = ['2016-10-22 00:00:00','2016-10-23 00:00:00','2016-10-29 00:00:00','2016-10-30 00:00:00']
test_ratio_wk = (test_x[test_weekend]).sum(axis=1)/(test_sum.replace(0,1))

test_x = transfrom_Arr_DF(poly.fit_transform(test_x))
test_x['sumABCD'] = test_sum
test_x['open_ratio'] = test_open_ratio.open_ratio
test_x['ratio_wk'] = test_ratio_wk

RF = RandomForestRegressor(n_estimators=500,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=25)
RF.fit(train_x,train_y)
pre = (RF.predict(test_x)).round()

result = get_result(pre)
