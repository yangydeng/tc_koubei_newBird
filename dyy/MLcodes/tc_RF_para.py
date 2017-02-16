# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:52:26 2017

@author: 邓旸旸
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

day_time = '_02_15_2'

#RF = RandomForestRegressor(n_estimators=100,criterion='mse',max_depth=None,\
#    min_samples_split=5,min_samples_leaf=1,min_weight_fraction_leaf=0.0,\
#    max_features='log2',max_leaf_nodes=None,bootstrap=True,oob_score=False,n_jobs=-1,\
#    random_state=1,verbose=0,warm_start=False)
    
RF = ExtraTreesRegressor()    
parameters = {'n_estimators':[1200],'n_jobs':[-1],'random_state':[1],'min_samples_split':[2],\
                'min_samples_leaf':[2],'max_depth':[25],'criterion':['mse'],'max_features':[270]}

train_x = pd.read_csv('../train_0/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_0/train_y'+day_time+'.csv')


train_x_val = train_x.values
train_y_val = train_y.values

kf = KFold(len(train_x.values),n_folds=5,shuffle=True,random_state=1)
loss = make_scorer(calculate_score,greater_is_better=False)

clf = GridSearchCV(RF,param_grid=parameters,cv=kf,scoring=loss)
clf.fit(train_x_val,train_y_val)

print clf.best_params_





