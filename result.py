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
  return s.encode('utf-8').strip()

def get_result(code):
  try:
    url="http://keiba.yahoo.co.jp/race/result/"+code+"/"
    res=urllib.urlopen(url)
    page=res.read()
    root=etree.fromstring(page,etree.HTMLParser())
    get_course(code,root)
    get_odds(code,root)
    get_resultlist(code,root)
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
  

def get_course(code,root):
  elem=root.xpath('//p[@id="raceTitDay"]/text()')
  date=to_s(elem[0]) # date
  date=to_date(date)
  kaisai=to_s(elem[1]) # kaisai
  hasso=to_s(elem[2]).replace('発走','') # hasso

  elem=root.xpath('//div[@id="raceTitName"]/h1/text()')
  racename=to_s(elem[0]) # race name

  elem=root.xpath('//p[@id="raceTitMeta"]/text()')
  course=to_s(elem[0]).replace('[','') # course
  sarakei=to_s(elem[4]) # sarakei
  teiryo=to_s(elem[5]) #  teiryo
  syokin=to_s(elem[6]) #  syokin

  elem=root.xpath('//p[@id="raceTitMeta"]/img')
  tenki= to_s(elem[0].attrib['alt']) # weather
  turf= to_s(elem[1].attrib['alt']) # turf condition
  f=open("data/race.txt","a")
  f.write(code+"\t"+date+"\t"+kaisai+"\t"+hasso+"\t"+racename+"\t"+course+"\t"+sarakei+"\t"+teiryo+"\t"+syokin+"\t"+tenki+"\t"+turf+"\n")
  f.close()


def get_odds(code,root):
  #elem=root.xpath('//div[@class="clearFix"]/table[@class="resultYen"]/tr')
  elem=root.xpath('//div[@class="clearFix"]/table/tr')
  type=""
  for tr in elem:
    try:
      syubetsu=tr.xpath('./th[@class="txC"]/text()')
      if len(syubetsu)>0 :
        type=to_s(syubetsu[0])
      resultNo=to_s(tr.xpath('./td[@class="txC resultNo"]/text()')[0])
      harai=to_s(tr.xpath('./td[2]/text()')[0]).replace('円','')
      ninki=to_s(tr.xpath('./td[3]/span/text()')[0]).replace('番人気','')
      #print type
      #print resultNo
      #print harai
      #print ninki
      f=open("data/harai.txt","a")
      f.write(code+"\t"+type+"\t"+resultNo+"\t"+harai+"\t"+ninki+"\n")
      f.close()
    except :
      print tr


def get_resultlist(code,root):
  elem=root.xpath('//table[@id="resultLs"]/tr')
#  for tr in elem[1].xpath('./td/text()'):
#    print tr
  cnt=0
  for ele in elem:
    cnt=cnt+1
    if cnt > 1:
      td=ele.xpath('./td')
      if len(td) > 0 :
        try:
          chakujun=to_s(td[0].text)
          wakuban=to_s(td[1].xpath('./span/text()')[0])
          umaban=to_s(td[2].text)
          umano=to_s(td[3].xpath('./a')[0].attrib['href'].replace('/directory/horse/','').replace('/',''))
          umaname=to_s(td[3].xpath('./a/text()')[0])
          seirei=to_s(td[4].text)
          jockeyno=to_s(td[5].xpath('./a')[0].attrib['href'].replace('/directory/jocky/','').replace('/',''))
          jockey=to_s(td[5].xpath('./a/text()')[0])
          racetime=to_s(td[6].text)
          cyakusa=to_s(td[7].text)
          tuka=to_s(td[8].text)
          agari3f=to_s(td[9].text)
          kinryo=to_s(td[10].text)
          bataiju=to_s(td[11].text)
          bataijuzogen=to_s(td[11].xpath('./span/text()')[0])
          ninki=to_s(td[12].text)
          odds=to_s(td[13].text)
          blinker=to_s(td[14].text)
          trainerno=to_s(td[15].xpath('./a')[0].attrib['href'].replace('/directory/trainer/','').replace('/',''))
          trainer=to_s(td[15].xpath('./a/text()')[0])
          s=code+"\t"+chakujun+"\t"+wakuban+"\t"+umaban+"\t"+umano+"\t"+umaname+"\t"+seirei+"\t"+jockeyno+"\t"+jockey+"\t"+racetime+"\t"+cyakusa+"\t"+tuka+"\t"+agari3f+"\t"+kinryo+"\t"+bataiju+"\t"+bataijuzogen+"\t"+ninki+"\t"+odds+"\t"+trainerno+"\t"+trainer
          #print chakujun+"\t"+wakuban+"\t"+umaban+"\t"+umano+"\t"+umaname+"\t"+seirei+"\t"+jockeyno+"\t"+jockey+"\t"+racetime+"\t"+cyakusa
          f=open("data/seiseki.txt","a")
          f.write(s+"\n")
          f.close()
        except:
          print td

def get_result_detail(param):
  print param
  url="http://keiba.yahoo.co.jp"+param
  res=urllib.urlopen(url)
  page=res.read().replace('\n','').replace('\r','')
  root=etree.fromstring(page,etree.HTMLParser())
  name=root.xpath('//div[@id="dirTitName"]/h1/text()')[0]
  bday=root.xpath('//div[@id="dirTitName"]/ul/li/text()')[0]
  syozoku=root.xpath('//div[@id="dirTitName"]/ul/li/text()')[1]
  code=param.split("/")[3]
  f=open("data/result.txt","a")
  f.write(code+"\t"+name.encode('utf-8')+"\t"+bday.encode('utf-8')+"\t"+"\t"+syozoku.encode('utf-8')+"\n")
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
  get_resultall()
  #get_result("1406010111")
  #get_result("0001010101")
