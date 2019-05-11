import jieba.analyse
from dataService import book_name
import re


def getKeywords():
    file = open('D:/book_infor/bookinfor.txt', 'r', encoding='UTF-8-sig')
    textrank = jieba.analyse.textrank
    book_fields = []
    for line in file.readlines():
        fields = textrank(line,topK=3)
        for field in fields :
            if field not in book_fields and len(field)>1:
                book_fields.append(field)
                print(field)
    return book_fields

def getAuthor():
    file_nr = open('D:/book_infor/data/nr_nouns.txt', 'r', encoding='UTF-8-sig')
    authores = file_nr.readlines()
    file_nr.close()
    return authores


def getField():
    file_nz = open('D:/book_infor/data/nz_nouns.txt', 'a', encoding='UTF-8-sig')
    nouns = file_nz.readlines()
    file_nz.close()
    return nouns


# book_name():去除了带书名号的书名
def getBookName():
    bookFile = open('D:/book_infor/data/book_name1.txt', 'a', encoding='UTF-8-sig')
    pattern = re.compile(r"[0-9]版")
    brackets = re.compile(r"\)")
    erase = re.compile(r"[考研真题+参考教教育软件+售后+可付费打印+非纸质+汇编+软件+按需印刷商品发货时间+非质量问题不接受退换货+易宝典库章节练习模拟试卷教材库+个工作日]")  #需要擦除的描述
    books = []
    for book in book_name():
        newbook = erase.sub('',book)
        if pattern.findall(newbook):
            version = pattern.findall(book)[0]
            bookname = book.split(version)[0]+version+"版"

        elif brackets.findall(newbook):
            bookname = book.split(")")[0]
        else:
            bookname = newbook
        if re.findall('历年',bookname):
            bookname = bookname.split('历年')[0]
        if bookname not in books and len(bookname)<30:
            books.append(bookname)
            bookFile.write(bookname+'\n')

    bookFile.close()


def getBook():
    bookFile = open('D:/book_infor/data/book_name1.txt', 'r', encoding='UTF-8-sig')
    books = bookFile.readlines()
    bookFile.close()
    return books