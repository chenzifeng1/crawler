
from py2neo import Graph,Node,Relationship
import pymysql
import jieba.analyse
from bookService import readBookField
from keywordService import getKeywords,getAuthor
import jieba.posseg as psg
from pandas import DataFrame
'''
host:服务器ip地址，默认为'localhost'
http_port:http协议——服务器监听端口，默认为7474
https_port:https协议——服务器监听端口，默认为7473
bolt_port:bolt协议——服务器监听端口，默认为7687
user:登录用户名，默认为'neo4j'
password:登录密码，无默认值，故若数据库其他参数都为默认值，则可直接通过密码登录
'''
result = readBookField().fetchall()
cow_result = readBookField().description



#graph1 = Graph(host='localhost', http_port=7978, user='neo4j', password='neo4j')
graph1 = Graph(host='localhost', http_port=7474, user='neo4j', password='neo4j')
graph2 = Graph('http://localhost:7474/browser/', user='neo4j', password='neo4j')
graph3 = Graph('https://localhost:7473/browser/', user='neo4j', password='neo4j')
graph4 = Graph(password='neo4j')

graph = graph1.begin()  # 打开图数据库，未打开时不能进行操作


def createNode(label_name):
    node = Node('keyword', name=label_name)  # label为节点标签，name为节点名称，需要注意不要用label='label'否则label会成为节点的的属性
    #node['property'] = 'property_info'  # 向node添加属性'property'
    #node.setdefault('age', 18)  # 通过setdefault()方法赋值默认属性
    graph.merge(node,'keyword','name')  # 将节点加入图数据库与create不同之处在于若节点存在则不创建
    graph.commit()  # 提交图数据库的变更


def createBookNode():
    file = open('D:/book_infor/data/book_name1.txt', 'r', encoding='UTF-8-sig')
    books = file.readlines()
    textrank = jieba.analyse.textrank
    for line in books:
        book = line[2:-3]
        descirbe = textrank(line,topK=1)
        if len(descirbe)==0:
            descirbe = '计算机相关'
        node = Node('book',name= book)
        node['describe'] = descirbe
        node.setdefault('field',1)
        graph.merge(node,'book','name')
    graph.commit()


def creatFieldNode():
    return

def createKeywordNode():
    keywords = getKeywords()
    for keyword in keywords:
        keywordNode = Node('keyword',name=keyword)
        graph.merge(keywordNode,'keyword','name')
    graph.commit()
    print('insert node success!')

def createAuthorNode():
    authors = getAuthor()
    for author in authors:
        node = Node('author',name = author)
        graph.merge(node,'author','name')
    graph.commit()
    print('insert node success!')

def createRelation(book,keyword):
    book = Node("book", name=book)
    keywordNode = Node("keyword", name=keyword)
    relationship = Relationship(book, 'belong to', keywordNode)  # 创建a与b之间的Realize关系
    relationship['date'] = '2019'  # 在关系上添加data属性
    graph.merge(book, 'book', 'name')
    graph.merge(keywordNode, 'keyword', 'name')
    graph.merge(relationship)  # 将关系加入图数据库
    graph.commit()


def creataBookAuthorRelation():
    
    return

