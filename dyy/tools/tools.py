# -*- coding: utf-8 -*-
# encoding = utf-8
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
import random
from datetime import datetime,timedelta
from sklearn import preprocessing  


'''自动关机函数（包含取消关机功能）'''
def shutdown(minutes=0,reboot=False):
    if(minutes=='-a'):
        os.system('shutdown -a')
    elif(reboot):
        sec = minutes*60
        os.system('shutdown -r -t '+str(int(sec)))
    else:
        sec = minutes*60
        os.system('shutdown -s -t '+str(int(sec)))
    
'''解决dataframe保存为csv的时候，中文乱码问题'''
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

'''本模块用于将从MySQL获取的data 转变为np.array的形式，以便获取每一列。eg: data[:,1],data[:,2]...'''
def np_transform_data(data):
    data = np.array(data)
    i = 0
    for row in data:
        data[i]=np.array(row)
        i=i+1
    return data    
    

'''本模块用于计算得分，pre：预测的客流，real：实际的客流。两者都应当为array'''
def calculate_score(pre,real):
    if(len(pre.shape)==1):
        pre = DataFrame(pre,columns=[0])
        real = DataFrame(real,columns=[0])
    else:
        pre = DataFrame(pre,columns=[i for i in range(pre.shape[1])])
        real = DataFrame(real,columns=[i for i in range(real.shape[1])])        
        
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
            c_it = round(pre.ix[n,t])       #c_it：预测的客流量
            c_git = round(real.ix[n,t])    #c_git：实际的客流量
            
            
            if(c_it==0 and c_git==0):
                c_it=1
                c_git=1
            
            L = L+abs((float(c_it)-c_git)/(c_it+c_git))
            n=n+1
        t=t+1
    #print L
    return L/(N*T)


'''链接数据库，注意有两个返回值'''
def conn_MySQL():
    db = MySQLdb.connect(host="localhost",user='root',passwd="Dyy2008723",db="tc_koubei",charset="utf8")
    cursor = db.cursor()
    return cursor,db
    
'''gbk的字符形式链接MySQL，因为utf8的连接方式不能查询中文字符'''
def conn_MySQL_gbk():
    db = MySQLdb.connect(host="localhost",user='root',passwd="Dyy2008723",db="tc_koubei",charset="gbk")
    cursor = db.cursor()
    return cursor,db

'''输入sql语句，结果会以dataframe的形式返回，只能查询shop_info'''
def fetch_shop_info(sql):
    print sql
    cursor,db = conn_MySQL_gbk()
    cursor.execute(sql)
    data = cursor.fetchall()
    data = transform_data(data)
    db.close()
    df = DataFrame(data,columns=['shop_id','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name'])
    return df

''''''
def fetch_MySQL(sql):
    print sql 
    cursor,db = conn_MySQL_gbk()
    cursor.execute(sql)
    data = cursor.fetchall()
    data = np_transform_data(data)
    db.close()
    if(len(data.shape)==1):
        df = DataFrame(data,columns=[0])
    else:
        df = DataFrame(data,columns=['col_'+str(i) for i in range(data.shape[1])])
    return df

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


'''本函数用于得到任意时间段内2000个商家的开张率（既有客流的商家占总体的比例），纵向比例。'''
def open_ratio(start_col=0,end_col=488):
    count_user_pay = pd.read_csv('../csv/count_pay_and_view/count_user_pay.csv')
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
    
    fig = plt.figure(random.randint(1,10000))
    ax = fig.add_subplot(1,1,1)
    if(end_col-start_col<100):    #当时间段小于100天时，会显示具体日期。    
        ax.set_xticks([i for i in range(len(dates[start_col:end_col]))])
        ax.set_xticklabels(dates[start_col:end_col],rotation=-90)
    ax.set_title('open ratio')
    ax.grid()
    plt.subplots_adjust(bottom=0.2) #设置底部的位置，防止横坐标被遮挡
    ax.plot(Open_ratios[start_col:end_col])

'''本函数得到每个商家在任意时间段内“有客流的天数” 占 “总天数的比例”，横向比例。'''
def every_shop_open_ratio(threshold=0,start_day=0,end_day=488,smaller=False):
    #如果smaller=True 则取开张率小于threshold的商家。
    count_user_pay = pd.read_csv('../csv/count_pay_and_view/count_user_pay.csv')
    Row = len(count_user_pay)
    row = 0
    Open_ratios = []
    while(row<Row):
        single_row = count_user_pay.ix[row]
        single_row = single_row[start_day:end_day]
        open_ratio_ = (single_row>0).sum()/float(end_day-start_day+1)
        Open_ratios.append(round(open_ratio_,4))
        row = row+1
    Open_ratios = np.array(Open_ratios)
    if(smaller):
        mask = Open_ratios<=threshold
    else:
        mask = Open_ratios>=threshold
    df = DataFrame({'shop_id':(count_user_pay.shop_id)[mask].values,'open_ratio':Open_ratios[mask]})
    return  df   #返回大于threshold的shop_id,以及他们对应的开张比例


'''本函数用于将count_user_pay中，列名称全部转变为datetime格式，并且返回。'''
def transform_count_user_pay_datetime(count_user_pay):
    col = count_user_pay.columns
    tmp = []
    tmp1 = []
    for one in col:
        tmp.append(one.replace('count_user_pay_',''))
    for one in tmp:
        tmp1.append(one.replace('_','-'))
    col = []
    col.append(tmp1[0])
    for one in tmp1[1:]:
        col.append(datetime.strptime(one,'%Y-%m-%d'))
    count_user_pay.columns = col
    return count_user_pay

