from dataService import dataSplite,dataStore

from mysqlservice import *
import neo4jService
from keywordService import *
from bookService import *
from dataService import *
from PKUSegService import wordCut
import jieba.analyse
inputfile = 'D:/book_infor/bookinfor.txt'




#dataService.dataSplite()

#word_list = dataService.cut_word(inputfile)
#statistic_result=dataService.wordFrequencyCount(word_list,100)
#输出统计结果
#print(statistic_result)

#createTable('test',4)
#writeBookName()
'''
columns = []
result = readBookField().fetchall()
col_result = readBookField().description
'''
#ne

#getDoubanBooks()

getBookName()
#wordCut()































