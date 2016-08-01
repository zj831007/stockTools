# -*- coding: utf-8 -*-
# @Author: Jian Zhang
# @Date:   2016-07-30 11:30:07  大宗交易
# @Last Modified by:   Jian Zhang
# @Last Modified time: 2016-08-01 18:12:02

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
		url = "http://data.10jqka.com.cn/market/dzjy/field/enddate/order/desc/page/%s/ajax/1/" % (page)

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
	filepath = "data/DZJY/%s_%s.txt" %(datestr, datano)

	f=open(filepath,'a')
	
	f.write(content)

	f.write('\n')
	f.close()

##

def generateDataFile(currdate, page):
	global global_dic

	htmlData = getLHBdata(page);  

	soup = BeautifulSoup(htmlData)

	trs  = soup.table.tbody.find_all("tr")
	
	finish_data = False;

	for tr in trs:
		tds = tr.find_all("td")
		tradeDate = str(tds[1].string)
		scode = str(tds[2].string)
		price = tds[5].string
		num = tds[6].string
		currPrice = tds[4].string
		

		if currdate != tradeDate:
			# 如果今天数据已经取完，退出
			finish_data = True;
			break

		if not global_dic.has_key(tradeDate):
			global_dic[tradeDate] = {}

		if not global_dic[tradeDate].has_key(scode):
			global_dic[tradeDate][scode]={}
			
		totalMoney = float(price) * float(num)

		global_dic[tradeDate][scode]['scode'] = scode

		if not global_dic[tradeDate][scode].has_key('money'):
			global_dic[tradeDate][scode]['money'] = totalMoney
		else:
			global_dic[tradeDate][scode]['money'] += totalMoney

		global_dic[tradeDate][scode]['op'] = 1
		if float(price) < float(currPrice):
			global_dic[tradeDate][scode]['op'] = -1

	

	# if page < 39:
	# 	generateDataFile(currdate,page+1)
		
	if finish_data == False:
		generateDataFile(currdate,page+1)
	 
		
	
global_dic = {}
def main():
	

	reload(sys) 
	sys.setdefaultencoding('utf8')

	
	currdate = datetime.datetime.now().strftime("%Y-%m-%d")
	# currdate = '2016-07-29'
	generateDataFile(currdate, 1)


	

	for (dzjyDate, items) in global_dic.items():
		
		for (codek,item) in items.items():
			
			money = float(item['money'])* int(item['op'])
			

			tdate = datetime.datetime.strptime(dzjyDate,'%Y-%m-%d').date()
			tdatestr = datetime.datetime.strftime(tdate,'%Y%m%d')
			

			exchangeType = 1  #交易所类型：0 深圳  1 上证
			# 1、深圳创业板股票的代码是：300XXX 的股票
			# 2、而深圳中小板股票的代码是：002XXX 开头的股票
			# 3、上海主板的股票代码是：60XXXX 开头的股票
			# 4、深圳主板的股票代码是：000XXX 开头的股票

			if (int)(codek[:3]) < 600:
				exchangeType = 0

			dzjy = "%s|%s|%s|%s" %(exchangeType,codek,tdatestr,money)
			appendFile(currdate, "99", dzjy)
			# print dzjy


main()

