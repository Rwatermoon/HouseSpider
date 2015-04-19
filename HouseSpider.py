__author__ = 'haolvyuan'
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
def writefile(path,data):
    try:
        file_object = open(path,'w')
        file_object.writelines(data)
        file_object.close()
    except Exception as e:
        print(e)

def unzip(data):
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data
def getInfo(url):
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
    req = urllib2.Request(url,headers=headers)
    content = urllib2.urlopen(req).read()
    content = unzip(content)
    content = BeautifulSoup(content,"html5lib",from_encoding='gb18030')
    rentlist=content.find_all('dd',attrs={"class":"info rel floatr"})
    resultLines=[]
    for item in rentlist:
        fieldList=[]
        strLine=""
        soup=BeautifulSoup(str(item),"html5lib",from_encoding='utf8')
        print soup.find('span',attrs={"class":"price"}).string
        fieldList.append(str(soup.find('span',attrs={"class":"price"}).string).strip())
        print soup.find('p',attrs={"class":"alignR mt8"}).string
        t=soup.find('p',attrs={"class":"alignR mt8"}).string
        fieldList.append(str(soup.find('p',attrs={"class":"alignR mt8"}).string).strip())
        data=soup.find('p',attrs={"class":"gray6 mt10"}).string
        #pattern=re.compile(u"[\u4e00-\u9fa5_0-9]+")
        pattern=re.compile('/(?<=>).*?(?=<)/')
        result=pattern.findall(unicode(data))
        for datafiled in result:
            print(datafiled)
            fieldList.append(str(datafiled).strip())

        for filed in fieldList:
            strLine+=filed+','
        resultLines.append(strLine)
    return resultLines

def crawlChildurl(url,ParantDir):
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
    req = urllib2.Request(url,headers=headers)
    content = urllib2.urlopen(req).read()
    content = unzip(content)
    content = BeautifulSoup(content,"html5lib",from_encoding='gb18030')
    pageNum=content.find('div',attrs={"class":"fanye gray6"}).span.string
    Num=int(re.sub("\D", "", pageNum))
    for index in range(1,Num+1):
        # time.sleep(5)
        outputData=[]
        outputData=(getInfo(url+"/i3"+str(index)+"/"))
        outputData=[line+'\n' for line in  outputData]
        outPath=ParantDir+'/'+'Page'+str(index)+""
        writefile(outPath,outputData)
    return True
        # rentlist=content.find_all('dd',attrs={"class":"info rel floatr"})
        # for item in rentlist:
        #    fieldList=[]
        #    soup=BeautifulSoup(str(item),"html5lib",from_encoding='utf8')
        #    print soup.find('span',attrs={"class":"price"}).string
        #    print soup.find('p',attrs={"class":"alignR mt8"}).string
        #    data=soup.find('p',attrs={"class":"gray6 mt10"})
        #
        #    pattern=re.compile(u"[\u4e00-\u9fa5]+")
        #    result=pattern.findall(unicode(data))
        #    for item in result:
        #        print(item)

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
       fieldList=[]
       soup=BeautifulSoup(str(item),"html5lib",from_encoding='utf8')
       print soup.find('span',attrs={'class':'price'}).string
       fieldList.append(soup.find('span',attrs={'class':'price'}).string)
       print soup.find('div',attrs={'class':'info rel floatl ml15'}).dd
       for child in soup.find('dt'):
           print child.string
           fieldList.append(child.string)
       print soup.find('span',attrs={'class':'shequName'}).a.string
       fieldList.append(soup.find('span',attrs={'class':'shequName'}).a.string)
       linkList=soup.find_all('a',attrs={"class":"number"})
       print linkList[1]['href']
       for child in soup.find_all('a',attrs={"class":"number"}):
           print child.string
           print child['href']
       dirPath=rootDir+"/"+fieldList[1].encode('utf-8')
       mkdir(dirPath)

       file_object = open(dirPath+"/"+fieldList[1].encode('utf-8')+".txt",'w')
       for field in fieldList:
           file_object.write(field.encode('utf-8'))
           file_object.write(',')
       file_object.close()





    return houseList
if __name__ == '__main__':
    url="http://esf.sz.fang.com/housing/"
    rootDir="/Users/rwatermoon/Documents/houseData/"+str(datetime.date.today())
    mkdir(rootDir)
    # crawl(url,rootDir)
    crawlChildurl("http://zu.tj.fang.com/house-xm1110039333/","/Users/rwatermoon/Documents/houseData/2015-04-18")











