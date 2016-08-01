#!/usr/bin/python
# -*- coding: utf-8 -*-
from db.MyDB import MyDB

db = MyDB( {'host':"localhost",'port':3306,'user':"root",'passwd':"123123",'db':'test','charset':'utf8'})
# db.connect()
sql = "SELECT * FROM `log`"
db.query(sql)
# 获取结果列表
result = db.fetchAllRows( );

# 相当于php里面的var_dump
print result
db.close()