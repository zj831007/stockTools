# -*- coding: utf-8 -*-
# 敢死队
# @Author: justin
# @Date:   2016-07-25 09:31:59
# @Last Modified by:   Jian Zhang
# @Last Modified time: 2016-07-30 19:38:12
# http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/YYBJXMX/GetYYBJXMX?tkn=eastmoney&salesCode=80154308&tdir=&dayNum=&startDateTime=2015-07-30&endDateTime=2016-07-30&sortfield=&sortdirec=1&pageNum=2&pageSize=50&cfg=yybjymx

import urllib2
import json
import datetime,time
import os
import re
import codecs
import sys

def getLHBdata(salesCode="80154308", startDateTime="2016-07-21",endDateTime="2016-07-22",pageNum=1, pageSize=50):
	try:
		url = "http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/YYBJXMX/GetYYBJXMX?tkn=eastmoney&salesCode=%s&tdir=&dayNum=&startDateTime=%s&endDateTime=%s&sortfield=&sortdirec=1&pageNum=%s&pageSize=%s&cfg=yybjymx" % (salesCode,startDateTime,endDateTime,pageNum, pageSize)
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
	filepath = "data/GSD/%s_%s.txt" %(datestr, datano)

	f=open(filepath,'a')
	f.write(content)
	f.write('\n')
	f.close()


def generateDataFile(salesCode, startDateTime, endDateTime,pageNum, pageSize):
	
	jsonData = getLHBdata(salesCode, startDateTime, endDateTime,pageNum, pageSize);  

	if jsonData != None and jsonData['Status'] == 0:
		tableData = jsonData['Data']
		tableObj =  tableData[0]
		
		totalPage =  tableObj['TotalPage']
		print "totalPage:%s, pageNum:%s" %(totalPage, pageNum)

		for row in tableObj['Data']:
			rowList = row.split("|")

			scode = rowList[10]
			smoney = rowList[15]
			bmoney = rowList[0]
			tdate = datetime.datetime.strptime(rowList[22],'%Y-%m-%d').date()
			tdatestr = datetime.datetime.strftime(tdate,'%Y%m%d')
			jm = float(rowList[17])   #净买
			
			salesType = salesCode;
			if  jm<0 :
				salesType = "-"+salesCode.strip()
			

			# 去掉连续三个交易日内数据
			ctypedesc = rowList[25];
			# print ctypedesc.find("连续三个交易日")

			if ctypedesc.find("连续三个交易日")  != -1:
				continue

			
			

			exchangeType = 1  #交易所类型：0 深圳  1 上证
			# 1、深圳创业板股票的代码是：300XXX 的股票
			# 2、而深圳中小板股票的代码是：002XXX 开头的股票
			# 3、上海主板的股票代码是：60XXXX 开头的股票
			# 4、深圳主板的股票代码是：000XXX 开头的股票

			if (int)(scode[:3]) < 600:
				exchangeType = 0
			

			gsd = "%s|%s|%s|%s" %(exchangeType,scode,tdatestr,salesType)
			
			appendFile(tdatestr, "91", gsd)
			

		# iterator 
		if pageNum< totalPage:
			pageNum+=1
			generateDataFile(salesCode, startDateTime, endDateTime,pageNum, pageSize)

def main():
	reload(sys) 
	sys.setdefaultencoding('utf8')

	daybefore = 1 # 几天前
	currdate = datetime.datetime.now().strftime("%Y-%m-%d")

	startDateTime="2016-01-01"
	endDateTime="2016-07-30"	
	
	beforedate = (datetime.datetime.now() - datetime.timedelta(days=daybefore)).strftime("%Y-%m-%d")		

	'''
	国金证券股份有限公司上海奉贤区金碧路证券营业部  80436592
	华泰证券股份有限公司深圳益田路荣超商务中心证券营业部 80154611
	中国中投证券有限责任公司无锡清扬路证券营业部 80174625
	华泰证券股份有限公司厦门厦禾路证券营业部 80190854
	国泰君安证券股份有限公司上海福山路证券营业部 80033894
	华泰证券股份有限公司上海武定路证券营业部 80094766
	中信证券股份有限公司上海溧阳路证券营业部 80032107
	国金证券股份有限公司上海互联网证券分公司 80095368
	申万宏源证券有限公司上海闵行区东川路证券营业部 80152193
	平安证券有限责任公司深圳深南东路罗湖商务中心证券营业部 80141030
	光大证券股份有限公司宁波中山西路证券营业部 80119604
	华泰证券股份有限公司上海长宁区仙霞路证券营业部 80124572
	中信证券股份有限公司杭州四季路证券营业部 80086086
	中信证券股份有限公司上海淮海中路证券营业部  80065939
	华泰证券股份有限公司浙江分公司 80422837
	光大证券股份有限公司佛山绿景路证券营业部 80144552
	华泰证券股份有限公司上海共和新路证券营业部 80154448
	海通证券股份有限公司北京中关村南大街证券营业部 80034110
	华泰证券股份有限公司成都南一环路第二证券营业部  80090067
	中信证券股份有限公司上海漕溪北路证券营业部 80152115
	国信证券股份有限公司深圳泰然九路证券营业部 80096570
	'''
	salesCodeList = ['80436592','80154611','80174625','80190854','80033894','80094766',
	'80032107','80095368','80152193','80141030','80119604','80124572','80086086','80065939',
	'80422837','80144552','80154448','80034110','80090067','80152115','80096570']

	# salesCodeList = ['80436592']
	for salesCode  in salesCodeList:
		# generateDataFile(salesCode, startDateTime, endDateTime, 1, 50)
		generateDataFile(salesCode, currdate, currdate, 1, 50)

	

main()




