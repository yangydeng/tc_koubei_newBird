# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 20:14:51 2017

@author: Administrator
"""

import pandas as pd
from pandas import DataFrame
import sys
import numpy as np
sys.path.append('../tools')
from tools import transform_count_user_pay_datetime,
get_open_15
from datetime import datetime
from sklearn.ensemble import ExtraTreesRegressor

day_time = '_03_02_2'

count_user_pay = pd.read_csv('../csv/count_pay_and_view/count_user_pay.csv')
count_user_pay = transform_count_user_pay_datetime(count_user_pay)

open_15 = get_open_15()


count_user_pay.index = [i for i in range(1,2001)]

features_11_2015 = count_user_pay.ix[open_15,datetime(2015,10,13):datetime(2015,11,2)]
labels_11_2015 = count_user_pay.ix[open_15,datetime(2015,11,3):datetime(2015,11,16)]
features_11_2016 = count_user_pay.ix[:,datetime(2016,10,11):datetime(2016,10,31)]

#------------------------------------------------------------------------------------------------------------------
count_2015_11_03 = labels_11_2015[datetime(2015,11,3)]
count_2015_11_04 = labels_11_2015[datetime(2015,11,4)]
count_2015_11_10 = labels_11_2015[datetime(2015,11,10)]
count_2015_11_11 = labels_11_2015[datetime(2015,11,11)]
delta_10_03 = count_2015_11_10 - count_2015_11_03
delta_11_04 = count_2015_11_11 - count_2015_11_04

labels_11_2015[datetime(2015,11,10)] = labels_11_2015[datetime(2015,11,3)]        # 移动 11-11 产生的影响
labels_11_2015[datetime(2015,11,11)] = labels_11_2015[datetime(2015,11,4)]
labels_11_2015[datetime(2015,11,12)] = labels_11_2015[datetime(2015,11,12)] + delta_10_03
labels_11_2015[datetime(2015,11,13)] = labels_11_2015[datetime(2015,11,13)] + delta_11_04/2
#------------------------------------------------------------------------------------------------------------------

mean_11_2015 = features_11_2015.mean(axis=1)
max_11_2015 = features_11_2015.max(axis=1)
min_11_2015 = (features_11_2015.min(axis=1)).replace(0,170)
median_11_2015 = (features_11_2015.median(axis=1)).replace(0,170)
mean_11_2016 = features_11_2016.mean(axis=1)
max_11_2016 = features_11_2016.max(axis=1)
min_11_2016 = (features_11_2016.min(axis=1)).replace(0,170)
median_11_2016 = (features_11_2016.median(axis=1)).replace(0,170)

mean_11_2015 = np.array(mean_11_2015.values).reshape(328,1)
max_11_2015 = np.array(max_11_2015.values).reshape(328,1)
min_11_2015 = np.array(min_11_2015.values).reshape(328,1)
median_11_2015 = np.array(median_11_2015.values).reshape(328,1)
mean_11_2016 = np.array(mean_11_2016.values).reshape(2000,1)
max_11_2016 = np.array(max_11_2016.values).reshape(2000,1)
min_11_2016 = np.array(min_11_2016.values).reshape(2000,1)
median_11_2016 = np.array(median_11_2016.values).reshape(2000,1)

train_x_mean = np.array(features_11_2015.values)/mean_11_2015
train_x_max = np.array(features_11_2015.values)/max_11_2015
train_x_min = np.array(features_11_2015.values)/min_11_2015
train_x_median = np.array(features_11_2015.values)/median_11_2015
test_x_mean = np.array(features_11_2016.values)/mean_11_2016
test_x_max = np.array(features_11_2016.values)/max_11_2016
test_x_min = np.array(features_11_2016.values)/min_11_2016
test_x_median = np.array(features_11_2016.values)/median_11_2016

train_y = np.array(labels_11_2015.values)/mean_11_2015

train_x_mean = DataFrame(train_x_mean,columns=['train_mean_'+str(i) for i in range(len(train_x_mean[0]))])
train_x_max = DataFrame(train_x_max,columns=['train_max_'+str(i) for i in range(len(train_x_max[0]))])
train_x_min = DataFrame(train_x_min,columns=['train_min_'+str(i) for i in range(len(train_x_min[0]))])
train_x_median = DataFrame(train_x_median,columns=['train_median_'+str(i) for i in range(len(train_x_median[0]))])
test_x_mean = DataFrame(test_x_mean,columns=['test_mean_'+str(i) for i in range(len(test_x_mean[0]))])
test_x_max = DataFrame(test_x_max,columns=['test_max_'+str(i) for i in range(len(test_x_max[0]))])
test_x_min = DataFrame(test_x_min,columns=['test_min_'+str(i) for i in range(len(test_x_min[0]))])
test_x_median = DataFrame(test_x_median,columns=['test_median_'+str(i) for i in range(len(test_x_median[0]))])

train_x = train_x_mean.join(train_x_max,how='left')
train_x = train_x.join(train_x_min,how='left')
train_x = train_x.join(train_x_median,how='left')
test_x = test_x_mean.join(test_x_max,how='left')
test_x = test_x.join(test_x_min,how='left')
test_x = test_x.join(test_x_median,how='left')
test_x = test_x.fillna(1)

train_y = DataFrame(train_y)

#----------------------------------------------------------------------------------------
ET = ExtraTreesRegressor(n_estimators=2600,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=12,max_features='sqrt')
ET.fit(train_x,train_y)
pre = ET.predict(test_x)
pre = sqrt(pre)
pre = pre*mean_11_2016

pre = DataFrame(pre.round())
pre.insert(0,'shop_id',[i for i in range(1,2001)])
pre.to_csv('../results/result'+day_time+'_pre.csv',index=False,header=False)
