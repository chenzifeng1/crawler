import re
from py2neo import Graph,Node,Relationship,NodeMatcher,walk
import pymysql
import jieba.analyse
from bookService import readBookField
from keywordService import getKeywords,getAuthor,douba_book
from authorService import createNationNode
from tagService import getTag
from publishService import getPublish
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
#cow_result = readBookField().description()



#graph1 = Graph(host='localhost', http_port=7978, user='neo4j', password='neo4j')
graph1 = Graph(host='localhost', http_port=7474, user='neo4j', password='neo4j')
graph2 = Graph('http://localhost:7474/browser/', user='neo4j', password='neo4j')
graph3 = Graph('https://localhost:7473/browser/', user='neo4j', password='neo4j')
graph4 = Graph(password='neo4j')

graph = graph1.begin()  # 打开图数据库，未打开时不能进行操作
matcher = NodeMatcher(graph) #使用NodeMatcher来查找数据

def createNode(label_name):
    node = Node('base_node', name=label_name)  # label为节点标签，name为节点名称，需要注意不要用label='label'否则label会成为节点的的属性
    #node['property'] = 'property_info'  # 向node添加属性'property'
    #node.setdefault('age', 18)  # 通过setdefault()方法赋值默认属性
    graph.merge(node,'base_node','name')  # 将节点加入图数据库与create不同之处在于若节点存在则不创建
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


#作者节点
def createAuthorNode():
    authors = getAuthor()
    for line in authors:
        id = line[0]
        author = line[1]
        nation = line[2]
        node = Node('author',name = author)
        node['nation'] = nation
        node['id'] = id
        graph.merge(node,'author','name')
    graph.commit()
    print('insert node success!')

#国籍节点
def createNation():
    file = open('D:/book_infor/data/nation.txt', 'r', encoding='UTF-8-sig')
    for line in file.readlines():
        nation = line.split(':')[0]
        alias = line.split(':')[1]
        node = Node('nation',name = nation)
        node['alias'] = alias
        graph.merge(node,'nation','name')
    graph.commit()
    print('insert success!')

def createRelation(book,keyword):
    book = Node("book", name=book)
    keywordNode = Node("keyword", name=keyword)
    relationship = Relationship(book, 'belong to', keywordNode)  # 创建a与b之间的Realize关系
    relationship['date'] = '2019'  # 在关系上添加data属性
    graph.merge(book, 'book', 'name')
    graph.merge(keywordNode, 'keyword', 'name')
    graph.merge(relationship)  # 将关系加入图数据库
    graph.commit()



def creataBookAuthorRelation(books,authors):
    file = open()#凭借爬取数据来确定关系
    for book in books:
        book = Node("book",name = book)
        for author in authors:
            author = Node("author",name=author)
            relationship =Relationship(book,"is writen by",author)

    graph.merge(book, 'book', 'name')
    graph.merge(author, 'author', 'name')
    graph.merge(relationship)  # 将关系加入图数据库
    graph.commit()



def createAuthor_Nation():
    authors = matcher.match('author') #获取图数据库中的author节点
    nations = matcher.match('nation') #获取图数据库中的nation节点
    print('begin:')
    for author in authors:
        authorname = dict(author)['name']
        nation_alias = dict(author)['nation']
        for nation in nations :
            if nation_alias == re.sub('\n','',dict(nation)['name']):
                relationship = Relationship(author, 'nationality is', nation)  # 创建a与b之间的Realize关系
                graph.merge(relationship)  # 将关系加入图数据库
            elif nation_alias == re.sub('\n','',dict(nation)['alias']):
                relationship = Relationship(author, 'nationality is', nation)  # 创建a与b之间的Realize关系
                graph.merge(relationship)
    print('success')
    other_graph =createNationNode()
    walk()
    graph.commit()


def insertTagNode():
    result = getTag()
    for line in result:
        id = line[0]
        tag = line[1]
        tagNode = Node('tag', name=tag)
        tagNode['id'] = id
        graph.merge(tagNode,'tag','name')
    graph.commit()
    print('insert tag_node success')

def createTagBase():
    tagNodes = matcher.match("tag")
    BaseTag = Node('base_node',name = '领域标签')
    BaseTag["describe"] ="书籍所属的领域标签"
    graph.merge(BaseTag,"base_node","name")
    for tagNode in tagNodes:
        relationship = Relationship(tagNode, 'Inherit_from', BaseTag)  # 创建a与b之间的Realize关系
        relationship["relation"] = "tag_to_base"
        graph.merge(relationship)
    graph.commit()
    print("insert success")


def insertPublishNode():
    publishes = getPublish()
    for line in publishes:
        id = line[0]
        name = line[1]
        node = Node("publish",name=name)
        node["id"] = id
        graph.merge(node,"publish","name")
    graph.commit()
    print("success")

def createPublishBase():
    publishes = matcher.match("publish")
    baseNode = Node("base_node",name="出版社")
    baseNode["describe"]="出版社的基类"
    graph.merge(baseNode,"base_node","name")
    for publish in publishes:
        relation = Relationship(publish,"Inherit_from",baseNode)
        graph.merge(relation)
    graph.commit()
    print("insert success")

def book_tag():
    books = douba_book()
    for book in books:
        bookName = book[1]
        bookTag = book[-1]
        bookNode = Node("book",name = bookName)
        tagNode =Node("tag",name = bookTag)
        graph.merge(bookNode,"book","name")
        graph.merge(tagNode,"tag","name")
        relation = Relationship(bookNode,"belong to",tagNode)
        graph.merge(relation)

    graph.commit()
    print("success")


def book_author():
    other = Node("author",name="佚名")
    graph.merge(other,"author","name")
    authors=[]
    for author in matcher.match("author"):
        authors.append(author["name"])
    books = douba_book()
    print("begin")
    print(len(books))
    for book in books:
        authorName = book[2]
        bookName = book[1]

        print(bookName+":"+authorName)
        for author in authors:
            if re.compile(author).search(authorName):
                print(book+":"+author+':'+authorName)

            #authorNode = Node("author",name=authorName)
            #graph.merge(authorNode,"author","name")
            #relation = Relationship(bookNode,"is_written_by",authorNode)
        #else:
            #print("佚名:"+authorName+bookName)
            #relation = Relationship(bookNode,"is_written_by",other)
        #graph.delete(relation)
    #graph.commit()
    print("success")

def exitConnect():
    graph.finish()