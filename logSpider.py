#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import re
import requests
from PIL import Image
from StringIO import StringIO

# from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

baseUrl = 'http://50.22.62.66/tools/feedback/bug/'
totalNum = 0
loadedNum = 0
items = []
retryItems = []


# 打开本地文件
def openFile(fileName):
    with codecs.open(fileName, "rb", "utf-8") as f:
        str = f.read()
        return str


# 保存文件到本地
def saveFile(fileName, content):
    with codecs.open(fileName, 'wb', 'utf-8') as f:
        try:
            f.write(content)
        except UnicodeDecodeError, e:
            print UnicodeDecodeError, e


# 获取Html
def getHtml(url, timeout=60):
    # print url
    global html
    html = None
    try:
        page = requests.get(url, timeout=timeout)
    except requests.exceptions.RequestException, e:
        print u'====>下载超时：' + url
    else:
        html = page.content

    return html


# 下载图片
def getImg(html, page):
    reg = r'class="BDE_Image" src="(.*?\.jpg)"'
    imgRe = re.compile(reg)
    imgList = imgRe.findall(html)
    x = 1
    for imgurl in imgList:
        n = "aaa/%04d-%04d.jpg" % (page, x)
        print n
        r = requests.get(imgurl)
        img = Image.open(StringIO(r.content))
        img.save(n)
        x += 1


def getFolder(url):
    arr = url.split("_")
    # print arr

    return 'log/' + arr[1]


# 下载列表中的文件
def downloadItems():
    global loadedNum
    # 下载日志
    for item in items:
        folder = getFolder(item)
        if not os.path.exists(folder) or not os.path.isdir(folder):
            os.mkdir(folder)
        if not os.path.exists(folder + "/" + item):
            str = getHtml(baseUrl + item, 10)
            if str is not None:
                # print str
                saveFile(folder + "/" + item, str)
                loadedNum += 1
                print u'下载成功(%d/%d)：%s' % (loadedNum, totalNum, baseUrl + item)
            else:
                print u'加入retryItems'
                retryItems.append(item)
        else:
            loadedNum += 1
            print u'已存在(%d/%d):%s' % (loadedNum, totalNum, baseUrl + item)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = baseUrl + "reg.php?f=" + sys.argv[1] + "&f1=(.txt)"
    else:
        url = baseUrl + "reg.php?f=*V1.0.45*&f1=(.txt)"

    # 加载日志列表
    html = getHtml(url)
    # 保存日志列表
    if html:
        # print html
        # saveFile("list.html",html)

        # 提取日志链接
        reg = re.compile(r'<a href=[\"|\'](.+?)[\"|\']>')
        items = reg.findall(html)
        totalNum = len(items)
        print u"共 %d 个" % len(items)
        retryItems = []
        for i in xrange(1, 4):
            print u'第 %d 轮下载尝试' % i
            downloadItems()
            if len(retryItems) > 0:
                items = retryItems
                retryItems = []
            else:
                break

        if len(retryItems) == 0:
            print u'all complete!'
        else:
            print u'未成功：'
            print retryItems
    else:
        print u'列表下载失败'
