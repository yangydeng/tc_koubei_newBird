# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:00:34 2017

@author: 邓旸旸
"""

import MySQLdb
import pandas as pd
#from pandas import DataFrame

df_count = pd.read_csv('../csv/count_user_pay.csv')
db = MySQLdb.connect(host="localhost",user='root',passwd="Dyy2008723",db="tc_koubei",charset="utf8")
cursor = db.cursor()

sql = 'create table count_user_pay('
for col in df_count.columns:
    sql = sql+col+(' int,')

sql = sql[0:len(sql)-1] #把最后一个逗号替换掉
sql = sql+')'

cursor.execute(sql)
cursor.close()
