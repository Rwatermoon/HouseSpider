__author__ = 'haolvyuan'
#-*- coding:utf-8 -*-
import encodings
encodings.aliases.aliases['gb2312'] = 'gb18030'
import time,os,datetime,re
import urllib2
from bs4 import BeautifulSoup
import gzip
import StringIO

def mkdir(path):
    # 引入模块
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+' 目录已存在'
        return False

def unzip(data):
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data
def crawlChildurl(url,ParantDir):
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
    req = urllib2.Request(url,headers=headers)
    content = urllib2.urlopen(req).read()
    content = unzip(content)
    content = BeautifulSoup(content,"html5lib",from_encoding='gb18030')
    pageNum=content.find('div',attrs={"class":"fanye gray6"}).span.string
    print re.sub("\D", "", pageNum)
    rentlist=content.find_all('dd',attrs={"class":"info rel floatr"})
    for item in rentlist:
        print item

def crawl(url,rootDir):
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
    req = urllib2.Request(url,headers=headers)
    content = urllib2.urlopen(req).read()
    content = unzip(content)
    content = BeautifulSoup(content,"html5lib",from_encoding='gb18030')

    houseList = content.find_all('div',attrs={"class":"list rel"})
    for item in houseList:

       soup=BeautifulSoup(str(item),"html5lib",from_encoding='utf8')
       print soup.find('span',attrs={'class':'price'}).string
       fieldList=[]
       for child in soup.find('dt'):
           print child.string
           fieldList.append(child.string)
       mkdir(rootDir+"/"+fieldList[0].encode('utf-8'))

       print soup.find('span',attrs={'class':'shequName'}).a.string
       linkList=soup.find_all('a',attrs={"class":"number"})
       print linkList[1]['href']
       for child in soup.find_all('a',attrs={"class":"number"}):
           print child.string
           print child['href']

    return houseList
if __name__ == '__main__':
    url="http://esf.sz.fang.com/housing/"
    rootDir="/Users/rwatermoon/Documents/houseData/"+str(datetime.date.today())
    mkdir(rootDir)
    # crawl(url,rootDir)
    crawlChildurl("http://zu.sz.fang.com/house-xm2810027780/","")
