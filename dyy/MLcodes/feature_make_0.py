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

day_time = '_03_01_3'

open_ABCD_ID = every_shop_open_ratio(0.85,447)
open_ABCD_ID = open_ABCD_ID.shop_id.values

weekA = pd.read_csv('../csv/weekABCD/weekA.csv'); weekA.index=weekA.shop_id
weekB = pd.read_csv('../csv/weekABCD/weekB.csv'); weekB.index=weekB.shop_id
weekC = pd.read_csv('../csv/weekABCD/weekC.csv'); weekC.index=weekC.shop_id
weekD = pd.read_csv('../csv/weekABCD/weekD.csv'); weekD.index=weekD.shop_id
add_July_Aug = pd.read_csv('../csv/add_July_Aug.csv')
analysis_all_week = pd.read_csv('../csv/analysis_all_week.csv')
point_feature = pd.read_csv('../csv/point_feature.csv')  #天气


weekA_view = pd.read_csv('../csv/weekABCD/weekA_view.csv'); weekA_view.index = weekA_view.shop_id
weekB_view = pd.read_csv('../csv/weekABCD/weekB_view.csv'); weekB_view.index = weekB_view.shop_id
weekC_view = pd.read_csv('../csv/weekABCD/weekC_view.csv'); weekC_view.index = weekC_view.shop_id
weekD_view = pd.read_csv('../csv/weekABCD/weekD_view.csv'); weekD_view.index = weekD_view.shop_id
shop_info_num = pd.read_csv('../csv/shop_info_num.csv')

'''  poly   degree=2     '''
poly = PolynomialFeatures(1,interaction_only=True,include_bias=False)
train_x = pd.merge(weekA,weekB,on='shop_id')                                       #train = weekA+ weekB + weekC
train_x = (pd.merge(train_x,weekC,on='shop_id')).drop('shop_id',axis=1)
train_x_view = pd.merge(weekA_view,weekB_view,on='shop_id')
train_x_view = (pd.merge(train_x_view,weekC_view,on='shop_id')).drop('shop_id',axis=1)

train_sum = train_x.sum(axis=1)
train_mean = train_x.mean(axis=1)
train_open_ratio_A = every_shop_open_ratio(start_day=447,end_day=453)
train_open_ratio_BC = every_shop_open_ratio(start_day=468,end_day=481)
train_open_ratio = (train_open_ratio_A.open_ratio + train_open_ratio_BC.open_ratio*2)/3
train_weekend = ['2016-09-24 00:00:00','2016-09-25 00:00:00','2016-10-15 00:00:00','2016-10-16 00:00:00','2016-10-22 00:00:00','2016-10-23 00:00:00']
train_ratio_wk = (train_x[train_weekend]).sum(axis=1)/(train_sum.replace(0,1))
train_std = train_x.std(axis=1)
train_max = train_x.max(axis=1)
train_min = train_x.min(axis=1)
train_median = train_x.median(axis=1)
train_mad = train_x.mad(axis=1)
train_var = train_x.var(axis=1) 

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

#train_x = transfrom_Arr_DF(poly.fit_transform(train_x))
train_x['sumABCD'] = train_sum
train_x['open_ratio'] = train_open_ratio
train_x['ratio_wk'] = train_ratio_wk
train_x['meanABCD'] = train_mean
train_x = train_x.join(OHE_city_name,how='left')
train_x = train_x.join(OHE_cate_1,how='left')
train_x = train_x.join(OHE_cate_2,how='left')
train_x = train_x.join(OHE_cate_3,how='left')
#train_x['location_id'] = shop_info_num.location_id
#train_x = train_x.join(OHE_score,how='left')
train_x = train_x.join(OHE_shop_level,how='left')
train_x = train_x.join(train_x_view)
train_x['std'] = train_std
train_x['max'] = train_max
train_x['min'] = train_min
train_x['median'] = train_median
train_x['mad'] = train_mad
train_x['var'] = train_var

#train_x = train_x.join(week_poly_2(weekA,'poly2A'),how='left')
#train_x = train_x.join(week_poly_2(weekB,'poly2B'),how='left')
#train_x = train_x.join(week_poly_2(weekC,'poly2C'),how='left')
train_x = train_x.join(add_July_Aug,how='left')
train_x = train_x.join(analysis_all_week,how='left')
train_x = train_x.join(point_feature.ix[:,'2016-10-25':'2016-10-31'],how='left')

train_y = weekD.drop('shop_id',axis=1)

#筛选 shop_id
train_x.index= [i for i in range(1,2001)]
test_x.index= [i for i in range(1,2001)]
train_x = train_x.ix[open_ABCD_ID]
train_y = train_y.ix[open_ABCD_ID]

train_x.to_csv('../train_0/train_x'+day_time+'.csv',index=False)
train_y.to_csv('../train_0/train_y'+day_time+'.csv',index=False)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
test_x = pd.merge(weekB,weekC,on='shop_id')                                         #test = weekB + weekC + weekD 
test_x = (pd.merge(test_x,weekD,on='shop_id')).drop('shop_id',axis=1)
test_x_view = pd.merge(weekB_view,weekC_view,on='shop_id')
test_x_view = (pd.merge(test_x_view,weekD_view)).drop('shop_id',axis=1)

test_sum = test_x.sum(axis=1)
test_mean = test_x.mean(axis=1)
test_open_ratio = every_shop_open_ratio(start_day=468)
test_weekend = ['2016-10-15 00:00:00','2016-10-16 00:00:00','2016-10-22 00:00:00','2016-10-23 00:00:00','2016-10-29 00:00:00','2016-10-30 00:00:00']
test_ratio_wk = (test_x[test_weekend]).sum(axis=1)/(test_sum.replace(0,1))
test_std = test_x.std(axis=1)
test_max = test_x.max(axis=1)
test_min = test_x.min(axis=1)
test_median = test_x.median(axis=1)
test_mad = test_x.mad(axis=1)
test_var = test_x.var(axis=1)

#test_x = transfrom_Arr_DF(poly.fit_transform(test_x))
test_x['sumABCD'] = test_sum
test_x['open_ratio'] = test_open_ratio.open_ratio
test_x['ratio_wk'] = test_ratio_wk
test_x['meanABCD'] = test_mean
test_x = test_x.join(OHE_city_name,how='left')
test_x = test_x.join(OHE_cate_1,how='left')
test_x = test_x.join(OHE_cate_2,how='left')
test_x = test_x.join(OHE_cate_3,how='left')
#test_x['location_id'] = shop_info_num.day_time = '_02_26_2_p1'location_id
#test_x = test_x.join(OHE_score,how='left')
test_x = test_x.join(OHE_shop_level,how='left')
test_x = test_x.join(test_x_view)
test_x['std'] = test_std
test_x['max'] = test_max
test_x['min'] = test_min
test_x['median'] = test_median
test_x['mad'] = test_mad
test_x['var'] = test_var

#test_x = test_x.join(week_poly_2(weekB,'poly2B'),how='left')
#test_x = test_x.join(week_poly_2(weekC,'poly2C'),how='left')
#test_x = test_x.join(week_poly_2(weekD,'poly2D'),how='left')
test_x = test_x.join(add_July_Aug,how='left')
test_x = test_x.join(analysis_all_week,how='left')
test_x = test_x.join(point_feature.ix[:,'2016-11-08':'2016-11-14'])

test_x.to_csv('../test_0/test_x'+day_time+'.csv',index=False)



