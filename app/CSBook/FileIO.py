import csv
import re


def strdeal(str):
    if str[0] == '[':
        str = str[2:len(str) - 1]
    elif str[0] == '\'':
        str = eval(str)
    return str


data = []
i = 0;
titles = []
urls = []
evaluate = []  # 评价
pattern = re.compile('<Element html at 0x([a-zA-Z0-9]+)>')
for book in open('D:/book_infor/book.txt', 'r', encoding='UTF-8'):
    ismatch = pattern.match(book)
    if ismatch != None:
        continue
    str = book.split(',')
    if i % 3 == 0:
        for s in str:
            evaluate.append(s)
    if i % 3 == 1:
        for s in str:
            s = strdeal(s)
            print(s)
            titles.append(s)

    if i % 3 == 2:
        for s in str:
            urls.append(s)
    i = i + 1

with open('D:/book_infor/book2.txt', 'a',  encoding='UTF-8') as file:
    file.writelines('目录：' + '\n')
    for title in titles:
        file.writelines(title + '\n')
    file.writelines('链接：' + '\n')
    for url in urls:
        file.writelines(url + '\n')
    file.writelines('评价：' + '\n')
    for eval in evaluate:
        file.writelines(eval + '\n')

'''
with open('D:/book_infor/book.xlsx','a',encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile)
    for title in titles:
        writer.writerows(title)
    csvfile.close()
'''