'''单个商家客流量的走势图，可调整时间段，也可以按指定的周几绘图'''
def draw_single_shop(shop_id,num_start_day=0,num_end_day=488,week=False,fr='D'):
        
    start_day = '2015-07-01'
    start_day = datetime.strptime(start_day,'%Y-%m-%d')+timedelta(days=num_start_day)
    end_day = start_day+timedelta(days=num_end_day-num_start_day)
    dates = pd.date_range(start=start_day,end=end_day,freq=fr)
    
    try:
        dates = dates.drop(datetime(2015,12,12))
    except ValueError:
        print ''        
    
    delta = (end_day-start_day).days
    count_user_pay = pd.read_csv('../csv/count_pay_and_view/count_user_pay.csv')
    count_user_pay.index = count_user_pay.shop_id.values
    count_user_pay = transform_count_user_pay_datetime(count_user_pay)
    values = count_user_pay.ix[shop_id,dates]  
    fig = plt.figure(random.randint(1,10000))
    ax = fig.add_subplot(111)
    
    xticklabels_date=values.index
    xticklabels_week = []
    for one in xticklabels_date:
        xticklabels_week.append(one.strftime('%a'))
    if(week):
        xticklabels = xticklabels_week
    else:
        xticklabels = xticklabels_date
    if(delta<100):
        ax.set_xticks([i for i in range(len(values))])  
        ax.set_xticklabels(xticklabels,rotation=-90)
    ax.set_title('shop_id:'+str(shop_id)+'   '+start_day.strftime('%Y-%m-%d')+' ~ '+end_day.strftime('%Y-%m-%d'))
    ax.grid()
    plt.subplots_adjust(bottom=0.2)
    ax.plot(values,label=shop_id)
    ax.legend(loc='best')

'''多个商家客流量的走势图，可调整时间段，也可以按指定的周几绘图，可以计算avg.'''
def draw_multi_shops(shop_id=[i for i in range(2000)],num_start_day=0,num_end_day=488,week=False,fr='D',_mean=False,_min=False,_std=False,_25=False,_50=False,_75=False,_max=False): 
    start_day = '2015-07-01'
    start_day = datetime.strptime(start_day,'%Y-%m-%d')+timedelta(days=num_start_day)
    end_day = start_day+timedelta(days=num_end_day-num_start_day)
    dates = pd.date_range(start=start_day,end=end_day,freq=fr)
        
    try:
        dates = dates.drop(datetime(2015,12,12))
    except ValueError:
        print ''
            
    delta = (end_day-start_day).days
    count_user_pay = pd.read_csv('../csv/count_pay_and_view/count_user_pay.csv')
    count_user_pay.index = count_user_pay.shop_id.values
    count_user_pay = transform_count_user_pay_datetime(count_user_pay)
    values = count_user_pay.ix[shop_id,dates]
        
    fig = plt.figure(num=random.randint(1,10000))
    ax = fig.add_subplot(111)    
    xticklabels_date=values.columns
    xticklabels_week = []
    for one in xticklabels_date:
        xticklabels_week.append(one.strftime('%a'))
    if(week):
        xticklabels = xticklabels_week
    else:
        xticklabels = xticklabels_date
                
    if(delta<100):
        ax.set_xticks([i for i in range(len(values.columns))])  
        ax.set_xticklabels(xticklabels,rotation=-90)
    ax.set_title(start_day.strftime('%Y-%m-%d')+' ~ '+end_day.strftime('%Y-%m-%d'))
    ax.grid()
    if(_mean):
        _mean = (values.describe()).ix['mean']
        ax.plot(_mean,label='avg')
    elif(_std):
        _std = (values.describe()).ix['std']
        ax.plot(_std,label='std')
    elif(_min):
        _min = (values.describe()).ix['min']
        ax.plot(_min,label='min')     
    elif(_25):
        _25 = (values.describe()).ix['25%']
        ax.plot(_25,label='25%')
    elif(_50):
        _50 = (values.describe()).ix['50%']
        ax.plot(_50,label='50%')
    elif(_75):
        _75 = (values.describe()).ix['75%']
        ax.plot(_75,label='75%')
    elif(_max):
        _max = (values.describe()).ix['max']
        ax.plot(_max,label='max')       
    else:
        for i in shop_id:
            ax.plot(values.ix[i],label=str(i))
    plt.subplots_adjust(bottom=0.2)  
    ax.legend(loc='best')

'''将clf.predict(~) 得到的结果转变为df的格式，，加入shop_id,并且将一个星期变为两个星期。'''
def get_result(result):
    result = result.round()
    if(len(result.shape)==1):
        df = DataFrame(result,columns=[0])
    else:
        df = DataFrame(result,columns=['col_'+str(i) for i in range(result.shape[1])])
    df.insert(0,'shop_id',[i for i in range(1,2001)])
    df = pd.merge(df,df,on='shop_id')
    return df        


def transfrom_Arr_DF(arr,col_name = 'col_'):
    if(len(arr.shape)==1):
        df = DataFrame(arr,columns=['col_0'])
    else:
        df = DataFrame(arr,columns=[col_name+str(i) for i in range(arr.shape[1])])
    return df

def make_OHE(names):
    data = []
    for name in names:
        data.append([name])
            
    enc = preprocessing.OneHotEncoder()
    enc.fit(data)
    OHE_data = enc.transform(data).toarray()  
    return OHE_data
        
        
        


