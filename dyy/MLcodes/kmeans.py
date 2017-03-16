# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 19:15:19 2017

    采用kmeans的方法将商家分类，结果发现有一部分商家是在周末销量下降的。

@author: Administrator
"""

from sklearn.cluster import KMeans
import pandas as pd
import sys
sys.path.append('../tools')
from tools import transform_count_user_pay_datetime
from pandas import DataFrame
from datetime import *

count_user_pay = pd.read_csv('../csv/count_pay_and_view/count_user_pay.csv')
count_user_pay = transform_count_user_pay_datetime(count_user_pay)
weekA = count_user_pay.ix[:,datetime(2016,9,20):datetime(2016,9,26)]
weekBCD = count_user_pay.ix[:,datetime(2016,10,11):datetime(2016,10,31)]


weeks = weekA.join(weekBCD,how='left')
'''按照涨跌划分'''
df = DataFrame(dtype='int64')

for i in range(len(weeks.ix[0])-1):
    vs = weeks.icol(i)<weeks.icol(i+1)
    df['col_'+str(i)] = vs
kmeans = KMeans(n_clusters=4,random_state=1).fit(df)
labels = kmeans.labels_

#'''按照客流量划分'''
#kmeans = KMeans(n_clusters=4,random_state=1).fit(weeks)
#labels = kmeans.labels_