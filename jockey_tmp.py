#!/bin/env python
# coding:utf-8

import urllib
import urllib2
from lxml import etree
import time


def get_jockey(hira):
  p=1
  ret="dummy"
  ss=""
  while(ret!=""):
    ret=get_jockey_list(hira,p)
    p=p+1

def get_jockey_list(hira,p):
  hira=hira.encode('utf-8')
  url="http://keiba.yahoo.co.jp/directory/jockeysearch/?%s"
  params={"hq":hira,"p":p}
  data=urllib.urlencode(params)
  #print data
  res=urllib.urlopen(url % data)
  page=res.read()
  root=etree.fromstring(page,etree.HTMLParser())
  elem=root.xpath('//table[@class="dataLs mgnBS"]/tr/td/a')
  i=0
  ret=""

  for td in elem:
    get_jockey_detail(td.attrib['href'])
    ret="dummy"
  time.sleep(1)
  return ret

def get_jockey_detail(param):
  print param
  url="http://keiba.yahoo.co.jp"+param
  res=urllib.urlopen(url)
  page=res.read().replace('\n','').replace('\r','')
  root=etree.fromstring(page,etree.HTMLParser())
  name=root.xpath('//div[@id="dirTitName"]/h1/text()')[0]
  bday=root.xpath('//div[@id="dirTitName"]/ul/li/text()')[0]
  syozoku=root.xpath('//div[@id="dirTitName"]/ul/li/text()')[1]
  code=param.split("/")[3]
  f=open("data/jockey.txt","a")
  f.write(code+"\t"+name.encode('utf-8')+"\t"+bday.encode('utf-8')+"\t"+"\t"+syozoku.encode('utf-8')+"\n")
  f.close()

def get_jockeyall():
  hira=u"あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわ"
  size=len(hira)
  for i in range(0,size-1):
    print hira[i:i+1]
    get_jockey(hira[i:i+1])

if __name__ == '__main__':
  #get_jockeyall()
  get_jockey_list(u"わ",1)
