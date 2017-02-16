# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:34:37 2017

@author: Administrator
"""

day_time = '_02_15_2'

import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
import sys
sys.path.append('../tools')
from tools import calculate_score,draw_feature_importance,get_result

train_x = pd.read_csv('../train_0/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_0/train_y'+day_time+'.csv')
test_x = pd.read_csv('../test_0/test_x'+day_time+'.csv')
#test_y = pd.read_csv('../test_1/test_y'+day_time+'.csv')


#para0 = n_estimators=120,learning_rate=0.05,random_state=1,min_samples_split=2,min_samples_leaf=1,max_depth=4,max_features=140,subsample=1

#param1 = {'n_estimators':[120],'learning_rate':[0.01],'random_state':[1],'min_samples_split':[4],'min_samples_leaf':[3],'max_depth':[4],'max_features':[140],'subsample':[1]}

param = {'subsample':[1,1,1,1,1,1,1],'min_samples_leaf':[1,1,1,1,1,1,1],'n_estimators':[200,100,200,200,200,200,100],'min_samples_split':[4,8,2,8,2,4,4],\
        'learning_rate':[0.05,0.1,0.05,0.05,0.05,0.05,0.1],'max_features':[270,'auto',280,'auto',270,280,270],'random_state':[1,1,1,1,1,1,1]\
        ,'max_depth':[4,6,4,4,4,4,4]}


result = DataFrame()

for i in range(0,7):
    GB = GradientBoostingRegressor(n_estimators=param['n_estimators'][i],learning_rate=0.05,random_state=1,\
                                min_samples_split=param['min_samples_split'][i],min_samples_leaf=1,max_depth=param['max_depth'][i],max_features=param['max_features'][i],subsample=0.85)     
   
    GB.fit(train_x,train_y.icol(i))
    pre = (GB.predict(test_x)).round()
    
    result['col'+str(i)] = pre

result = get_result(result.values)
result.to_csv('../results/result'+day_time+'.csv',index=False,header=False)
    

#draw_feature_importance(train_x,ET)

#0: {'subsample': 1, 'learning_rate': 0.05, 'min_samples_leaf': 1, \
#'n_estimators': 200, 'min_samples_split': 4, 'random_state': 1, 'max_features': 270, 'max_depth': 4}

#1: {'subsample': 1, 'learning_rate': 0.1, 'min_samples_leaf': 3,\
# 'n_estimators': 100, 'min_samples_split': 8, 'random_state': 1, 'max_features': auto, 'max_depth': 6}

#2: {'subsample': 1, 'learning_rate': 0.05, 'min_samples_leaf': 1,\
# 'n_estimators': 200, 'min_samples_split': 2, 'random_state': 1, 'max_features': 280, 'max_depth': 4}

#3: {'subsample': 1, 'learning_rate': 0.05, 'min_samples_leaf': 1,\
# 'n_estimators': 200, 'min_samples_split': 8, 'random_state': 1, 'max_features': auto, 'max_depth': 4}

#4: {'subsample': 1, 'learning_rate': 0.05, 'min_samples_leaf': 1,\
# 'n_estimators': 200, 'min_samples_split': 2, 'random_state': 1, 'max_features': 270, 'max_depth': 4}

#5: {'subsample': 1, 'learning_rate': 0.05, 'min_samples_leaf': 1,\
# 'n_estimators': 200, 'min_samples_split': 4, 'random_state': 1, 'max_features': 280, 'max_depth': 4}

#6: {'subsample': 1, 'learning_rate': 0.10, 'min_samples_leaf': 1,\
# 'n_estimators': 100, 'min_samples_split': 4, 'random_state': 1, 'max_features': 270, 'max_depth': 4}