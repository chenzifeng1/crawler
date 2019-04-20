import search

from Item import DDItems
import csv
import re

#import pymysql

#import piplimens

#import getOpener

import getRequest


from lxml import html



item = DDItems()
url = 'http://search.dangdang.com/?key=%BC%C6%CB%E3%BB%FA&act=input'
page = 100
test_urls= search.getUrls(url,page)
tree = ''
list = []
def getPathList(response,xpat=''):

    data = response.text
    #tree = etree.HTML(data)
    etree = html.etree
    tree = etree.HTML(data)

    list = tree.xpath(xpat)

    try:
        print(list)
    except:
        print('error!the expression xpat is null or error')
    return list

for url1 in test_urls:
    response = search.getResopnse(url1)

    xpatTitle = '//a[@name="itemlist-title"]/@title'
    xpatLink = '//a[@name="itemlist-title"]/@href'
    xpatComCount = '//a[@class="search_comment_num"]/text()'
    item.tittle = getPathList(response,xpatTitle)
    item.link = getPathList(response,xpatLink)
    item.commentCount = getPathList(response,xpatComCount)

with open('D:/book_infor/book1.txt','a',newline='') as data:
    data.write(list)

    data.close()


