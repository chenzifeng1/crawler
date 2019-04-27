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


def writeBookName():
    root = getUsernameAndPassword()
    textrank = jieba.analyse.textrank
    book_namelist = []
    print('begin:')
    rowcount = 0
    readFile = open('D:/book_infor/data/books.txt','r',encoding='UTF-8-sig')
    print('open file success!')
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
            print('insert failed')
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