import pymysql
import re
import traceback

# 获取用户名和密码
def getUsernameAndPassword():
    file = open('D:/book_infor/data/mysql.txt', 'r', encoding='UTF-8-sig')
    host = file.readline().replace('\n', '')
    username = file.readline().replace('\n', '')
    password = file.readline()
    return {'host': host, 'username': username, 'password': password}


# 创建数据库
def creatDatabase(databaseName):
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        charset='utf8'
    )
    databases = showDatabases()
    cursor = conn.cursor()
    existFlag = isExist(databases, databaseName)
    if existFlag:
        print('数据库已存在')
    else:
        sqlStr = 'create database ' + databaseName + ' default charset utf8 collate utf8_unicode_ci;'
        cursor.execute(sqlStr)
    cursor.close()


# 显示数据库
def showDatabases():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        charset='utf8'
    )
    sqlStr = 'show databases ;'
    cursor = conn.cursor()
    cursor.execute(sqlStr)
    row = [cursor.fetchall()]
    for r in row:
        print(r)
    conn.close()
    return row


# 创建表
'''
@:param DBName 数据库名
@:param num 对应的表名
    0:book_field
    1:book_author
    2:book
    3:field
'''


def createTable(DBName, num):
    root = getUsernameAndPassword()
    SQL = ''
    table_name = ''
    try:
        conn = pymysql.connect(
            host=root['host'],
            port=3306,
            user=root['username'],
            password=root['password'],
            database=DBName,
            charset='utf8'
        )
        sqlStr0 = '''create table `book_field` (
            `name_id` INT NOT NULL AUTO_INCREMENT,
            `book_name` VARCHAR(50) NOT NULL ,
            `book_field` VARCHAR(50) NOT NULL ,
            `book_relation` VARCHAR(10) NOT NULL , 
            PRIMARY KEY(name_id));'''
        sqlStr1 = '''create table `book_author` (
            `name_id` INT NOT NULL AUTO_INCREMENT,
            `book_name` VARCHAR(50) NOT NULL ,
            `author_name` VARCHAR(50) NOT NULL ,
            `relation` VARCHAR(10) NOT NULL , 
            PRIMARY KEY(name_id));'''
        sqlStr2 = '''create table `book` (
            `book_id` INT NOT NULL AUTO_INCREMENT,
            `book_name` VARCHAR(50) NOT NULL ,
            `book_describe` VARCHAR(100) NOT NULL ,
            PRIMARY KEY(book_id));'''
        sqlStr3 = '''create table `field` (
            `field_id` INT NOT NULL AUTO_INCREMENT,
            `field_name` VARCHAR(50) NOT NULL ,
            `field_describe` VARCHAR(50) NOT NULL , 
            PRIMARY KEY(field_id));'''
        sql_douban = '''create table `douban_book` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(50) NOT NULL ,
            `author` VARCHAR(50) NOT NULL , 
            `intepretor` VARCHAR(50) NOT NULL,
            `publish` VARCHAR(50) NOT NULL,
            `time` VARCHAR(50) NOT NULL,
            `price` VARCHAR(50) NOT NULL,
            `score` VARCHAR(50) NOT NULL,
            `person` VARCHAR(50) NOT NULL,
            `tag` VARCHAR(50) NOT NULL,
            PRIMARY KEY(id));'''

        sql_tag = '''create table `tag` (
            `tag_id` INT NOT NULL AUTO_INCREMENT,
            `tag_name` VARCHAR(50) NOT NULL ,
            PRIMARY KEY(tag_id));'''
        sql_author = '''create table `author` (
            `author_id` INT NOT NULL AUTO_INCREMENT,
            `author_name` VARCHAR(50) NOT NULL ,
            `nation` VARCHAR(50) NOT NULL,
            PRIMARY KEY(author_id));'''
        sql_publish = '''create table `publish` (
            `publish_id` INT NOT NULL AUTO_INCREMENT,
            `publish_name` VARCHAR(50) NOT NULL ,
            PRIMARY KEY(publish_id));'''
        cursor = conn.cursor()
        cursor.execute('show tables;')
        row = cursor.fetchall()
        if num == 0:
            SQL = sqlStr0
            table_name = 'book_field'
        elif num == 1:
            SQL = sqlStr1
            table_name = 'book_author'
        elif num == 2:
            SQL = sqlStr2
            table_name = 'book'
        elif num == 3:
            SQL = sqlStr3
            table_name = 'field'
        elif num ==4 :
            SQL = sql_douban
            table_name = 'douban_book'
        elif num ==5:
            SQL = sql_tag
            table_name = 'tag'
        elif num ==6:
            SQL = sql_author
            table_name = 'author'
        elif num ==7:
            SQL =sql_publish
            table_name = 'publish'
        else:
            print('请补充')
        exist_flag = isExist(row, table_name)

        if exist_flag:
            print('数据表已存在')
        else:
            cursor.execute(SQL)
            print('create table:' + table_name)

    except:
        traceback.print_exc()
    finally:
        conn.close()


# 查找数据库或数据表是否存在
def isExist(row, search_name):
    List = re.findall('(\'.*?\')', str(row))
    List = [re.sub("'", '', each) for each in List]
    if search_name in List:
        return True
    else:
        return False


def selectData(DBName,table):
    root = getUsernameAndPassword()
    sqlStr =  "SELECT * FROM "+ table
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database=DBName,
        charset='utf8'
    )
    cursor =conn.cursor()
    cursor.execute(sqlStr)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result