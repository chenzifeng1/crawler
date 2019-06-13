import re
from py2neo import Graph,Node,Relationship,NodeMatcher,walk
import pymysql
import jieba.analyse
from bookService import readBookField
from keywordService import getKeywords,getAuthor,douba_book
from authorService import createNationNode
from tagService import getTag
from publishService import getPublish
import difflib
import jieba.posseg as psg
from pandas import DataFrame
from newBookInfor import *
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
graph1 = Graph(host='http://112.74.160.185', http_port=7474, user='neo4j', password='root')
graph2 = Graph('http://112.74.160.185:7474/browser/', user='neo4j', password='root')
graph3 = Graph('https://localhost:7473/browser/', user='neo4j', password='root')
graph4 = Graph(password='neo4j')

graph = graph2.begin()  # 打开图数据库，未打开时不能进行操作
matcher = NodeMatcher(graph) #使用NodeMatcher来查找数据

def createNode(label_name):
    node = Node('base_node', name=label_name)  # label为节点标签，name为节点名称，需要注意不要用label='label'否则label会成为节点的的属性
    #node['property'] = 'property_info'  # 向node添加属性'property'
    #node.setdefault('age', 18)  # 通过setdefault()方法赋值默认属性
    graph.merge(node,'base_node','name')  # 将节点加入图数据库与create不同之处在于若节点存在则不创建
    graph.commit()  # 提交图数据库的变更


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
    nationFile = open('D:/book_infor/data/nation_new.txt', 'a', encoding='UTF-8-sig')
    Japan = re.compile(r"日")
    Japan_s =[]
    America = re.compile(r"美")
    America_s =[]
    France = re.compile(r"法")
    France_s =[]
    England = re.compile(r"英")
    England_s =[]
    Denmark = re.compile(r"丹")
    Denmark_s =[]
    Germany = re.compile(r"德")
    Germany_s =[]
    #*********************
    HongKong = re.compile(r"港")
    HongKong_s =[]
    Italy = re.compile(r"意")
    Italy_s =[]
    Canada = re.compile(r"加")
    Canada_s =[]
    China = []
    for author in authors:
        nation = author["name"]

        if Japan.search(nation):
            Japan_s.append(nation)
            print(nation+":"+"日本")
        elif America.search(nation):
            America_s.append(nation)
            print(nation + ":" + "美国")
        elif France.search(nation):
            France_s.append(nation)
        elif England.search(nation):
            England_s.append(nation)
        elif Denmark.search(nation):
            Denmark_s.append(nation)
        elif Germany.search(nation):
            Germany_s.append(nation)
        elif HongKong.search(nation):
            HongKong_s.append(nation)
        elif Italy.search(nation):
            Italy_s.append(nation)
        elif Canada.search(nation):
            Canada_s.append(nation)
        elif len(nation)<4:
            China.append(nation)

    nationFile.write("日本"+"\n")
    nationNode = matcher.match("nation", name="日本")
    for line in Japan_s:
        authorNode =matcher.match("author",name=line)
        relation = Relationship(authorNode.first(),"nationality_is",nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("美国"+"\n")
    nationNode = matcher.match("nation", name="美国")
    for line in America_s:
        authorNode =matcher.match("author",name=line)
        relation = Relationship(authorNode.first(),"nationality_is",nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("英国"+"\n")
    for line in England_s:
        nationNode = matcher.match("nation", name="英国")
        authorNode = matcher.match("author", name=line)
        relation = Relationship(authorNode.first(),"nationality_is",nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("德国"+"\n")
    nationNode = matcher.match("nation", name="德国")
    for line in Germany_s:
        authorNode = matcher.match("author", name=line)
        relation = Relationship(authorNode.first(),"nationality_is",nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("法国"+"\n")
    nationNode = matcher.match("nation", name="法国")
    for line in France_s:
        authorNode = matcher.match("author", name=line)
        relation = Relationship(authorNode.first(),"nationality_is",nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("意大利"+"\n")
    nationNode = matcher.match("nation", name="意大利")
    for line in Italy_s:
        authorNode = matcher.match("author", name=line)
        relation = Relationship(authorNode.first(), "nationality_is", nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("丹麦"+"\n")
    nationNode = matcher.match("nation", name="丹麦")
    for line in Denmark_s:
        authorNode = matcher.match("author", name=line)
        relation = Relationship(authorNode.first(), "nationality_is", nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("香港"+"\n")
    nationNode = matcher.match("nation", name="香港")
    for line in HongKong_s:
        authorNode = matcher.match("author", name=line)
        relation = Relationship(authorNode.first(), "nationality_is", nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("加拿大"+"\n")
    nationNode = matcher.match("nation", name="加拿大")
    for line in Canada_s:
        authorNode = matcher.match("author", name=line)
        relation = Relationship(authorNode.first(), "nationality_is", nationNode.first())
        graph.merge(relation)
    #************************************************************************
    nationFile.write("中国"+"\n")
    nationNode = matcher.match("nation", name="中国")
    for line in China:
        authorNode = matcher.match("author", name=line)
        relation = Relationship(authorNode.first(), "nationality_is", nationNode.first())
        graph.merge(relation)

    graph.commit()
    nationFile.close()

    print("over")
    #graph.commit()


def insertTagNode():
    result = getNewTag()
    for line in result:
        id = line[0]
        tag = line[1]
        page = line[2]
        tagNode = Node('tag', name=tag)
        tagNode['id'] = id
        tagNode['page'] = page
        print(tag)
        graph.merge(tagNode,'tag','name')
    graph.commit()
    print('insert tag_node success')

def createTagBase():
    tagNodes = matcher.match("tag")
    BaseTag = Node('base_node',name = '领域标签')
    BaseTag["describe"] ="书籍所属的领域标签"
    graph.merge(BaseTag,"base_node","name")
    for tagNode in tagNodes:
        relationship = Relationship(tagNode, 'is_a', BaseTag)  # 创建a与b之间的Realize关系
        relationship["relation"] = "tag_to_base"
        graph.merge(relationship)
    graph.commit()
    print("insert success")


def insertPublishNode():
    #publishes = getPublish()
    publishes = getNewPubulisher()
    for line in publishes:
        #id = line[0]
        #name = line[1]
        node = Node("publish",name=line)
        #node["id"] = id
        graph.merge(node,"publish","name")
    graph.commit()
    print("success")



def createPublishBase():
    publishes = matcher.match("publish")
    baseNode = Node("base_node",name="出版社")
    baseNode["describe"]="出版社的基类"
    graph.merge(baseNode,"base_node","name")
    for publish in publishes:
        relation = Relationship(publish,"is_a",baseNode)
        graph.merge(relation)
    graph.commit()
    print("insert success")

def createAuthorBase():
    authors = matcher.match("author")
    baseNode = Node("base_node",name="author")
    baseNode["describe"]="作者的基类"
    graph.merge(baseNode,"base_node","name")
    for author in authors:
        relation = Relationship(author,"is_a",baseNode)
        graph.merge(relation)
    graph.commit()
    print("insert success")


def book_tag():
    result = getResult()

    for line in result:
        bookNode = matcher.match("book",name = line[1])
        tagNode = matcher.match("tag",name = line[-1])
        print(bookNode.first()["name"]+":"+tagNode.first()["name"])
        relation = Relationship(bookNode.first(),"belong_to",tagNode.first())
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

        print(bookName+":"+authorName+"***************************")
        for author in authors:
           # if re.compile(author).search(authorName):
            print(author)

            #authorNode = Node("author",name=authorName)
            #graph.merge(authorNode,"author","name")
            #relation = Relationship(bookNode,"is_written_by",authorNode)
        #else:
            #print("佚名:"+authorName+bookName)
            #relation = Relationship(bookNode,"is_written_by",other)
        #graph.delete(relation)
    #graph.commit()
    print("success")

def addAuthorForBook():
    author = "东野圭吾"
    book = "解忧杂货店"
    nation = "日本"
    author_node = matcher.match("author",{"name":author})

    print(author_node)
    #author_node["nation"] = nation
    author_node = matcher.match("author", "name")
    print("step 1")
    #graph.merge(author_node,"author","name")
    #graph.merge(book_node,"book","name")
    print("step 2")
    #relation = Relationship(book_node,"is_writen_by",author_node)
    #graph.merge(relation)
    print("step 3")
    #graph.commit()
    print("success")

def createNewBookNode():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database="test",
        charset='utf8'
    )

    sqlStr = "select * from book_info;"
    cursor = conn.cursor()
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    for line in result:
        bookNode = Node("book",name=line[1])
        bookNode["book_id"]=line[0]
        print(line[0])
        desc_s = getDesc(line[0])
        if len(desc_s) !=0:
            for desc in desc_s:
                bookNode["desc"] =desc[2]
                bookNode['img'] = desc[3]

        else:
            bookNode["desc"] = "该图书未添加描述"
            bookNode['img'] = '/img/0.jpg'
        graph.merge(bookNode,"book","book_id")
    graph.commit()
    print("success")

def createNewAuthor():
    authors = getNewAuthor()
    for line in authors:
        authorNode =Node("author",name=line)
        graph.merge(authorNode,'author',"name")
    graph.commit()
    print("success")

def createBook_Author():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database="test",
        charset='utf8'
    )

    sqlStr = "select * from book_info;"
    cursor = conn.cursor()
    cursor.execute(sqlStr)
    result = cursor.fetchall()
    i = 0
    cursor.close()
    conn.close()
    print("begin")
    for line in result:
        bookNode = matcher.match("book",name=line[1])
        authorNode = matcher.match("author",name=line[2])

        relation =Relationship(bookNode.first(),"is_written_by",authorNode.first())
        graph.merge(relation)
        print("1")
    graph.commit()

    print("success")

def createNationBase():
    nations = matcher.match("nation")
    baseNode = Node("base_node",name="国家")
    baseNode["describe"]="国籍类的基类节点"
    graph.merge(baseNode,"base_node","name")
    print("begin:")
    for nation in nations:

        relation = Relationship(nation,"is_a",baseNode)
        graph.merge(relation)
    graph.commit()
    print("success")

def book_publisher():
    result =getResult()
    for line in result:
        bookid=line[0]
        bookNode = matcher.match("book",book_id=bookid).first()
        publish = line[3]
        publishNode =matcher.match("publish",name=publish)
        if len(publishNode)>0:
            relation = Relationship(bookNode,"is_published_by",publishNode.first())
            graph.merge(relation)
        else:
            publishNode1 = Node("publish",name=publish)
            graph.merge(publishNode1,"publish","name")
            relation = Relationship(bookNode, "is_published_by", publishNode1)
            graph.merge(relation)
    graph.commit()
    print("success")
def exitConnect():
    graph.finish()

def desc():
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database="test",
        charset='utf8'
    )
    cursor =conn.cursor()
    sql = "select * from book_desc"
    cursor.execute(sql)
    result = cursor.fetchall()
    for line in result:
        id = line[0]
        book_name = line[1]
        book_desc = line[2]
        book_img = line[3]
        node = matcher.match("book",book_id = id)
        node =  node.first()
        node["book_desc"] = book_desc
        print( book_desc)
        node["book_img"] = book_img
        graph.merge(node,"book","book_id")

    graph.commit()
    cursor.close()
    conn.close()