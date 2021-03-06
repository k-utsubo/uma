#!/bin/env python
# coding:utf-8

import urllib
import urllib2
from lxml import etree
import time
import re
import datetime

def to_s(s):
  if s is None:
    return ""
  if s == "****":
    return ""
  return s.encode('utf-8').strip()

def get_result(code):
  try:
    url="http://keiba.yahoo.co.jp/odds/tfw/"+code+"/"
    res=urllib.urlopen(url)
    page=res.read()
    root=etree.fromstring(page,etree.HTMLParser())
    get_tanfuku(code,root)
    time.sleep(1)
  except :
    print "error:"+code

def to_date(s):
  s=re.sub('（.*$','',s)
  s=re.sub('年','/',s)
  s=re.sub('月','/',s)
  s=re.sub('日','',s)
  now=datetime.datetime.strptime(s,"%Y/%m/%d")
  return now.strftime("%Y-%m-%d")
  #return s
  

def get_tanfuku(code,root):
  elem=root.xpath('//div[@class="clearFix mgnBL"]//table[@class="dataLs"]')
  for tbl in elem:
    for tr in tbl.xpath('./tr'):
      td=tr.xpath('./td')
      if len(td) != 0:
        waku=td[0].xpath('./span/text()')[0]
        umaban=to_s(td[1].text)
        umano=to_s(td[2].xpath('./a')[0].attrib['href'].replace('/directory/horse/','').replace('/',''))
        tan=to_s(td[3].text)
        fukulow=to_s(td[5].text)
        fukuupp=to_s(td[7].text)

        f=open("data/odds_tanfuku.txt","a")
        f.write(code+"\t"+waku+"\t"+umaban+"\t"+umano+"\t"+tan+"\t"+fukulow+"\t"+fukuupp+"\n")
        f.close()


#http://keiba.yahoo.co.jp/race/result/1403010101/
#14 : 年
#03 : 競馬場
#01 : 第何回
#01 : 第何日
#01 : レース番号
#競馬場:
#01 : 札幌
#02 : 函館
#03 : 福島
#04 : 新潟
#05 : 東京
#06 : 中山
#07 : 中京
#08 : 京都
#09 : 阪神
#10 : 小倉



def get_resultall():
  nen=["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
  jou=["01","02","03","04","05","06","07","08","09","10"]
  kai=["01","02","03","04","05","06","07","08","09","10"]
  nichi=["01","02","03","04","05","06","07","08","09","10"]
  race=["01","02","03","04","05","06","07","08","09","10","11","12"]
  for n in nen:
    for j in jou:
      for k in kai:
        for ni in nichi:
          for r in race:
            get_result( n+j+k+ni+r )

if __name__ == '__main__':
  get_resultall()
  #get_result("1404030211")
  #get_result("0001010101")
