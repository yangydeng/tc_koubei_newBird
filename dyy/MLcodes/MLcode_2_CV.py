# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:22:54 2017
    
    交叉验证 + GridSearch调参，calculate_score 按照主办方给出的方式计算得分。    
    
@author: yangydeng
"""

import pandas as pd
from datetime import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
import sys
sys.path.append('../tools')
from tools import *
from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer

day_time = '_02_20_3'

#RF = RandomForestRegressor(n_estimators=100,criterion='mse',max_depth=None,\
#    min_samples_split=5,min_samples_leaf=1,min_weight_fraction_leaf=0.0,\
#    max_features='log2',max_leaf_nodes=None,bootstrap=True,oob_score=False,n_jobs=-1,\
#    random_state=1,verbose=0,warm_start=False)
    
RF = ExtraTreesRegressor()    
parameters = {'n_estimators':[2600],'n_jobs':[-1],'random_state':[1],'min_samples_split':[2],\
                'min_samples_leaf':[1],'max_depth':[12],'criterion':['mse'],'max_features':['auto'],'bootstrap':[0]}

train_x = pd.read_csv('../train_2/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_2/train_y'+day_time+'.csv')


train_x_val = train_x.values
train_y_val = train_y.values

kf = KFold(len(train_x.values),n_folds=5,shuffle=True,random_state=1)
loss = make_scorer(calculate_score,greater_is_better=False)

clf = GridSearchCV(RF,param_grid=parameters,cv=kf,scoring=loss)
clf.fit(train_x_val,train_y_val)

print clf.best_params_