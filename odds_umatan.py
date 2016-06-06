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
    url="http://keiba.yahoo.co.jp/odds/ut/"+code+"/"
    res=urllib.urlopen(url)
    page=res.read()
    root=etree.fromstring(page,etree.HTMLParser())
    get_umatan(code,root)
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
  

def get_umatan(code,root):
  get_umatan_part(code,root,"mgnBS")
  get_umatan_part(code,root,"mgnBL")

def get_umatan_part(code,root,cls):
  elem=root.xpath('//div[@class="clearFix '+cls+'"]//table')
  jiku=""
  waku=""
  for tbl in elem:
    for tr in tbl.xpath('./tr'):
      if len(tr.xpath("./th[@class='oddsJk']"))!=0:
        jiku=to_s(tr.xpath("./th[@class='oddsJk']")[0].text)
        #print "jiku="+jiku+"\n"
      elif len(tr.xpath("./th"))!=0:
        waku=to_s(tr.xpath("./th")[0].text)
        #print "waku="+waku+"\n"
      td=tr.xpath('./td')
      if len(td) != 0 and jiku!="" and waku!="" :
        odds=to_s(td[0].text)
        #print odds+"\n"
        f=open("data/odds_umatan.txt","a")
        f.write(code+"\t"+jiku+"\t"+waku+"\t"+odds+"\n")
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
  nen=["00","01","02","03","04","05","06","07","08","09","10","11","12","13"]
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
  #get_resultall()
  get_result("1605021210")
