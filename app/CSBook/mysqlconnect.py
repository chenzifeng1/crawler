import pymysql
from mysqlservice import getUsernameAndPassword

root = getUsernameAndPassword()

conn = pymysql.connect(
    host=root['host'],
    port=3306,
    user=root['username'],
    password=root['password'],
    database='test',
    charset='utf8'
)
cursor = conn.cursor()
sql = """
CREATE TABLE BOOK (
id INT auto_increment PRIMARY KEY ,
bookName VARCHAR NOT NULL UNIQUE,
author CHAR(10) NOT NULL,
kind VARCHAR NOT NULL,
publishTime DATE,
publishingCompany varchar 
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""
# 执行SQL语句
cursor.execute(sql)
# 关闭光标对象
cursor.close()
# 关闭数据库连接

conn.close()
