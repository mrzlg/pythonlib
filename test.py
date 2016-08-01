#!/usr/bin/python
# -*- coding: utf-8 -*-
from db.MyDB import MyDB

db = MyDB( {'host':"localhost",'port':3306,'user':"root",'passwd':"123123",'db':'test','charset':'utf8'})
# db.connect()
# INSERT INTO `landmap` VALUES (1,'',1,0,1,1,0,0,1,2,'','');
sql = "INSERT INTO `log` VALUES (13234,'2','234234','ttt',2,'zxsds dfg sdfg sdf gsdfg sdfgs ')"
db.insert(sql)
sql = "SELECT * FROM `log`"
db.query(sql)
# 获取结果列表
result = db.fetchAllRows( )

# 相当于php里面的var_dump
print result

# db.close()