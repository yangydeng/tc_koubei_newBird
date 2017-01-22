# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 21:44:33 2017

@author: 邓旸旸
"""

import MySQLdb
conn = MySQLdb.connect(host="localhost",user='root',passwd="Dyy2008723",db="tc_koubei",charset="utf8")

cursor = conn.cursor()  

n=cursor.execute('select * from shop_info')

for row in cursor.fetchall():
    for r in row:
        print r
    print '\n'