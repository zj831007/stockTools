# -*- coding: utf-8 -*-
# 抓取机构调研数据
# @Author: justin
# @Date:   2016-07-25 09:31:59
# @Last Modified by:   Jian Zhang
# @Last Modified time: 2016-08-01 18:23:11
# http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=50&page=2&js=&param=&sortRule=-1&sortType=0&rt=48983168
# 

import urllib2
import json
import datetime,time
import os
import codecs

def getLHBdata(startDateTime="2016-07-21",endDateTime="2016-07-22",pageNum=1, pageSize=50):
	try:
		url = "http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=%s&page=%s&js=&param=&sortRule=-1&sortType=0&rt=48983168" % (pageSize,pageNum)

		print "url: %s" % (url)
		response = urllib2.urlopen(url, timeout = 1000)
		html = response.read()
		response.close()

		html = unicode(html, "gbk").encode("utf8")
		
		decoded = json.loads(html)
		

		return decoded

	except urllib2.URLError as e:
		print e.reason


#
# datestr  日期字符串
# datano   数据编号 3 机构净买
# content  
#		 
def  appendFile(datestr, datano,content):
	# datestr = "history"
	filepath = "data/JGDY/%s_%s.txt" %(datestr, datano)

	f=open(filepath,'a')
	
	f.write(content)

	f.write('\n')
	f.close()


def generateDataFile(startDateTime, endDateTime,pageNum, pageSize):
	# 只取前5页
	if pageNum == 3:
		return

	jsonData = getLHBdata(startDateTime, endDateTime,pageNum, pageSize);  

	print jsonData['success']
	if jsonData != None and jsonData['success'] == True:
		tableData = jsonData['data']
		
		
		totalPage =  jsonData['pages']
		print "totalPage:%s, pageNum:%s" %(totalPage, pageNum)

		for row in tableData:
			
			scode = row['SCode'];
			orgSum = row['OrgSum'];
			startDate = row['StartDate'];
			tdate = datetime.datetime.strptime(startDate,'%Y-%m-%d').date()
			tdatestr = datetime.datetime.strftime(tdate,'%Y%m%d')

			

			exchangeType = 1  #交易所类型：0 深圳  1 上证
			# 1、深圳创业板股票的代码是：300XXX 的股票
			# 2、而深圳中小板股票的代码是：002XXX 开头的股票
			# 3、上海主板的股票代码是：60XXXX 开头的股票
			# 4、深圳主板的股票代码是：000XXX 开头的股票

			if (int)(scode[:3]) < 600:
				exchangeType = 0
			

			jgdy = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,orgSum)
			
			
			currdate = datetime.datetime.now().strftime("%Y%m%d")

			appendFile(currdate, "95", jgdy)
			

		# iterator 
		if pageNum< totalPage:
			pageNum+=1
			generateDataFile(startDateTime, endDateTime,pageNum, pageSize)

def main():
	
	daybefore = 180 # 几天前
	currdate = datetime.datetime.now().strftime("%Y-%m-%d")

	startDateTime="2016-01-01"
	endDateTime="2016-07-24"	
	
	beforedate = (datetime.datetime.now() - datetime.timedelta(days=daybefore)).strftime("%Y-%m-%d")		

	generateDataFile(beforedate, currdate, 1, 50)
	# generateDataFile(currdate, currdate, 1, 50)

main()




