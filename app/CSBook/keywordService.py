import jieba.analyse


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