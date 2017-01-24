# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:42:07 2017

@author: 邓旸旸
"""

import pandas as pd
from pandas import DataFrame
import os

os.chdir('../csv')
files = os.listdir('./')    #这里改变工作路径
dfs = DataFrame(columns=['shop_id'])
dfs.shop_id = [i for i in range(1,2001)]

for file_csv in files:
    df= pd.read_csv(file_csv)
    dfs = pd.merge(dfs,df,on='shop_id',how='outer')
    
dfs = dfs.fillna(0)
dfs.to_csv('all_user_pay.csv',index=False)