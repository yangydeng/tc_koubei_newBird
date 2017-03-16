# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:14:14 2017

    通过2015年预测2016年    
    
@author: yangydeng
"""

import pandas as pd
from pandas import DataFrame
#from datetime import datetime
from sklearn.ensemble import ExtraTreesRegressor
import sys
sys.path.append('../tools')
from tools import draw_feature_importance


day_time = '_03_02_2'

train_x = pd.read_csv('../train_2/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_2/train_y'+day_time+'.csv')
test_x = pd.read_csv('../test_2/test_x'+day_time+'.csv')


ET = ExtraTreesRegressor(n_estimators=2600,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=12,max_features='sqrt')
ET.fit(train_x,train_y)
pre = (ET.predict(test_x)).round()

result = DataFrame(pre,columns=['col_'+str(i) for i in range(1,15)])
result.insert(0,'shop_id',[i for i in range(1,2001)])
result.to_csv('../results/result'+day_time+'.csv',index=False,header=False)

draw_feature_importance(train_x,ET)