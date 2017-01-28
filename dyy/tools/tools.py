# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 19:28:32 2017

@author: 邓旸旸
"""
import numpy as np

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

    




