#-*- encoding:utf-8 -*-
import re
import pymysql
import jieba
import codecs
import pandas as pd
import jieba.analyse
import jieba.posseg as psg
from collections import Counter
from mysqlservice import getUsernameAndPassword
from logging import log

LOG_ERROR = 'bookService_ERROR'
LOG_WARNING ='bookService_WARNING'

def writeBookName():

    textrank = jieba.analyse.textrank
    book_namelist = []
    print('begin:')
    rowcount = 0
    readFile = open('D:/book_infor/data/books.txt','r',encoding='UTF-8-sig')
    print('open file success!')
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
    print('mysql connected.')
    print('show tables;')
    cursor.execute('show tables;')
    tables = cursor.fetchall()
    for table in tables:
        print(table)
    print('desc book_field;')
    cursor.execute('desc book_field;')
    booklist = cursor.fetchall()
    for book in booklist:
        print(book)
    for line in readFile.readlines():
        keywords = textrank(line)
        sql_str = "INSERT INTO book_field(book_name,book_field, book_relation) VALUES (%s, %s, %s)"
        try:
            if(len(keywords)==0):
                cursor.execute(sql_str,[line[2:-3], 'CS','Belong to'])
            else:
                for keyword in keywords:
                    cursor.execute(sql_str,[line[2:-3], keyword, 'Belong to'])
            conn.commit()
        except Exception:
            log(LOG_ERROR,'insert failed')
        rowcount = rowcount+ cursor.rowcount
    print(rowcount)
    cursor.close()
    conn.close()
    readFile.close()

def readBookField():
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
    sqlStr = 'select * from book;'
    cursor.execute(sqlStr)
    cursor.close()
    conn.close()
    return cursor


def insertBook():
    file = open('D:/book_infor/data/books.txt','r',encoding='UTF-8-sig')
    books = file.readlines()
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
    textrank = jieba.analyse.textrank
    for book in books:
        sqlStr = 'INSERT INTO book(book_name,book_describe) VALUES (%s,%s)'
        desc = textrank(book,topK=1)
        if(len(desc)==0):
            print(desc)
            cursor.execute(sqlStr,[book[2:-3],'CS'])
        else:
            print(desc)
            cursor.execute(sqlStr, [book[2:-3], desc])
    conn.commit()
    cursor.close()
    conn.close()
    file.close()

def getDoubanBooks():
    try:
        file = open('D:/book_infor/book_info.txt','r',encoding='UTF-8-sig')
        for book in file.readlines():

            for item in book.split(' '):
                print(item)
    except FileNotFoundError:
        print('没有找到文件:'+FileNotFoundError.filename)

def getTags():
    try:
        inputFile = open('D:/book_infor/book_info.txt','r',encoding='UTF-8')
        outputFile = open('D:/book_infor/tag.txt','a',encoding='UTF-8')
    except FileNotFoundError:
        log(LOG_ERROR,'File not found:'+FileNotFoundError.filename)

    tags = []

    for book in inputFile.readlines():
        word = book.split(':')[0]
        if word == 'tag':
            book_tag = book.split(':')[1]
            print(book_tag.replace('\n',''))
            tags.append(book_tag)
    outputFile.writelines(tags)
    inputFile.close()
    outputFile.close()


def getBooks():
    inputFile = open('D:/book_infor/book_infor1.txt', 'r', encoding='UTF-8-sig')

    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database='test',
        charset='utf8'
    )

    for book in inputFile.readlines():
        words = book.split(',')
        if len(words) <= 2 :
            book = book.split(':')[1]
            author = '佚名'
            intepretor = 'null'
            publish = 'null'
            time = 'null'
            price = 'null'
            score = 'null'
            person = 'null'
            tag = 'null'
        else:
            book = words[0].split(':')[1]
            if len(words[1].split(':')) > 1:
                author = words[1].split(':')[1]
            if len(words[2].split(':')) > 1:
                intepretor = words[2].split(':')[1]
            if len(words[3].split(':'))>1:
                publish = words[3].split(':')[1]
            if len(words[4].split(':')) > 1:
                time = words[4].split(':')[1]
            if len(words[5].split(':')) > 1:
                price = words[5].split(':')[1]
            if len(words[6].split(':')) > 1:
                score = words[6].split(':')[1]
            if len(words[7].split(':')) > 1:
                person = words[7].split(':')[1]
            if len(words[8].split(':')) > 1:
                tag = words[8].split(':')[1]

        cursor = conn.cursor()
        sqlstr = 'INSERT INTO douban_book (name,author,intepretor,publish,time,price,score,person,tag)' \
                 ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sqlstr,[book,author,intepretor,publish,time,price,score,person,tag])

    conn.commit()
    cursor.close()
    conn.close()

    inputFile.close()



def get_doubanBook():
    print(123)
    try:
        print('begin:')
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
        print('mysql connected')
    except ConnectionError:
        print('数据库连接失败->error_no:'+ConnectionError.errno)
    sqlStr = 'select * from douban_book'
    cursor.execute(sqlStr)
    result = cursor.fetchall()

    for line in result:
        print(line)
    cursor.close()
    conn.close()
    return result


def insertTag():
    inputFile = open('D:/book_infor/tag.txt', 'r', encoding='UTF-8-sig')
    tags = inputFile.readlines()
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
    for tag in tags:
        sqlStr = 'insert into tag(tag_name) values (%s)'
        cursor.execute(sqlStr,[tag])
    print('insert success')
    conn.commit()
    cursor.close()
    conn.close()
    inputFile.close()

