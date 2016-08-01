# -*- coding: utf-8 -*-
# @Author: Jian Zhang
# @Date:   2016-07-30 11:30:07  股权质押
# @Last Modified by:   Jian Zhang
# @Last Modified time: 2016-08-01 17:56:46

import urllib2
import json
import datetime,time
import os
import codecs
import re
import HTMLParser
import sys
from bs4 import BeautifulSoup



def getLHBdata(currdate, page):
	try:
		url = "http://data.eastmoney.com/Notice/Noticelist.aspx?type=6&market=all&date=%s&page=%s" % (currdate,page)

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
	# datestr = "history"
	filepath = "data/GQZY/%s_%s.txt" %(datestr, datano)

	f=open(filepath,'a')
	
	f.write(content)

	f.write('\n')
	f.close()

##

def generateDataFile(currdate, page):

	htmlData = getLHBdata(currdate,page);  

	soup = BeautifulSoup(htmlData)
	trs  = soup.table.tbody.find_all("tr")
	
	
	#质押 解除质押 质押解除 解除股份质押 重新质押  再质押 
	for tr in trs:
		tds = tr.find_all("td")

		if len(tds) <3:
			return


		codek = str(tds[0].a.string)
		broad = str(tds[3].a.string)
		broaddate = tds[5].string
		
		# 3次过滤
		zyStatus = 0

		if broad.find('质押') != -1:
			zyStatus = 1
		if broad.find('解除') != -1:
			zyStatus = -1
		if broad.find('重新质押') !=-1 or broad.find('再质押') != -1:
			zyStatus = 1
		
		

		tdate = datetime.datetime.strptime(broaddate,'%Y-%m-%d').date()
		tdatestr = datetime.datetime.strftime(tdate,'%Y%m%d')
		

		exchangeType = 1  #交易所类型：0 深圳  1 上证
		# 1、深圳创业板股票的代码是：300XXX 的股票
		# 2、而深圳中小板股票的代码是：002XXX 开头的股票
		# 3、上海主板的股票代码是：60XXXX 开头的股票
		# 4、深圳主板的股票代码是：000XXX 开头的股票

		if (int)(codek[:3]) < 600:
			exchangeType = 0

		if zyStatus!= 0:

			dzjy = "%s|%s|%s|%s" %(exchangeType,codek,tdatestr,zyStatus)
			appendFile(currdate, "87", dzjy)
			# print dzjy

	generateDataFile(currdate,page+1)
		
		
	
def main():
	
	reload(sys) 
	sys.setdefaultencoding('utf8')

	currdate = datetime.datetime.now().strftime("%Y-%m-%d")
	# currdate = '2016-07-28'

	# for day in xrange(1,100):
	# 	beforedate = (datetime.datetime.now() - datetime.timedelta(days=day)).strftime("%Y-%m-%d")
	# 	generateDataFile(beforedate, 1)

	generateDataFile(currdate, 1)



main()

