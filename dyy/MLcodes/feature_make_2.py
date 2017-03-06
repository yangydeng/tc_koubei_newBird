# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 10:22:20 2017

@author: Administrator
"""

import pandas as pd
#from pandas import DataFrame
from datetime import datetime
#from sklearn.ensemble import ExtraTreesRegressor
import sys
sys.path.append('../tools')
from tools import transform_count_user_pay_datetime,every_shop_open_ratio,transfrom_Arr_DF,make_OHE,week_poly_2

day_time = '_02_21_1'

shop_info_num = pd.read_csv('../csv/shop_info_num.csv')
count_user_pay = pd.read_csv('../csv/count_pay_and_view/count_user_pay.csv')
# 15-07 开业的店铺
open_15_07 = every_shop_open_ratio(0.001,0,30)
# 15-11 期间开业的店铺
open_15_11 = every_shop_open_ratio(0.9,104,138)
                        
open_15_07 = open_15_07.shop_id.values
open_15_11 = open_15_11.shop_id.values
#取交集
open_15 = set(open_15_07) & set(open_15_11)
open_15 = list(open_15)
open_15.sort()

count_user_pay = transform_count_user_pay_datetime(count_user_pay)
count_user_pay.index = [i for i in range(1,2001)]   #注意：要把count_user_pay 的 index 设置为跟 shop_id 相同；这样后续根据shop_id的切片才会准确；
train_x = count_user_pay.ix[:,datetime(2015,10,13):datetime(2015,11,2)]
weekA = count_user_pay.ix[:,datetime(2015,10,13):datetime(2015,10,19)]
weekB = count_user_pay.ix[:,datetime(2015,10,20):datetime(2015,10,26)]
weekC = count_user_pay.ix[:,datetime(2015,10,27):datetime(2015,11,02)]

poly_trainA = week_poly_2(weekA,'poly_train_A_')
poly_trainB = week_poly_2(weekB,'poly_train_B_')
poly_trainC = week_poly_2(weekC,'poly_train_C_')

poly_trainA.index = poly_trainB.index = poly_trainC.index = [i for i in range(1,2001)]
train_x = train_x.join(poly_trainA,how='left')
train_x = train_x.join(poly_trainB,how='left')
train_x = train_x.join(poly_trainC,how='left')

train_std = train_x.std(axis=1)
train_max = train_x.max(axis=1)
 
 
 train_min = train_x.min(axis=1)
train_median = train_x.median(axis=1)
train_mad = train_x.mad(axis=1)
train_var = train_x.var(axis=1) 
train_sum = train_x.sum(axis=1)
train_mean = train_x.mean(axis=1)

#   make城市的OHE码
names = []          
for name in (shop_info_num.city_name).values:
    if(name in [8,4,23,15,25,12,10]):                              #一系列数组表示排名城市对应的编号
        names.append(name)
    else:
        names.append(100)
OHE_city_name = transfrom_Arr_DF(make_OHE(names),'city_')
OHE_city_name.index = [i for i in range(1,2001)]

#  make 行业cate_1_name的OHE码
names = []          
for name in (shop_info_num.cate_1_name).values:
    if(name in [0,1]):                              #一系列数组表示cate_1_name对应的编号
        names.append(name)
    else:
        names.append(100)
OHE_cate_1 = transfrom_Arr_DF(make_OHE(names),'cate_1_')
OHE_cate_1.index = [i for i in range(1,2001)]

# make 行业cate_2_name 的OHE码
names = []          
for name in (shop_info_num.cate_2_name).values:
    if(name in [4,1,9,0,5,2,3,6,10,7]):                              #一系列数组表示cate_2_name对应的编号
        names.append(name)
    else:
        names.append(100)
OHE_cate_2 = transfrom_Arr_DF(make_OHE(names),'cate_2_')
OHE_cate_2.index = [i for i in range(1,2001)]

# make 行业cate_3_name 的OHE码
names = []          
for name in (shop_info_num.cate_3_name).values:
    if(name in [5,8,3,2,6,4,0,16,11]):                              #一系列数组表示cate_3_name对应的编号
        names.append(name)
    else:
        names.append(100)
OHE_cate_3 = transfrom_Arr_DF(make_OHE(names),'cate_3_')
OHE_cate_3.index = [i for i in range(1,2001)]

#   make shop_info.score 的OHE码 
OHE_score = transfrom_Arr_DF(make_OHE(shop_info_num.score),'shop_info_score_')
OHE_score.index = [i for i in range(1,2001)]

#   make shop_info.shop_level 的OHE码
OHE_shop_level = transfrom_Arr_DF(make_OHE(shop_info_num.shop_level),'shop_info_level_')
OHE_shop_level.index = [i for i in range(1,2001)]

train_y = count_user_pay.ix[:,datetime(2015,11,3):datetime(2015,11,16)]

count_2015_11_03 = train_y[datetime(2015,11,3)]
count_2015_11_04 = train_y[datetime(2015,11,4)]
count_2015_11_10 = train_y[datetime(2015,11,10)]
count_2015_11_11 = train_y[datetime(2015,11,11)]
delta_10_03 = count_2015_11_10 - count_2015_11_03
delta_11_04 = count_2015_11_11 - count_2015_11_04

train_x['std'] = train_std
train_x['max'] = train_max
train_x['min'] = train_min
#train_x['median'] = train_median
train_x['mad'] = train_mad
train_x['var'] = train_var
train_x['sum'] = train_sum
train_x['mean'] = train_mean
train_x = train_x.join(OHE_city_name.ix[open_15],how='left')
train_x = train_x.join(OHE_cate_1,how='left')
train_x = train_x.join(OHE_cate_2,how='left')
train_x = train_x.join(OHE_cate_3,how='left')
#train_x['location_id'] = shop_info_num.location_id
#train_x = train_x.join(OHE_score,how='left')
train_x = train_x.join(OHE_shop_level,how='left')

train_y[datetime(2015,11,10)] = train_y[datetime(2015,11,3)]        # 移动 11-11 产生的影响
train_y[datetime(2015,11,11)] = train_y[datetime(2015,11,4)]
train_y[datetime(2015,11,12)] = train_y[datetime(2015,11,12)] + delta_10_03
train_y[datetime(2015,11,13)] = train_y[datetime(2015,11,13)] + delta_11_04/2
#----------------------------------------------------------------------------------------------------------------------

test_x = count_user_pay.ix[:,datetime(2016,10,11):datetime(2016,10,31)]
weekA = count_user_pay.ix[:,datetime(2016,10,11):datetime(2016,10,17)]
weekB = count_user_pay.ix[:,datetime(2016,10,18):datetime(2016,10,24)]
weekC = count_user_pay.ix[:,datetime(2016,10,25):datetime(2016,10,31)]

poly_testA = week_poly_2(weekA,'poly_test_A_')
poly_testB = week_poly_2(weekB,'poly_test_B_')
poly_testC = week_poly_2(weekC,'poly_test_C_')

poly_testA.index = poly_testB.index = poly_testC.index =[i for i in range(1,2001)]
test_x = test_x.join(poly_testA,how='left')
test_x = test_x.join(poly_testB,how='left')
test_x = test_x.join(poly_testC,how='left')

test_std = test_x.std(axis=1)
test_max = test_x.max(axis=1)
test_min = test_x.min(axis=1)
#test_median = test_x.median(axis=1)
test_mad = test_x.mad(axis=1)
test_var = test_x.var(axis=1) 
test_sum = test_x.sum(axis=1)
test_mean = test_x.mean(axis=1)

test_x['std'] = test_std
test_x['max'] = test_max
test_x['min'] = test_min
#test_x['median'] = train_median
test_x['mad'] = test_mad
test_x['var'] = test_var
test_x['sum'] = test_sum
test_x['mean'] = test_mean

test_x = test_x.join(OHE_city_name,how='left')
test_x = test_x.join(OHE_cate_1,how='left')
test_x = test_x.join(OHE_cate_2,how='left')
test_x = test_x.join(OHE_cate_3,how='left')
#train_x['location_id'] = shop_info_num.location_id
#train_x = train_x.join(OHE_score,how='left')
test_x = test_x.join(OHE_shop_level,how='left')

train_x.index = [i for i in range(1,2001)]
train_y.index = [i for i in range(1,2001)]
train_x = train_x.ix[open_15]
train_y = train_y.ix[open_15]


train_x.to_csv('../train_2/train_x'+day_time+'.csv',index=False)
train_y.to_csv('../train_2/train_y'+day_time+'.csv',index=False)
test_x.to_csv('../test_2/test_x'+day_time+'.csv',index=False)

