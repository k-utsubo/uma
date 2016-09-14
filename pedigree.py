#!/bin/env python
# coding:utf-8

import urllib
import urllib2
from lxml import etree
import time
import re


def get_pedigree(hira):
  p=1
  ret="dummy"
  ss=""
  while(ret!=""):
    ret=get_pedigree_list(hira,p)
    p=p+1

def get_pedigree_list(hira,p):
  hira=hira.encode('utf-8')
  url="http://keiba.yahoo.co.jp/directory/horse/%s/"
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
    get_pedigree_detail(td.attrib['href'])
    ret="dummy"
  time.sleep(1)
  return ret

def get_pedigree_detail(code):
  print code
  url="http://keiba.yahoo.co.jp/directory/horse/"+code
  res=urllib.urlopen(url)
  page=res.read().replace('\n','').replace('\r','')
  root=etree.fromstring(page,etree.HTMLParser())
  td=root.xpath('//table[@id="dirUmaBlood"]//td/text()')
  f=td[0].encode('utf-8')
  ff=td[1].encode('utf-8')
  fff=td[2].encode('utf-8')
  ffm=td[3].encode('utf-8')
  fm=td[4].encode('utf-8')
  fmf=td[5].encode('utf-8')
  fmm=td[6].encode('utf-8')
  m=td[7].encode('utf-8')
  mf=td[8].encode('utf-8')
  mff=td[9].encode('utf-8')
  mfm=td[10].encode('utf-8')
  mm=td[11].encode('utf-8')
  mmf=td[12].encode('utf-8')
  mmm=td[13].encode('utf-8')
  print "父:"+f
  print "父父:"+ff
  print "父父父:"+fff
  print "父父母:"+ffm
  print "父母:"+fm
  print "父母父:"+fmf
  print "父母母:"+fmm
  print "母:"+m
  print "母父:"+mf
  print "母父父:"+mff
  print "母父母:"+mfm
  print "母母:"+mm
  print "母母父:"+mmf
  print "母母母:"+mmm
  name=root.xpath('//div[@id="dirTitName"]//h1/text()')[0]
  print "bamei:"+name
  ele=root.xpath('//div[@id="dirTitName"]//ul/li/text()')
  bday=ele[0].encode('utf-8')
  bday=re.sub(r'年','-',bday)
  bday=re.sub(r'月','-',bday)
  bday=re.sub(r'日','',bday)
  print "bday:"+bday
  keiro=ele[1].encode('utf-8')
  print "keiro:"+keiro
  banusi=ele[3].encode('utf-8')
  print "banusi:"+banusi
  seisan=ele[4].encode('utf-8')
  print "seisan:"+seisan
  sanchi=ele[5].encode('utf-8')
  print "sanchi:"+sanchi
  #return
  fi=open("data/pedigree.txt","a")
  fi.write(code+"\t"+f+"\t"+ff+"\t"+fff+"\t"+ffm+"\t"+fm+"\t"+fmf+"\t"+fmm+"\t"+m+"\t"+mf+"\t"+mff+"\t"+mfm+"\t"+mm+"\t"+mmf+"\t"+mmm)
  fi.close()
  fi.open("data/uma.txt","a")
  fi.write(code+"\t"+name+"\t"+bday+"\t"+keiro+"\t"+banusi+"\t"+seisan+"\t"+sanchi)
  fi.close()

def get_pedigreeall():
  hira=u"あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよわ"
  size=len(hira)
  for i in range(0,size):
    #print hira[i:i+1]
    get_pedigree(hira[i:i+1])
    exit 

if __name__ == '__main__':
  get_pedigreeall()
  #get_pedigree_detail(u"2010104902")
