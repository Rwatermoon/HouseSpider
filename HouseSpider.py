__author__ = 'haolvyuan'
#-*- coding:utf-8 -*-
import encodings
encodings.aliases.aliases['gb2312'] = 'gb18030'
import time
import urllib2
from bs4 import BeautifulSoup
def unzip(data):
        import gzip
        import StringIO
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data

def crawl(url):
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
    req = urllib2.Request(url,headers=headers)
    content = urllib2.urlopen(req).read()
    content = unzip(content)
    content = BeautifulSoup(content,"html5lib",from_encoding='gb18030')
    print content.original_encoding
    result = content.find_all('div',attrs={"class":"list rel"})
    for item in result:
       soup=BeautifulSoup(str(item),"html5lib",from_encoding='utf8')
       print soup.find('span',attrs={'class':'price'}).string
       for child in soup.find('dt'):
           print child.string
       print soup.find('span',attrs={'class':'shequName'}).a.string

       for child in soup.find_all('a',attrs={"class":"number"}):
           print child.string
           print child['href']

    return result
if __name__ == '__main__':
    url="http://esf.sz.fang.com/housing/"
    for i in range(500):
        print i
        print crawl(url)
        time.sleep(5)






