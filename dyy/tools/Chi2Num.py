# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 15:27:40 2017

@author: Administrator
"""

import os 
import pandas as pd
shop_info = pd.read_csv('../train/shop_info.csv')
files = os.listdir('../train/shop_info_Chinese2Num')
os.chdir('../train/shop_info_Chinese2Num')


for file_name in files:
    df = pd.read_csv(file_name)
    index = df.index
    
    for i in index:
        Chinese = df.ix[i,'col_0']
        shop_info = shop_info.replace(Chinese,i)
        
shop_info.to_csv('shop_info_num.csv',index=False)