# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 21:44:33 2017

@author: 邓旸旸
"""
'''重启电脑记得打开 MySQL服务'''

import MySQLdb
from pandas import DataFrame
from datetime import timedelta,datetime

db = MySQLdb.connect(host="localhost",user='root',passwd="Dyy2008723",db="tc_koubei",charset="utf8")

cursor = db.cursor()  

start_day = datetime(2016,7,1)  #查询开始时间
end_day = datetime(2016,10,31)   #查询结束时间
save_dir = 'H://tc_koubei_newBird//dyy//csv//'  #结果保存路径

while(start_day<=end_day):
    sql = 'select shop_id,count(user_id) from user_pay where time_stamp>="'+\
    start_day.strftime('%Y-%m-%d')+' 00:00:00" and time_stamp<="'+\
    start_day.strftime('%Y-%m-%d')+' 23:59:59" group by shop_id order by shop_id;'
    
    cursor.execute(sql)
    data = cursor.fetchall()
    data = list(data)
    i=0
    for row in data:
        data[i] = list(row)
        i=i+1
        
    df = DataFrame(data,columns=['shop_id','count_user_pay_'+start_day.strftime('%Y_%m_%d')])
    df.to_csv(save_dir+start_day.strftime('%Y_%m_%d')+'.csv',index=False)
    
    print start_day.strftime('%Y_%m_%d'),'\n'
    start_day = start_day+timedelta(days=1)
    
db.close()