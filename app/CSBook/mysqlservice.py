import pymysql
import re
import traceback

#获取用户名和密码
def getUsernameAndPassword():
    file =open('D:/book_infor/data/mysql.txt','r',encoding='UTF-8-sig')
    host = file.readline().replace('\n','')
    username = file.readline().replace('\n','')
    password = file.readline()
    return {'host':host,'username':username,'password':password}

#创建数据库
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
    existFlag = isExist(databases,databaseName)
    if existFlag:
        print('数据库已存在')
    else:
        sqlStr  = 'create database ' +databaseName+ ' default charset utf8 collate utf8_unicode_ci;'
        cursor.execute(sqlStr)
    cursor.close()

#显示数据库
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

#创建表
def createTable(DBName):
    root = getUsernameAndPassword()
    try:
        conn = pymysql.connect(
            host=root['host'],
            port=3306,
            user=root['username'],
            password=root['password'],
            database=DBName,
            charset='utf8'
        )
        sqlStr ='''create table `book_field` (
            `name_id` INT NOT NULL AUTO_INCREMENT,
            `book_name` VARCHAR(50) NOT NULL ,
            `book_field` VARCHAR(50) NOT NULL ,
            `book_relation` VARCHAR(10) NOT NULL , 
            PRIMARY KEY(name_id));'''
        sqlStr1 ='''create table `book_author` (
            `name_id` INT NOT NULL AUTO_INCREMENT,
            `book_name` VARCHAR(50) NOT NULL ,
            `author_name` VARCHAR(50) NOT NULL ,
            `relation` VARCHAR(10) NOT NULL , 
            PRIMARY KEY(name_id));'''
        sqlStr2 ='''create table `book` (
            `book_id` INT NOT NULL AUTO_INCREMENT,
            `book_name` VARCHAR(50) NOT NULL ,
            `book_describe` VARCHAR(100) NOT NULL ,
            PRIMARY KEY(book_id));'''
        sqlStr3 ='''create table `field` (
            `field_id` INT NOT NULL AUTO_INCREMENT,
            `field_name` VARCHAR(50) NOT NULL ,
            `field_describe` VARCHAR(50) NOT NULL , 
            PRIMARY KEY(field_id));'''
        cursor = conn.cursor()
        cursor.execute('show tables;')
        row = cursor.fetchall()
        exist_flag = isExist(row,'book_field')
        if exist_flag:
            print('数据表已存在')
        else:
            cursor.execute(sqlStr)
    except:
        traceback.print_exc()
    finally:
        conn.close()

#查找数据库或数据表是否存在
def isExist(row,search_name):
    List = re.findall('(\'.*?\')',str(row))
    List = [re.sub("'", '', each) for each in List]
    if search_name in List:
        return True
    else:
        return False

#向数据表中插入数据
def insertData(DBName,datas):
    root = getUsernameAndPassword()
    sqlStr = 'insert '
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database=DBName,
        charset='utf8'
    )

