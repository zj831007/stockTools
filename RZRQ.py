# -*- coding: utf-8 -*-
# @Author: Jian Zhang
# @Date:   2016-07-30 11:30:07  融资融券
# @Last Modified by:   Jian Zhang
# @Last Modified time: 2016-07-31 23:26:58

import urllib2
import json
import datetime,time
import os
import codecs
import re
import HTMLParser
import sys
from bs4 import BeautifulSoup



def getLHBdata(page):
	try:
		url = "http://data.10jqka.com.cn/market/rzrq/board/ls/field/rzjmr/order/desc/page/%s/ajax/1/" % (page)

		print "url: %s" % (url)
		response = urllib2.urlopen(url, timeout = 1000)
		html = response.read()
		response.close()

		html = unicode(html, "gbk").encode("utf8")
		
		return html

	except urllib2.URLError as e:
		print e.reason

def getHistoryData(code, page):
	try:
		url = "http://data.10jqka.com.cn/market/rzrqgg/code/%s/order/desc/page/%s/ajax/1/" % (code,page)

		print "url: %s" % (url)
		response = urllib2.urlopen(url, timeout = 1000)
		html = response.read()
		response.close()

		html = unicode(html, "gbk").encode("utf8")
		
		return html

	except urllib2.URLError as e:
		print e.reason

#
# datestr  日期字符串
# datano   数据编号 3 机构净买
# content  
#		 
def  appendFile(datestr, datano,content):
	datestr = "history"
	filepath = "data/RZRQ/%s_%s.txt" %(datestr, datano)

	f=open(filepath,'a')
	
	f.write(content)

	f.write('\n')
	f.close()

def generateHistory(scode, page):
	
	if page > 2:
		return

	htmlData = getHistoryData(scode, page);  

	soup = BeautifulSoup(htmlData)

	trs  = soup.table.tbody.find_all("tr")
	
	

	if len(trs) <1:
		return

	for tr in trs:
		tds = tr.find_all("td")
		
		tradedate = str(tds[1].string).strip()
		bmoney = tds[3].string
		smoney = tds[4].string
		
		if tradedate == '':
			return

		if bmoney[-1] == '万':
			bmoney = bmoney[:-1]
		else:
			bmoney = float(bmoney[:-1])*10000

		if smoney[-1] == '万':
			smoney = smoney[:-1]
		else:
			smoney = float(smoney[:-1])*10000

		
		tdate = datetime.datetime.strptime(tradedate,'%Y-%m-%d').date()
		tdatestr = datetime.datetime.strftime(tdate,'%Y%m%d')
		
		
		exchangeType = 1  #交易所类型：0 深圳  1 上证
		# 1、深圳创业板股票的代码是：300XXX 的股票
		# 2、而深圳中小板股票的代码是：002XXX 开头的股票
		# 3、上海主板的股票代码是：60XXXX 开头的股票
		# 4、深圳主板的股票代码是：000XXX 开头的股票

		if (int)(scode[:3]) < 600:
			exchangeType = 0

		rzrqb = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,bmoney)
		rzrqs = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,smoney)
		# print rzrqb
		# print rzrqs
		
		appendFile(tdatestr, "89", rzrqb)
		appendFile(tdatestr, "90", rzrqs)
		
		
	generateHistory(scode,page+1) 
	

def generateDataFile(currdate, page):
	

	htmlData = getLHBdata(page);  

	soup = BeautifulSoup(htmlData)

	trs  = soup.table.tbody.find_all("tr")
	

	if len(trs) <1:
		return

	for tr in trs:
		tds = tr.find_all("td")
		
		scode = str(tds[1].a.string)
		bmoney = tds[4].string
		smoney = tds[5].string
		
		# # 获取历史数据
		# generateHistory(scode, 1)
		# continue 

		if bmoney[-1] == '万':
			bmoney = bmoney[:-1]
		else:
			bmoney = float(bmoney[:-1])*10000

		if smoney[-1] == '万':
			smoney = smoney[:-1]
		else:
			smoney = float(smoney[:-1])*10000

		
		tdate = datetime.datetime.strptime(currdate,'%Y-%m-%d').date()
		tdatestr = datetime.datetime.strftime(tdate,'%Y%m%d')
		
		
		exchangeType = 1  #交易所类型：0 深圳  1 上证
		# 1、深圳创业板股票的代码是：300XXX 的股票
		# 2、而深圳中小板股票的代码是：002XXX 开头的股票
		# 3、上海主板的股票代码是：60XXXX 开头的股票
		# 4、深圳主板的股票代码是：000XXX 开头的股票

		if (int)(scode[:3]) < 600:
			exchangeType = 0

		rzrqb = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,bmoney)
		rzrqs = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,smoney)
		# print rzrqb
		# print rzrqs
		
		appendFile(currdate, "89", rzrqb)
		appendFile(currdate, "90", rzrqs)
		
		
	generateDataFile(currdate,page+1) 
		
	
def main():
	

	reload(sys) 
	sys.setdefaultencoding('utf8')

	
	currdate = datetime.datetime.now().strftime("%Y-%m-%d")
	currdate = '2016-07-29'
	generateDataFile(currdate, 10)


	



main()

