# -*- coding: utf-8 -*-
# 抓去龙虎榜数据
# @Author: justin
# @Date:   2016-07-25 09:31:59
# @Last Modified by:   justin
# @Last Modified time: 2016-07-25 18:36:50
# http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?tkn=eastmoney&mkt=0&dateNum=&startDateTime=2016-06-13&endDateTime=2016-07-22&sortRule=1&sortColumn=&pageNum=1&pageSize=1&cfg=lhbggdrtj

import urllib2
import json
import datetime,time
import os
import re

def getLHBdata(startDateTime="2016-07-21",endDateTime="2016-07-22",pageNum=1, pageSize=50):
	try:
		url = "http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?tkn=eastmoney&mkt=0&dateNum=&startDateTime=%s&endDateTime=%s&sortRule=1&sortColumn=&pageNum=%s&pageSize=%d&cfg=lhbggdrtj" % (startDateTime,endDateTime,pageNum, pageSize)
		print "url: %s" % (url)
		response = urllib2.urlopen(url, timeout = 1000)
		return json.load(response)
	except urllib2.URLError as e:
		print e.reason


#
# datestr  日期字符串
# datano   数据编号 92 龙虎买 93 龙虎卖
# content  
#		 
def  appendFile(datestr, datano,content):
	# datestr = "history"
	filepath = "LHB/%s_%s.txt" %(datestr, datano)

	f=open(filepath,'a')
	f.write(content)
	f.write('\n')
	f.close()


def generateDataFile(startDateTime, endDateTime,pageNum, pageSize):
	
	jsonData = getLHBdata(startDateTime, endDateTime,pageNum, pageSize);  

	if jsonData != None and jsonData['Status'] == 0:
		tableData = jsonData['Data']
		tableObj =  tableData[0]
		
		totalPage =  tableObj['TotalPage']
		print "totalPage:%s, pageNum:%s" %(totalPage, pageNum)

		for row in tableObj['Data']:
			rowList = row.split("|")

			scode = rowList[0]
			smoney = rowList[10]
			bmoney = rowList[11]
			tdate = datetime.datetime.strptime(rowList[13],'%Y-%m-%d').date()
			tdatestr = datetime.datetime.strftime(tdate,'%Y%m%d')
			jm = rowList[5]   #净买
			dp = rowList[43]  #成功率
			dprate = re.search(r"(\d*)%",dp).group(1);
			

			exchangeType = 1  #交易所类型：0 深圳  1 上证
			# 1、深圳创业板股票的代码是：300XXX 的股票
			# 2、而深圳中小板股票的代码是：002XXX 开头的股票
			# 3、上海主板的股票代码是：60XXXX 开头的股票
			# 4、深圳主板的股票代码是：000XXX 开头的股票

			if (int)(scode[:3]) < 600:
				exchangeType = 0
			

			lhbb = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,bmoney)
			lhbs = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,smoney)
			lhbdp = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,dprate)

			appendFile(tdatestr, "92", lhbb)
			appendFile(tdatestr, "93", lhbs)
			appendFile(tdatestr,"94",lhbdp)

		# iterator 
		if pageNum< totalPage:
			pageNum+=1
			generateDataFile(startDateTime, endDateTime,pageNum, pageSize)

def main():
	
	daybefore = 1 # 几天前
	currdate = datetime.datetime.now().strftime("%Y-%m-%d")

	startDateTime="2016-01-01"
	endDateTime="2016-07-24"	
	
	beforedate = (datetime.datetime.now() - datetime.timedelta(days=daybefore)).strftime("%Y-%m-%d")		

	# generateDataFile(startDateTime, endDateTime, 1, 50)
	generateDataFile(currdate, currdate, 1, 50)

main()




