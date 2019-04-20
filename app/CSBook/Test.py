import dataService
from bookService import writeBookName
import mysqlservice
import bookService
inputfile = 'D:/book_infor/bookinfor.txt'
#dataService.dataSplite()

#word_list = dataService.cut_word(inputfile)
#statistic_result=dataService.wordFrequencyCount(word_list,100)
#输出统计结果
#print(statistic_result)

#mysqlservice.createTable('test')
#writeBookName()
bookService.readBookField()