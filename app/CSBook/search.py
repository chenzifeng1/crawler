import requests


url_book = 'http://book.dangdang.com/'
url_cs = url_book+'/01.54.htm?ref=book-01-A'

#text = requests.get(url_cs).content
#print((text))


def getResopnse(url,opener= ''):
    resopnse = ''
    try:
        resopnse = requests.get(url)
    except:
        print("error!")

    return resopnse

content1 = getResopnse(url_book)
print(content1)

def getUrls(url,page=''):
    suffix = '&page_index='
    newurl = url+suffix
    urls = []
    urls.append(newurl)
    page = int(page)+1
    for i in range(2,page):
        urls.append(newurl[0:len(newurl)]+str(i))
    return urls

