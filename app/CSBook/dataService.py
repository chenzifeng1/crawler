#-*- encoding:utf-8 -*-
import re
import pymysql
import jieba
import codecs
import pandas as pd
import numpy
import jieba.analyse

import jieba.posseg as psg
from collections import Counter

#数据清洗
user_dictionary = 'D:/book_infor/user_dictionary.txt'
jieba.load_userdict(user_dictionary)
# 保存全局分词，用于词频统计
segments = []
#载入停用词
stopwords = [line.strip() for line in codecs.open('D:/book_infor/stoped.txt', 'r', 'utf-8').readlines()]
jieba.analyse.set_stop_words('D:/book_infor/stoped.txt')
#获取书名 注：只含书名号的书名
def dataSplite():
    row = []
    books = []
    infor = []
    patten = re.compile(r'《(.*?)》')
    writeFile = open('D:/book_infor/data/book_infor.txt','a',encoding='UTF-8')
    books_name = []

    with open('D:/book_infor/bookinfor.txt', 'r', encoding='UTF-8') as file:
        row = file.readlines()
        for line in row:
            book = patten.findall(line)
            if len(book)!=0 and book not in books:
                book_name = '《'+book[0]+'》'
                books.append(book)
                line =line.replace(book_name ,' ')
                writeFile.write(book_name+'\n')
                strs = jieba.cut(line)
                writeFile.write(','.join(strs))
        file.close()
        writeFile.close()

def dataStore(bookName,relations):
    conn = pymysql.connect(host='112.74.160.185', port='3306', user='root', password='czf001413', database='test',charset='utf8')
    sqlStr = 'INSERT INTO book (book_name,book_describe)'+'VALUES ('+bookName+','+relations+')'
    cursor = conn.cursor()
    cursor.execute(sqlStr)

    conn.close()

#使用词典进行分词 统计词频
def splitSentence(inputFile):
    try:
        fin = open(inputFile,'r',encoding='utf-8')
        for eachLine in fin:
            line = eachLine.strip()
            patten = re.compile(r'[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+')
            line1 = re.sub(patten,'',line)
            splitedStr = ''

            wordList = list(jieba.cut(line1)) #用结巴分词，对每行内容进行分词
            for word in wordList:
                if word not in stopwords:
                    segments.append({'word':word , 'count':1})
                    splitedStr = splitedStr + word+ ' '

    except FileNotFoundError:
        print('error:文件未找到->'+FileNotFoundError.filename)
    finally:
        # 将结果数组转为df序列
        dfSg = pd.DataFrame(segments)
        dfSg.sort_values(axis = 0,ascending = False,by = 'count')


        # 词频统计
        dfWord = dfSg.groupby('word')

        #dfWord = dfSg.groupby('word')['count'].sum()
        dfWord = dfSg.groupby('word')['count']

        #for dfw in dfWord:
        #print(dfWord.mean())


        # 导出csv
        #dfWord.to_csv('D:/book_infor/keywords.csv','a', encoding='utf_8_sig')
        fin.close()


def word():
    word_c = []  # 分词：词及词性
    word_n = []  # 分词：名词
    patten1 = re.compile(r'n*?')
    # for w in  re.findall(patten1):

    # for x in psg.cut(line1):
    # word_c.append({'word':x.word,'flag':x.flag})

def cut_word(datapath):
    with open(datapath, 'r',encoding='utf-8') as fr:
        string=fr.read()
        print(type(string))
        #对文件中的非法字符进行过滤
        data=re.sub(r"[\s+\.\!\/_,$%^*(【】：\]\[\-:;+\"\']+|[+——！，。？、~@#￥%……&*（）《》]+|[0-9]+","",string)
        word_list= jieba.cut(data)
        print(word_list)
        return word_list


#使用词典进行分词 统计词频
def wordFrequencyCount(word_list,top=100):
    # 统计每个单词出现的次数，别将结果转化为键值对（即字典）
    result = dict(Counter(word_list))
    print(result)
    # sorted对可迭代对象进行排序
    # items()方法将字典的元素转化为了元组，而这里key参数对应的lambda表达式的意思则是选取元组中的第二个元素作为比较参数
    # 排序厚的结果是一个列表，列表中的每个元素是一个将原字典中的键值对转化为的元组
    sortlist = sorted(result.items(), key=lambda item: item[1], reverse=True)
    resultlist = []
    for i in range(0, top):
        resultlist.append(sortlist[i])
    return resultlist

#领域名词清洗
def getNouns():
    textrank = jieba.analyse.textrank
    file = open('D:/book_infor/bookinfor.txt', 'r', encoding='UTF-8-sig')
    book_fields = []
    n_nouns = []  # 名词
    nr_nouns = []  # 人名
    nz_nouns = []  # 其他专有名词
    file_n = open('D:/book_infor/data/n_nouns.txt', 'a', encoding='UTF-8-sig')
    file_nr = open('D:/book_infor/data/nr_nouns.txt', 'a', encoding='UTF-8-sig')
    file_nz = open('D:/book_infor/data/nz_nouns.txt', 'a', encoding='UTF-8-sig')
    for line in file.readlines():
        nouns = psg.cut(line)
        for noun in nouns:
            if noun.flag == 'n' and noun.word+'\n' not in n_nouns and len(noun.word)>1:
                n_nouns.append(noun.word+'\n')
            elif noun.flag =='nr' and noun.word+'\n' not in nr_nouns and len(noun.word)>1:
                nr_nouns.append(noun.word+'\n')
            elif noun.flag =='nz' and noun.word+'\n' not in nz_nouns and len(noun.word)>1:
                nz_nouns.append(noun.word+'\n')
    file_n.writelines(n_nouns)
    file_nr.writelines(nr_nouns)
    file_nz.writelines(nz_nouns)

    print('名词：')
    print(n_nouns)
    print('人名：')
    print(nr_nouns)
    print('专有名词：')
    print(nz_nouns)

    file.close()
    file_n.close()
    file_nr.close()
    file_nz.close()


# 获取书名
def book_name():
    file = open('D:/book_infor/data/book_use.txt', 'r', encoding='UTF-8-sig')
    patten = re.compile(r'[《》]')
    books = []
    for line in file.readlines():
        if patten.findall(line) :
            continue
        else:
            newline =re.sub(r"[\.\!\/_,$%^*(【】：\]\[\-:;+\"\']+|[+—'—！，。？?、~@#￥%……&*（）《》]","",line).strip()
            book=newline.split(' ')[0]
        if len(book)>0 and book not in books:
            books.append(book)
    file.close()
    return books