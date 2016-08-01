# -*- coding: utf-8 -*-
# 机构每日买卖数据
# @Author: justin
# @Date:   2016-07-25 09:31:59
# @Last Modified by:   Jian Zhang
# @Last Modified time: 2016-07-30 17:02:12
# http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBJGTJ/GetHBJGTJ?tkn=eastmoney&code=&mkt=0&dateNum=&startDateTime=2016-07-29&endDateTime=2016-07-29&sortfield=PBuy&sortdirec=1&pageNum=1&pageSize=50&cfg=lhbjgtj

import urllib2
import json
import datetime,time
import os
import re
import sys

def getLHBdata(startDateTime="2016-07-21",endDateTime="2016-07-22",pageNum=1, pageSize=50):
	try:
		url = "http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBJGTJ/GetHBJGTJ?tkn=eastmoney&code=&mkt=0&dateNum=&startDateTime=%s&endDateTime=%s&sortfield=PBuy&sortdirec=1&pageNum=%s&pageSize=%s&cfg=lhbjgtj" % (startDateTime,endDateTime,pageNum, pageSize)
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
	filepath = "data/JGBS/%s_%s.txt" %(datestr, datano)

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

			scode = rowList[9]
			smoney = rowList[16]
			bmoney = rowList[22]
			tdate = datetime.datetime.strptime(rowList[15],'%Y-%m-%d').date()
			tdatestr = datetime.datetime.strftime(tdate,'%Y%m%d')
			
			# 去掉连续三个交易日内数据
			ctypedesc = rowList[29];
			

			if ctypedesc.find("连续三个交易日")  != -1:
				# print ctypedesc
				continue


			exchangeType = 1  #交易所类型：0 深圳  1 上证
			# 1、深圳创业板股票的代码是：300XXX 的股票
			# 2、而深圳中小板股票的代码是：002XXX 开头的股票
			# 3、上海主板的股票代码是：60XXXX 开头的股票
			# 4、深圳主板的股票代码是：000XXX 开头的股票

			if (int)(scode[:3]) < 600:
				exchangeType = 0
			

			jgbb = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,bmoney)
			jgbs = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,smoney)
			
			

			appendFile(tdatestr, "97", jgbb)
			appendFile(tdatestr, "98", jgbs)
			

		# iterator 
		if pageNum< totalPage:
			pageNum+=1
			generateDataFile(startDateTime, endDateTime,pageNum, pageSize)

def main():
	reload(sys) 
	sys.setdefaultencoding('utf8')

	daybefore = 1 # 几天前
	currdate = datetime.datetime.now().strftime("%Y-%m-%d")

	startDateTime="2016-01-01"
	endDateTime="2016-07-30"	
	
	beforedate = (datetime.datetime.now() - datetime.timedelta(days=daybefore)).strftime("%Y-%m-%d")		

	# generateDataFile(startDateTime, endDateTime, 1, 50)
	generateDataFile(currdate, currdate, 1, 50)

main()




