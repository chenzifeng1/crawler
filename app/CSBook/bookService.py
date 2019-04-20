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
    readFile = open('D:/book_infor/data/books.txt','r',encoding='UTF-8')
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
    sqlStr = 'select * from book_field;'
    cursor.execute(sqlStr)
    book_fields = cursor.fetchall()
    for line in book_fields:
        print(line)