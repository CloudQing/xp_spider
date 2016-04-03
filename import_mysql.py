#!/usr/bin/python2.6
#coding=UTF-8
import MySQLdb
db=MySQLdb.connect('localhost','root','beibei','python')
sql="SOURCE  /root/python/spider/test.sql;"
cursor=db.cursor()
result=cursor.execute(sql)
db.commit()
db.close()
