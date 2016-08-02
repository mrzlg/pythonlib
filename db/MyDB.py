#!/usr/bin/python
# -*- coding: utf-8 -*-

u'''对MySQLdb常用函数进行封装的类

 整理者：兔大侠和他的朋友们（http://www.tudaxia.com）
 日期：2014-04-22
 出处：源自互联网，共享于互联网:-)

 注意：使用这个类的前提是正确安装 MySQL-Python模块。
 官方网站：http://mysql-python.sourceforge.net/
'''

import MySQLdb
import time


class MyDB:
    u'''对MySQLdb常用函数进行封装的类'''

    def __init__(self, cfg):
        # u'构造器：根据数据库连接参数，创建MySQL连接'
        self.error_code = ''  # MySQL错误号码

        self._instance = None  # 本类的实例
        self._conn = None  # 数据库conn
        self._cur = None  # 游标

        self._TIMEOUT = 30  # 默认超时30秒
        self._timeCount = 222
        try:
            self._conn = MySQLdb.connect(host=cfg['host'],
                                         port=cfg['port'],
                                         user=cfg['user'],
                                         passwd=cfg['passwd'],
                                         db=cfg['db'],
                                         charset=cfg['charset'])

        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print error_msg
            # 如果没有超过预设超时时间，则再次尝试连接，
            if self._timeCount < self._TIMEOUT:
                interval = 5
                self._timeCount += interval
                time.sleep(interval)
                self.__init__(cfg)
                return
            else:
                raise Exception(error_msg)

        self._cur = self._conn.cursor()
        self._instance = MySQLdb

    def query(self, sql):
        # print u'执行 SELECT 语句'
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:", e.args[0], e.args[1]
            result = False
        return result

    def update(self, sql):
        # print u'执行 UPDATE 及 DELETE 语句'
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:", e.args[0], e.args[1]
            result = False
        return result

    def insert(self, sql):
        # print u'执行 INSERT 语句。如主键为自增长int，则返回新生成的ID'
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return self._conn.insert_id()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print 'error code: ' + self.error_code
            return False

    def fetchAllRows(self):
        # print u'返回结果列表'
        return self._cur.fetchall()

    def fetchOneRow(self):
        # print u'返回一行结果，然后游标指向下一行。到达最后一行以后，返回None'
        return self._cur.fetchone()

    def getRowCount(self):
        # print u'获取结果行数'
        return self._cur.rowcount

    def commit(self):
        # print u'数据库commit操作'
        self._conn.commit()

    def rollback(self):
        # print u'数据库回滚操作'
        self._conn.rollback()

    def __del__(self):
        # print u'释放资源（系统GC自动调用）'
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass

    def close(self):
        # print u'关闭数据库连接'
        self.__del__()


# if __name__ == '__main__':
#     '''使用样例'''
#
#     # 数据库连接参数
#     dbconfig = {'host': 'localhost',
#                 'port': 3306,
#                 'user': 'dbuser',
#                 'passwd': 'dbpassword',
#                 'db': 'testdb',
#                 'charset': 'utf8'}
#
#     # 连接数据库，创建这个类的实例
#     db = MyDB(dbconfig)
#
#     # 操作数据库
#     sql = "SELECT * FROM `sample_table`"
#     db.query(sql)
#
#     # 获取结果列表
#     result = db.fetchAllRows()
#
#     # 相当于php里面的var_dump
#     print result
#
#     # 对行进行循环
#     for row in result:
#         # 使用下标进行取值
#         # print row[0]
#
#         # 对列进行循环
#         for colum in row:
#             print colum
#
#     # 关闭数据库
#     db.close()
