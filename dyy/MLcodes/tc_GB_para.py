# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:52:06 2017

@author: Administrator
"""

import pandas as pd
from datetime import *
from sklearn.ensemble import GradientBoostingRegressor
import sys
sys.path.append('../tools')
from tools import *
from sklearn.cross_validation import KFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer

day_time = '_02_15_2'
    
GB = GradientBoostingRegressor()    
parameters = {'n_estimators':[200,100],'learning_rate':[0.05,0.1],'random_state':[1],'min_samples_split':[4],\
                'min_samples_leaf':[1],'max_depth':[4],'max_features':[270],'subsample':[1]}

train_x = pd.read_csv('../train_0/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_0/train_y'+day_time+'.csv')

kf = KFold(len(train_x_val),n_folds=5,shuffle=True,random_state=1)
loss = make_scorer(calculate_score,greater_is_better=False)

i = 6

train_x_val = train_x.values
train_y_val = (train_y.icol(i)).values
clf = GridSearchCV(GB,param_grid=parameters,cv=kf,scoring=loss)
clf.fit(train_x_val,train_y_val)

print clf.best_params_

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