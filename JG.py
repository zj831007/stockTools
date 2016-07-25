# -*- coding: utf-8 -*-
# 抓取机构数据
# @Author: justin
# @Date:   2016-07-25 09:31:59
# @Last Modified by:   justin
# @Last Modified time: 2016-07-25 16:56:39
# http://data.eastmoney.com/DataCenter_V3/stock2016/JgStatistic/pagesize=50,page=1,sortRule=-1,sortType=,startDate=2016-06-25,endDate=2016-07-25,gpfw=0,js=var%20data_tab_3.html?rt=24490444
# http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBJGXWZZ/GetLHBJGXWZZ?tkn=eastmoney&code=&mkt=1&dateNum=&startDateTime=2016-06-25&endDateTime=2016-07-25&sortfield=&sortdirec=1&pageNum=1&pageSize=50&cfg=lhbjgxwzz

import urllib2
import json
import datetime,time
import os
import codecs

def getLHBdata(startDateTime="2016-07-21",endDateTime="2016-07-22",pageNum=1, pageSize=50):
	try:
		url = "http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBJGXWZZ/GetLHBJGXWZZ?tkn=eastmoney&code=&mkt=0&dateNum=&startDateTime=%s&endDateTime=%s&sortfield=&sortdirec=1&pageNum=%s&pageSize=%s&cfg=lhbjgxwzz" % (startDateTime,endDateTime,pageNum, pageSize)

		print "url: %s" % (url)
		response = urllib2.urlopen(url, timeout = 1000)
		return json.load(response)
	except urllib2.URLError as e:
		print e.reason


#
# datestr  日期字符串
# datano   数据编号 3 机构净买
# content  
#		 
def  appendFile(datestr, datano,content):
	# datestr = "history"
	filepath = "JG/%s_%s.txt" %(datestr, datano)

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
			
			JGBMoney = float(rowList[6])/10000
			JGBCount = int(rowList[7])
			JGSMoney = float(rowList[8])/10000
			JGSCount = int(rowList[9])
			JGPBuy = float(rowList[10])/10000

			

			

			exchangeType = 1  #交易所类型：0 深圳  1 上证
			# 1、深圳创业板股票的代码是：300XXX 的股票
			# 2、而深圳中小板股票的代码是：002XXX 开头的股票
			# 3、上海主板的股票代码是：60XXXX 开头的股票
			# 4、深圳主板的股票代码是：000XXX 开头的股票

			if (int)(scode[:3]) < 600:
				exchangeType = 0
			

			lhbb = "JGBuy Count: "+str(JGBCount)+", JGBuy Money: "+str(JGBMoney)+", JGSell Count: "+str(JGSCount)+", JGSell Money: "+str(JGSMoney)
			
			content = str(exchangeType)+"|"+ str(scode) +"|"+ lhbb + "|" + str(JGPBuy)
			

			currdate = datetime.datetime.now().strftime("%Y%m%d")

			appendFile(currdate, "3", content)
			

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




