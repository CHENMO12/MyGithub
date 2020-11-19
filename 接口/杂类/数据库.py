# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 10:07
# @Author  : Huizi
import pymysql

# 连接数据库
db = pymysql.connect(host='192.168.0.208', user='xybbc_dev', passwd='xybbc_dev', db='xybbc_dev', port=3306,
                     charset='utf8')

# 使用cursor()方法创建一个游标对象
cursor = db.cursor()

# 使用execute()方法执行SQL语句
cursor.execute("SELECT * from t_bbc_order_sku")

# 使用fetall()获取全部数据
data = cursor.fetchall()

# 打印获取到的数据
n = 0
for i in data:
    n += 1

print(n)

# 关闭游标和数据库的连接
cursor.close()
db.close()


# def connect(host, port, user, passwd, db, charset):
#     r
#
#     eturn None
def update_table(table, name, **kwargs):
    for i in kwargs:
        sql = 'update {}  set {} = {} where {} = {}'.format(table, i, kwargs[i], name, kwargs[name])
