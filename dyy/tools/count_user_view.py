# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 16:16:11 2017

@author: 邓旸旸
"""

'''重启电脑记得打开 MySQL服务'''
import sys
sys.path.append('./')
from tools import conn_MySQL,transform_data
from pandas import DataFrame
from datetime import timedelta,datetime

cursor,db = conn_MySQL()

start_day = datetime(2016,2,1)  #查询开始时间
end_day = datetime(2016,6,21)   #查询结束时间
save_dir = '../count_user_view/'  #结果保存路径

while(start_day<=end_day):
    sql = 'select shop_id,count(user_id) from extra_user_view where time_stamp>="'+\
    start_day.strftime('%Y-%m-%d')+' 00:00:00" and time_stamp<="'+\
    start_day.strftime('%Y-%m-%d')+' 23:59:59" group by shop_id order by shop_id;'
    
    cursor.execute(sql)
    data = cursor.fetchall()
    if(len(data)==0):
        start_day = start_day+timedelta(days=1)
        continue
    data = transform_data(data) #transform_data 将二维的data转变为list

    df = DataFrame(data,columns=['shop_id','count_user_view_'+start_day.strftime('%Y_%m_%d')])
    df.to_csv(save_dir+start_day.strftime('%Y_%m_%d')+'.csv',index=False)
    
    print start_day.strftime('%Y_%m_%d'),'\n'
    start_day = start_day+timedelta(days=1)
    
db.close()