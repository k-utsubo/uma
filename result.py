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
  basyo=re.sub(r'^.*回','',kaisai)
  basyo=re.sub(r'\d.*$','',basyo)

  hasso=to_s(elem[2]).replace('発走','') # hasso

  elem=root.xpath('//div[@id="raceTitName"]/h1/text()')
  racename=to_s(elem[0]) # race name

  grade=""
  if racename.find(')')>=0 and racename.find('(')>=0:
    grade=re.sub(r'^.*（G','',racename)
    grade=re.sub(r'）.*$','',grade)
    grade=str(len(grade))
  
  raceno=str(root.xpath('//td[@id="raceNo"]/text()')[0].replace("R",""))

  elem=root.xpath('//p[@id="raceTitMeta"]/text()')
  course=to_s(elem[0]).replace('[','') # course
  ba=re.sub(r'・.*$','',course)
  mawari=re.sub(r'^.*・','',course)
  mawari=re.sub(r' .*$','',mawari)
  kyori=re.sub(r'^\D*','',course)
  kyori=re.sub(r'm.*$','',kyori)


  sarakei=to_s(elem[6]) # sarakei
  teiryo=to_s(elem[7]) #  teiryo
  racetype=re.sub(r'\[.*$','',teiryo)
  racekinryo=re.sub(r'^.*\] ','',teiryo)


  syokin=to_s(elem[8]) #  syokin
  syokin_tmp=re.sub(r'^.*：','',syokin)
  syokin_tmp=re.sub(r'万円.*$','',syokin_tmp)
  syokin_ary=syokin_tmp.split('、')
  syokin1=""
  syokin2=""
  syokin3=""
  syokin4=""
  syokin5=""
  if len(syokin_ary)>=1:
    syokin1=str(syokin_ary[0])
  if len(syokin_ary)>=2:
    syokin2=str(syokin_ary[1])
  if len(syokin_ary)>=3:
    syokin3=str(syokin_ary[2])
  if len(syokin_ary)>=4:
    syokin4=str(syokin_ary[3])
  if len(syokin_ary)>=5:
    syokin5=str(syokin_ary[4])

  elem=root.xpath('//p[@id="raceTitMeta"]/img')
  tenki= to_s(elem[0].attrib['alt']) # weather
  turf= to_s(elem[1].attrib['alt']) # turf condition
  f=open("data/race.txt","a")
  f.write(code+"\t"+date+"\t"+kaisai+"\t"+hasso+"\t"+racename+"\t"+course+"\t"+sarakei+"\t"+teiryo+"\t"+"\t"+syokin+"\t"+tenki+"\t"+turf+"\n")
  f.close()
  f=open("data/race_data.txt","a")
  f.write(code+"\t"+date+"\t"+raceno+"\t"+basyo+"\t"+hasso+"\t"+grade+"\t"+ba+"\t"+mawari+"\t"+kyori+"\t"+sarakei+"\t"+racetype+"\t"+racekinryo+"\t"+syokin1+"\t"+syokin2+"\t"+syokin3+"\t"+syokin4+"\t"+syokin5+"\t"+tenki+"\t"+turf+"\n")
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
      f=open("data/harai.txt","a")
      f.write(code+"\t"+type+"\t"+resultNo+"\t"+harai+"\t"+ninki+"\n")
      f.close()
      no_ary=resultNo.split('－')
      uma1=""
      uma2=""
      uma3=""
      if len(no_ary)>=1:
        uma1=no_ary[0]
      if len(no_ary)>=2:
        uma2=no_ary[1]
      if len(no_ary)>=3:
        uma3=no_ary[2]
      harai=re.sub(r',','',harai)
      ninki=re.sub(r',','',ninki)

      f=open("data/harai_data.txt","a")
      f.write(code+"\t"+type+"\t"+uma1+"\t"+uma2+"\t"+uma3+"\t"+harai+"\t"+ninki+"\n")
      f.close()
    except :
      print tr


def get_resultlist(code,root):
  elem=root.xpath('//table[@id="resultLs"]/tr')
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
          s=code+"\t"+chakujun+"\t"+wakuban+"\t"+umaban+"\t"+umano+"\t"+umaname+"\t"+seirei+"\t"+jockeyno+"\t"+jockey+"\t"+racetime+"\t"+cyakusa+"\t"+tuka+"\t"+agari3f+"\t"+kinryo+"\t"+bataiju+"\t"+bataijuzogen+"\t"+ninki+"\t"+odds+"\t"+blinker+"\t"+trainerno+"\t"+trainer
          f=open("data/seiseki.txt","a")
          f.write(s+"\n")
          f.close()

          sei=re.sub(r'\d.*$','',seirei)
          rei=re.sub(r'^\D*','',seirei)

          tmp=racetime.split(".")
          racebyo=""
          if len(tmp)==3:
            racebyo=str(int(tmp[0])*60+int(tmp[1])+int(tmp[2])*0.1)
          if len(tmp)==2:
            racebyo=str(int(tmp[0])+int(tmp[1])*0.1)

          tuka1=""
          tuka2=""
          tuka3=""
          tuka4=""
          tmp=tuka.split("-")
          if len(tmp)==4:
            tuka1=tmp[0]
            tuka2=tmp[1]
            tuka3=tmp[2]
            tuka4=tmp[3]

          zogen=0
          tmp=bataijuzogen.replace('(','').replace(')','')
          try:
            zogen=int(tmp)
          except:
            zogen=0
          zogen=str(zogen)

          s=code+"\t"+chakujun+"\t"+wakuban+"\t"+umaban+"\t"+umano+"\t"+sei+"\t"+rei+"\t"+jockeyno+"\t"+racebyo+"\t"+cyakusa+"\t"+tuka1+"\t"+tuka2+"\t"+tuka3+"\t"+tuka4+"\t"+agari3f+"\t"+kinryo+"\t"+bataiju+"\t"+zogen+"\t"+ninki+"\t"+odds+"\t"+blinker+"\t"+trainerno
          f=open("data/seiseki_data.txt","a")
          f.write(s+"\n")
          f.close()
        except:
          print td


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
  #nen=["13"]
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
  #get_result("1605010711")
