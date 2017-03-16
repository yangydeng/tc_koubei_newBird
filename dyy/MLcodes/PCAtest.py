# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 12:22:35 2017

    降维
    
@author: Administrator
"""

from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import  PCA
import pandas as pd
from sklearn.feature_selection import  SelectKBest  #选出K个最好特征
from scipy.stats import pearsonr    #皮尔森系数，用于检验线性相关性
from sklearn.feature_selection import chi2  #卡方检验
from sklearn.feature_selection import SelectFromModel   #Embedded 选择特征，可以基于决策树的 feature_importance 选择特征
from sklearn.feature_selection import RFE   #Wrapper 选择特征，递归特征消除法

import numpy as np
from sklearn.feature_selection import RFE
from sklearn.ensemble import ExtraTreesRegressor

train_x = pd.read_csv('../train_1/train_x_03_07_2.csv')
train_y = pd.read_csv('../train_1/train_y_03_07_2.csv')

#pca=PCA(n_components=100)
#new_train_x = pca.fit_transform(train_x.values)

#tmp = VarianceThreshold(threshold=3).fit_transform(train_x)
#
#a = SelectKBest(chi2, k=100).fit_transform(train_x.values, train_y.icol(0).values)

ET = ExtraTreesRegressor(n_estimators=1200,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=20,max_features='sqrt',bootstrap=0)
tmp = SelectFromModel(estimator=ET,threshold='median').fit_transform(train_x.values, train_y.icol(0).values)

