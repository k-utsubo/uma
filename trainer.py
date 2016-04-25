#!/bin/env python
# coding:utf-8

import urllib
import urllib2
from lxml import etree
import time


def get_trainer(hira):
  p=1
  ret="dummy"
  ss=""
  while(ret!=""):
    ret=get_trainer_list(hira,p)
    p=p+1

def get_trainer_list(hira,p):
  hira=hira.encode('utf-8')
  url="http://keiba.yahoo.co.jp/directory/search/trainer/?%s"
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
    get_trainer_detail(td.attrib['href'])
    ret="dummy"
  time.sleep(1)
  return ret

def get_trainer_detail(param):
  print param
  url="http://keiba.yahoo.co.jp"+param
  res=urllib.urlopen(url)
  page=res.read().replace('\n','').replace('\r','')
  root=etree.fromstring(page,etree.HTMLParser())
  kname=root.xpath('//div[@id="dirTitName"]/p/text()')[0]
  name=root.xpath('//div[@id="dirTitName"]/h1/text()')[0]
  bday=root.xpath('//div[@id="dirTitName"]/ul/li/text()')[0]
  syozoku=root.xpath('//div[@id="dirTitName"]/ul/li/text()')[1]
  menkyo=root.xpath('//div[@id="dirTitName"]/ul/li/text()')[2]
  code=param.split("/")[3]
  f=open("data/trainer.txt","a")
  f.write(code+"\t"+kname.encode('utf-8')+"\t"+name.encode('utf-8')+"\t"+bday.encode('utf-8')+"\t"+"\t"+syozoku.encode('utf-8')+"\t"+menkyo.encode('utf-8')+"\n")
  f.close()

def get_trainerall():
  hira=u"あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわ"
  size=len(hira)
  for i in range(0,size):
    print hira[i:i+1]
    get_trainer(hira[i:i+1])

if __name__ == '__main__':
  get_trainerall()
  #get_trainer_list(u"あ",1)
