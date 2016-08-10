#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import re
import requests
import gevent
from gevent import monkey
from PIL import Image
from StringIO import StringIO

# from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
monkey.patch_all()

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
    result = None
    try:
        page = requests.get(url, timeout=timeout)
    except requests.exceptions.RequestException, e:
        print u'====>下载超时：' + url
        result = None
    else:
        result = page.content

    return result


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


def downloadOneItem(item):
    global loadedNum
    folder = getFolder(item)
    if not os.path.exists(folder) or not os.path.isdir(folder):
        os.makedirs(folder)
    print u'----->开始下载(%d/%d)：%s' % (totalNum - len(items), totalNum, baseUrl + item)
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
    if len(items) > 0:
        item = items.pop()
        gevent.spawn(downloadOneItem, item).join()


# 下载列表中的文件
def downloadItems():
    # 下载日志
    length = min(len(items), 200)
    print u'并发%d个' % length
    temp = []
    for i in xrange(length):
        temp.append(gevent.spawn(downloadOneItem, items.pop()))

    gevent.joinall(temp)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = baseUrl + "reg.php?f=" + sys.argv[1] + "&f1=(.txt)"
    else:
        url = baseUrl + "reg.php?f=*V1.0.46*&f1=(.txt)"

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
        for i in xrange(1, 5):
            downloadItems()
            print u'======================= 第 %d 轮下载尝试 (%d)========================' % (i, len(retryItems))
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
