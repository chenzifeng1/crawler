from py2neo import Graph,Node,Relationship,NodeMatcher,walk
import pymysql
from keywordService import  douba_book
from mysqlservice import *



def getPublishFromDouban_book():
    result = douba_book()
    pattern = re.compile(r"[0-9]")
    pattern1 =re.compile(r"[出版社]")
    publish = []
    for line in result:
        pub = line[4]
        if not pattern.search(pub) and pub not in publish:
                if pattern1.search(pub):
                    publish.append(pub)
                    print(pub)
    return  publish

def insertPublish():
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

    publishes = getPublishFromDouban_book()
    for line in publishes:
        sqlStr = "insert into publish(publish_name) values (%s)"
        cursor.execute(sqlStr,line)
    conn.commit()
    cursor.close()
    conn.close()
    print("insert success")


def getPublish():
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

    sqlStr = "select * from publish"
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

