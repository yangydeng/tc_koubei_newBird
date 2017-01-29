# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 19:28:32 2017

@author: 邓旸旸
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import MySQLdb
import os
from pandas import DataFrame

def gb2312(col):
    col_return = []
    for row in col:
        col_return.append(row.encode('gb2312'))
    
    return col_return
    
    
    
'''本模块用于将cursor获取得到的整张表转变为list的形式，以便生成DataFrame'''
def transform_data(data):
    data = list(data)
    i = 0
    for row in data:
        data[i]=list(row)
        i=i+1
        
    return data

'''本模块用于将data 转变为np.array的形式，以便获取每一列。eg: data[:,1],data[:,2]...'''
def np_transform_data(data):
    data = np.array(data)
    i = 0
    for row in data:
        data[i]=np.array(row)
        i=i+1
        
    return data    
    

'''本模块用于计算得分，pre：预测的客流，real：实际的客流。两者都应当为DataFrame'''
def calculate_score(pre,real):
    if(len(pre)!=len(real)):
        print 'len(pre)!=len(real)','\n'
    if(len(pre.columns)!=len(real.columns)):
        print 'len(pre.columns)!=len(real.columns)','\n'
        
    N = len(pre)    #N：商家总数
    T = len(pre.columns)    
    print 'N:',N,'\t','T:',T,'\n'
    
    n = 0
    t = 0
    L=0
    
    while(t<T):
        n=0
        while(n<N):
            c_it=pre.ix[n,t]        #c_it：预测的客流量
            c_git = real.ix[n,t]    #c_git：实际的客流量
            
            
            if(c_it==0 and c_git==0):
                c_it=1
                c_git=1
            
            L = L+abs((float(c_it)-c_git)/(c_it+c_git))
            n=n+1
        t=t+1
    print L


'''本函数用于得到任意时间段内2000个商家的开张率（既有客流的商家占总体的比例）'''
def open_ratio(start_col=0,end_col=488):
    count_user_pay = pd.read_csv('../csv/count_user_pay.csv')
    Col = len(count_user_pay.columns)
    
    col = 1 #col 从1开始，因为第一列是shop_id
    Open_ratios = []
    
    while(col<Col):
        single_col = count_user_pay.ix[:,col]
        open_ratio = (single_col>0).sum()/2000.0
        Open_ratios.append(round(open_ratio,4))
        col = col+1
    
    dates = []
    for row in count_user_pay.columns[1:]:
        dates.append(row.replace('count_user_pay_',''))
    
    fig = plt.figure(1)
    ax = fig.add_subplot(1,1,1)
    if(end_col-start_col<100):    #当时间段小于100天时，会显示具体日期。    
        ax.set_xticks([i for i in range(len(dates[start_col:end_col]))])
        ax.set_xticklabels(dates[start_col:end_col],rotation=-90)
    ax.set_title('open ratio')
    ax.plot(Open_ratios[start_col:end_col])

'''链接数据库，注意有两个返回值'''
def conn_MySQL():
    db = MySQLdb.connect(host="localhost",user='root',passwd="Dyy2008723",db="tc_koubei",charset="utf8")
    cursor = db.cursor()
    return cursor,db

'''将某一路径中所有的csv合称为一个csv文件。'''
def csvMerge(csv_dir,save_name):
    os.chdir(csv_dir)
    files = os.listdir('./')    #这里改变工作路径
    dfs = DataFrame(columns=['shop_id'])
    dfs.shop_id = [i for i in range(1,2001)]
    
    for file_csv in files:
        df= pd.read_csv(file_csv)
        dfs = pd.merge(dfs,df,on='shop_id',how='outer')
        
    dfs = dfs.fillna(0)
    dfs.to_csv(save_name,index=False)
    
