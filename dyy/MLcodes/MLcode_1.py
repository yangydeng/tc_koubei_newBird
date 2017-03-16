# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 13:48:55 2017

    产生离线结果，并计算离线得分

@author: yangydeng
"""
day_time = '_03_07_2'

import pandas as pd
from pandas import DataFrame
#from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import VarianceThreshold #方差选择法
from sklearn.feature_selection import SelectKBest   
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import RFE
import sys
sys.path.append('../tools')
from tools import calculate_score,draw_feature_importance

#from sklearn.decomposition import  PCA
#pca=PCA(n_components=200,svd_solver='full')

train_x = pd.read_csv('../train_1/train_x'+day_time+'.csv')
train_y = pd.read_csv('../train_1/train_y'+day_time+'.csv')
test_x = pd.read_csv('../test_1/test_x'+day_time+'.csv')
test_y = pd.read_csv('../test_1/test_y'+day_time+'.csv')

#VT = VarianceThreshold(threshold=10).fit(train_x)
#train_x = VT.transform(train_x)
#test_x = VT.transform(test_x)

#SK = SelectKBest(chi2,k=200).fit(train_x,train_y.icol(0).values)
#train_x = SK.transform(train_x)
#test_x = SK.transform(test_x)

ET = ExtraTreesRegressor(n_estimators=1200,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=20,max_features='sqrt',bootstrap=0)

#rfe = RFE(estimator=ET,n_features_to_select=180,step=5).fit(train_x.values, train_y.icol(0).values)
#train_x = rfe.transform(train_x.values)
#test_x = rfe.transform(test_x.values)

#sfm = SelectFromModel(estimator=ET,threshold='median').fit(train_x.values, train_y.icol(1).values)
#train_x = sfm.transform(train_x.values)
#test_x = sfm.transform(test_x.values)


#ET.fit(train_x,train_y)
#pre = (ET.predict(test_x)).round()

pre = DataFrame()
for i in range(7):
    ET.fit(train_x,list(train_y.icol(i).values))
    pre['col_'+str(i)] = (ET.predict(test_x)).round()
    tmp_score = calculate_score(pre.icol(i).values,test_y.icol(i).values)
    print str(i)+': ',tmp_score

score = calculate_score(pre.values,test_y.values)
print score

#draw_feature_importance(train_x,ET)