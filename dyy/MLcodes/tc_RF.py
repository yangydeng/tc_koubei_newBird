# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:52:26 2017

@author: 邓旸旸
"""

import pandas as pd
from datetime import *
from sklearn.ensemble import RandomForestRegressor
import sys
sys.path.append('../tools')
from tools import *
from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer

#RF = RandomForestRegressor(n_estimators=100,criterion='mse',max_depth=None,\
#    min_samples_split=5,min_samples_leaf=1,min_weight_fraction_leaf=0.0,\
#    max_features='log2',max_leaf_nodes=None,bootstrap=True,oob_score=False,n_jobs=-1,\
#    random_state=1,verbose=0,warm_start=False)
    
RF = RandomForestRegressor()    
parameters = {'n_estimators':[640],'n_jobs':[-1],'random_state':[1],'min_samples_split':[2],'min_samples_leaf':[2],'max_depth':[25]}

train = pd.read_csv('../train/train_02_07_2.csv')
test = pd.read_csv('../test/test_02_07_2.csv')

train_x = train.drop('2016-10-30 00:00:00',axis=1)
train_y = train['2016-10-30 00:00:00']
test_x = test.drop('2016-10-31 00:00:00',axis=1)
test_y = test['2016-10-31 00:00:00']

train_x_val = train_x.values
train_y_val = train_y.values
test_x_val = test_x.values
test_y_val = test_y.values

kf = KFold(len(train_x.values),n_folds=10,shuffle=True,random_state=1)
loss = make_scorer(calculate_score,greater_is_better=False)

clf = GridSearchCV(RF,param_grid=parameters,cv=kf,scoring=loss)
clf.fit(train_x_val,train_y_val)





