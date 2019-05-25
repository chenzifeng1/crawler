from py2neo import Graph,Node,Relationship,NodeMatcher,walk
import pymysql
from mysqlservice import *

def getTag():
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
    sqlStr = "select * from tag"
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    return result

