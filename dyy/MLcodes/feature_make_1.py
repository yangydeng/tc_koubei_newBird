# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:18:06 2017

@author: Administrator
"""

import pandas as pd
import sys
from sklearn.preprocessing import PolynomialFeatures
sys.path.append('../tools')
from tools import *

day_time = '_02_11_2'

weekA = pd.read_csv('../csv/weekABCD/weekA.csv'); weekA.index=weekA.shop_id
weekB = pd.read_csv('../csv/weekABCD/weekB.csv'); weekB.index=weekB.shop_id
weekC = pd.read_csv('../csv/weekABCD/weekC.csv'); weekC.index=weekC.shop_id
weekD = pd.read_csv('../csv/weekABCD/weekD.csv'); weekD.index=weekD.shop_id
shop_info_num = pd.read_csv('../csv/shop_info_num.csv')

'''     degree 应当为 3     '''
poly = PolynomialFeatures(3,interaction_only=True)

train_x = (pd.merge(weekA,weekB,on='shop_id')).drop('shop_id',axis=1)       #train = weekA + weekB
train_sum = train_x.sum(axis=1)
train_mean = train_x.mean(axis=1)
train_weekend = ['2016-09-24 00:00:00','2016-09-25 00:00:00','2016-10-15 00:00:00','2016-10-16 00:00:00']
train_ratio_wk = (train_x[train_weekend]).sum(axis=1)/(train_sum.replace(0,1))
train_open_ratio_wkA = every_shop_open_ratio(start_day=447,end_day=453)
train_open_ratio_wkB = every_shop_open_ratio(start_day=468,end_day=474)
train_open_ratio = (train_open_ratio_wkA.open_ratio + train_open_ratio_wkB.open_ratio)/2

#   make城市的OHE码
names = []          
for name in (shop_info_num.city_name).values:
    if(name in [8,4,23,15,25,12,10]):                              #一系列数组表示排名城市对应的编号
        names.append(name)
    else:
        names.append(100)
OHE_city_name = transfrom_Arr_DF(make_OHE(names),'city_')

#  make 行业cate_1_name的OHE码
names = []          
for name in (shop_info_num.cate_1_name).values:
    if(name in [0,1]):                              #一系列数组表示cate_1_name对应的编号
        names.append(name)
    else:
        names.append(100)
OHE_cate_1 = transfrom_Arr_DF(make_OHE(names),'cate_1_')

# make 行业cate_2_name 的OHE码
names = []          
for name in (shop_info_num.cate_2_name).values:
    if(name in [4,1,9,0,5,2,3,6,10,7]):                              #一系列数组表示cate_2_name对应的编号
        names.append(name)
    else:
        names.append(100)
OHE_cate_2 = transfrom_Arr_DF(make_OHE(names),'cate_2_')

# make 行业cate_3_name 的OHE码
names = []          
for name in (shop_info_num.cate_3_name).values:
    if(name in [5,8,3,2,6,4,0,16,11]):                              #一系列数组表示cate_3_name对应的编号
        names.append(name)
    else:
        names.append(100)
OHE_cate_3 = transfrom_Arr_DF(make_OHE(names),'cate_3_')

#   make shop_info.score 的OHE码 
OHE_score = transfrom_Arr_DF(make_OHE(shop_info_num.score),'shop_info_score_')

#   make shop_info.shop_level 的OHE码
OHE_shop_level = transfrom_Arr_DF(make_OHE(shop_info_num.shop_level),'shop_info_level_')

train_x = transfrom_Arr_DF(poly.fit_transform(train_x)) #将其中的日期生成多项式
train_x['sumABCD'] = train_sum    #加入总数
train_x['meanABCD'] = train_mean     #加入平均数
train_x['ratio_wk'] = train_ratio_wk  #周末占总量的比例
train_x['open_ratio_ABCD'] = train_open_ratio.values    #加入开业比例
train_x = train_x.join(OHE_city_name,how='left')
train_x = train_x.join(OHE_cate_1,how='left')
train_x = train_x.join(OHE_cate_2,how='left')
train_x = train_x.join(OHE_cate_3,how='left')
#train_x['location_id'] = shop_info_num.location_id
#train_x = train_x.join(OHE_score,how='left')
train_x = train_x.join(OHE_shop_level,how='left')

train_y = weekC.drop('shop_id',axis=1)

train_x.to_csv('../train_1/train_x'+day_time+'.csv',index=False)
train_y.to_csv('../train_1/train_y'+day_time+'.csv',index=False)
#-----------------------------------------------------------------------------------------------------------------------------------------------------
test_x = (pd.merge(weekB,weekC,on='shop_id')).drop('shop_id',axis=1)    #test = weekC + weekD
test_sum = test_x.sum(axis=1)
test_mean = test_x.mean(axis=1)
test_weekend = ['2016-10-15 00:00:00','2016-10-16 00:00:00','2016-10-22 00:00:00','2016-10-23 00:00:00']
test_ratio_wk = (test_x[test_weekend]).sum(axis=1)/(test_sum.replace(0,1))
test_open_ratio = every_shop_open_ratio(start_day=468,end_day=481)

test_x = transfrom_Arr_DF(poly.fit_transform(test_x))
test_x['sumABCD'] = test_sum
test_x['meanABCD'] = test_mean
test_x['ratio_wk'] = test_ratio_wk
test_x['open_ratio_ABCD'] = test_open_ratio.open_ratio
test_x = test_x.join(OHE_city_name,how='left')
test_x = test_x.join(OHE_cate_1,how='left')
test_x = test_x.join(OHE_cate_2,how='left')
test_x = test_x.join(OHE_cate_3,how='left')
#test_x['location_id'] = shop_info_num.location_id
#test_x = test_x.join(OHE_score,how='left')
test_x = test_x.join(OHE_shop_level,how='left')

test_y = weekD.drop('shop_id',axis=1)

test_x.to_csv('../test_1/test_x'+day_time+'.csv',index=False)
test_y.to_csv('../test_1/test_y'+day_time+'.csv',index=False)