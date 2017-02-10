# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 12:40:05 2017

@author: Administrator
"""

import pandas as pd
import sys
from sklearn.preprocessing import PolynomialFeatures
sys.path.append('../tools')
from tools import *


weekA = pd.read_csv('../csv/weekABCD/weekA.csv'); weekA.index=weekA.shop_id
weekB = pd.read_csv('../csv/weekABCD/weekB.csv'); weekB.index=weekB.shop_id
weekC = pd.read_csv('../csv/weekABCD/weekC.csv'); weekC.index=weekC.shop_id
weekD = pd.read_csv('../csv/weekABCD/weekD.csv'); weekD.index=weekD.shop_id

poly = PolynomialFeatures(3,interaction_only=True)
train_x = pd.merge(weekA,weekB,on='shop_id')                                       #train = weekA+ weekB + weekC
train_x = (pd.merge(train_x,weekC,on='shop_id')).drop('shop_id',axis=1)
train_sum = train_x.sum(axis=1)
train_mean = train_x.mean(axis=1)
train_open_ratio_A = every_shop_open_ratio(start_day=447,end_day=453)
train_open_ratio_BC = every_shop_open_ratio(start_day=468,end_day=481)
train_open_ratio = (train_open_ratio_A.open_ratio + train_open_ratio_BC.open_ratio*2)/3
train_weekend = ['2016-09-24 00:00:00','2016-09-25 00:00:00','2016-10-15 00:00:00','2016-10-16 00:00:00','2016-10-22 00:00:00','2016-10-23 00:00:00']
train_ratio_wk = (train_x[train_weekend]).sum(axis=1)/(train_sum.replace(0,1))

train_x = transfrom_Arr_DF(poly.fit_transform(train_x))
train_x['sumABCD'] = train_sum
train_x['open_ratio'] = train_open_ratio
train_x['ratio_wk'] = train_ratio_wk
train_x['mean'] = train_mean

train_y = weekD.drop('shop_id',axis=1)

train_x.to_csv('../train_2/train_x_02_10_2.csv',index=False)
train_y.to_csv('../train_2/train_y_02_10_2.csv',index=False)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
test_x = pd.merge(weekB,weekC,on='shop_id')                                         #test = weekB + weekC + weekD 
test_x = (pd.merge(test_x,weekD,on='shop_id')).drop('shop_id',axis=1)
test_sum = test_x.sum(axis=1)
test_mean = test_x.mean(axis=1)
test_open_ratio = every_shop_open_ratio(start_day=468)
test_weekend = ['2016-10-15 00:00:00','2016-10-16 00:00:00','2016-10-22 00:00:00','2016-10-23 00:00:00','2016-10-29 00:00:00','2016-10-30 00:00:00']
test_ratio_wk = (test_x[test_weekend]).sum(axis=1)/(test_sum.replace(0,1))

test_x = transfrom_Arr_DF(poly.fit_transform(test_x))
test_x['sumABCD'] = test_sum
test_x['open_ratio'] = test_open_ratio.open_ratio
test_x['ratio_wk'] = test_ratio_wk
test_x['meanABCD'] = test_mean

test_x.to_csv('../test_2/test_x_02_10_2.csv',index=False)



