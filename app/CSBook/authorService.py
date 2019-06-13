import pymysql
from mysqlservice import *
from bookService import *
from py2neo import Graph,Relationship,NodeMatcher,Node
from keywordService import *

graph1 = Graph(host='http://112.74.160.185', http_port=7474, user='neo4j', password='root')
graph2 = Graph('http://112.74.160.185:7474/browser/', user='neo4j', password='root')
graph3 = Graph('https://localhost:7473/browser/', user='neo4j', password='root')
graph4 = Graph(password='neo4j')

graph = graph2.begin()  # 打开图数据库，未打开时不能进行操作
matcher = NodeMatcher(graph) #使用NodeMatcher来查找数据
def insertAuthorFromFile():
    authorFile = open('D:/book_infor/data/nr_nouns1.txt', 'r', encoding='UTF-8-sig')
    root = getUsernameAndPassword()
    conn = pymysql.connect(
        host=root['host'],
        port=3306,
        user=root['username'],
        password=root['password'],
        database='test',
        charset='utf8'
    )
    cursor =conn.cursor()
    for author in authorFile.readlines():
        if len(author.split(':'))>1:
            nation = author.split(':')[0]
            authorname = author.split(':')[1]
            print(nation + ";" + authorname)
        sqlStr = "INSERT INTO author(author_name ,nation)  VALUES(%s,%s)"
        cursor.execute(sqlStr,[authorname,nation])

    conn.commit()
    cursor.close()
    conn.close()


def  insertDoubanAuthor():
    authorFile = open('D:/book_infor/data/nr_nouns1.txt', 'a', encoding='UTF-8-sig')
    books = douba_book()
    authors=[]
    pattern = re.compile(r"\[.*?\]")
    pattern1 = re.compile(r"\(.*?\).*?")
    pattern2 =  re.compile(r"（.*?）")
    pattern3 =  re.compile(r"【.*?】")
    for book in books:
        author = book[2]  #取出作者列
        if len(author)>3: #去除[日]这种情况
            author_s = re.split('、',author) #一本书多个作者的情况
            for author_a in author_s:
                if pattern1.search(author):
                    w =re.split('\)',author_a)
                    if(len(w)>1):
                        nation = re.sub('\(','',w[0])
                        author = w[1]
                elif pattern.search(author):
                    w = re.split('\]',author_a)
                    if len(w)>1:
                        nation = re.sub('\[','',w[0])
                        author = w[1]
                elif pattern2.search(author):
                    w = re.split('）', author_a)
                    if len(w) > 1:
                        nation = re.sub('（', '', w[0])
                        author = w[1]
                elif pattern3.search(author):
                    w = re.split('】', author_a)
                    if len(w) > 1:
                        nation = re.sub('【', '', w[0])
                        author = w[1]
                else:
                    author =author_a
                    nation = '中'
                if author not in authors:
                    authors.append(author)
                    authorFile.write(nation+':'+author+'\n')

    authorFile.close()


       # authors.append(author)
    #return authors

def createNationNode():
    nations = matcher.match('nation') #获取图数据库中的nation节点
    baseNode = Node('base_node', name='国家')  # label为节点标签，name为节点名称，需要注意不要用label='label'否则label会成为节点的的属性

    graph.merge(baseNode,'base_node','name')  # 将节点加入图数据库与create不同之处在于若节点存在则不创建
    for nation in nations:
        relationship = Relationship(nation, 'Inherit from', baseNode)  # 创建a与b之间的Realize关系
        graph.merge(relationship)  # 将关系加入图数据库
    graph.commit()
    return graph