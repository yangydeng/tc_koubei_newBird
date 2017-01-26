# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 17:58:10 2017

@author: 邓旸旸
"""

import MySQLdb
from pandas import DataFrame
import sys
sys.path.append('./')
from tools import transform_data,gb2312


db = MySQLdb.connect(host='localhost',user='root',passwd='Dyy2008723',db='tc_koubei',charset='utf8')

cursor = db.cursor()
#---------------------------cate_1_name---------------------------------------------------
sql = 'select cate_1_name,count(*) from shop_info group by cate_1_name order by count(*) desc;'
cursor.execute(sql)
data = cursor.fetchall()

data = transform_data(data)

df1 = DataFrame(data,columns=['cate_1_name','shop_number'])
print df1

df1.plot(kind='bar',rot=0)
df1_csv = df1.copy()
df1_csv.cate_1_name = gb2312(df1_csv.cate_1_name)
#---------------------------cate_2_name-----------------------------------------------------------
sql = 'select cate_2_name,count(*) from shop_info group by cate_2_name order by count(*) desc;'
cursor.execute(sql)
data = cursor.fetchall()

data = transform_data(data)

df2 = DataFrame(data,columns=['cate_2_name','shop_number'])
print df2

df2.plot(kind='bar',rot=0)
df2_csv = df2.copy()
df2_csv.cate_2_name = gb2312(df2_csv.cate_2_name)
#---------------------------cate_3_name------------------------------------------------------------
sql = 'select cate_3_name,count(*) from shop_info group by cate_3_name order by count(*) desc;'
cursor.execute(sql)
data = cursor.fetchall()

data = transform_data(data)

df3 = DataFrame(data,columns=['cate_3_name','shop_number'])
print df3

df3.plot(kind='bar',rot=0)
df3_csv = df3.copy()
df3_csv.cate_3_name = gb2312(df3_csv.cate_3_name)
cursor.close()