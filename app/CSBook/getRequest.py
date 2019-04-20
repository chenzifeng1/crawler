import urllib.request
import getOpener
import zlib
import codecs
import requests
from xml import etree


def getResopnse(url, opener=''):
    if (opener == ''):
        opener = getOpener.getOpenerf()
    urllib.request.install_opener(opener)
    response = ''
    try:
        response = requests.get(url)
    except:
        print("错误00")
    return response
