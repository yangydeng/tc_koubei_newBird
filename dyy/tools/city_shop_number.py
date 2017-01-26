# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:55:08 2017

@author: 邓旸旸
"""

import MySQLdb
from pandas import DataFrame
import sys
sys.path.append('./')
from tools import transform_data,gb2312


db = MySQLdb.connect(host='localhost',user='root',passwd='Dyy2008723',db='tc_koubei',charset='utf8')

cursor = db.cursor()
sql = 'select city_name,count(*) from shop_info group by city_name order by count(*) desc;'
cursor.execute(sql)
data = cursor.fetchall()

data = transform_data(data)


df = DataFrame(data,columns=['city_name','shop_number'])

print df

df_csv = df.copy()
df_csv.city_name = gb2312(df_csv.city_name)

df.ix[0:50].plot(kind='bar',rot=0,ylim=[0,300])
df.ix[51:100].plot(kind='bar',rot=0,ylim=[0,300])
df.ix[101:].plot(kind='bar',rot=0,ylim=[0,300])
df.plot(kind='bar',rot=0,ylim=[0,300])
cursor.close()