import pymysql
from mysqlservice import *


def getNewBookName():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database = "test",
        charset='utf8'
    )

    sqlStr = "select * from book_info;"
    cursor = conn.cursor()
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    i =0
    j =0
    cursor.close()
    conn.close()
    bookname = []
    for line in result:
        i = i+1
        if line not in bookname:
            bookname.append(line)
            j = j+1
            print(line[1])
    print("i:"+str(i))
    print("j:"+str(j))

    return bookname

def getNewAuthor():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database = "test",
        charset='utf8'
    )

    sqlStr = "select author from book_info;"
    cursor = conn.cursor()
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    i =0
    j =0

    cursor.close()
    conn.close()

    authorName = []
    for line in result:
        i = i+1
        if line[0] not in authorName:
            authorName.append(line[0])
            j = j+1
            print(line[0])
    print("i:"+str(i))
    print("j:"+str(j))

    return authorName

def getNewPubulisher():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database="test",
        charset='utf8'
    )

    sqlStr = "select publisher from book_info;"
    cursor = conn.cursor()
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    i=0;
    publisherName =[]
    pattern = re.compile(r"出版")
    for line in result:

        if line[0] not in publisherName and pattern.findall(line[0]):
            publisherName.append(line[0])
    return  publisherName

def getNewTag():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database="test",
        charset='utf8'
    )

    sqlStr = "select * from tag_info;"
    cursor = conn.cursor()
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return  result

def getResult():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database = "test",
        charset='utf8'
    )

    sqlStr = "select * from book_info;"
    cursor = conn.cursor()
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result