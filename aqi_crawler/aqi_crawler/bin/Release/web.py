# coding: UTF-8

import sys
sys.path.append('C:\\Python27\\lib\\site-package')
sys.path.append('C:\\Python27\\lib')
import urllib2
import re
import csv
import os

ab2name = {
"奥体中心":"朝阳奥体中心",
"八达岭":"京西北区域点",
"北部新区":"海淀北部新区",
"昌平":"昌平镇",
"大兴":"大兴黄村镇",
"定陵":"定陵对照点",
"东高村":"京东区域点",
"东四":"东城东四",
"东四环":"东四环交通点",
"房山":"房山良乡",
"丰台花园":"丰台花园",
"古城":"石景山古城",
"官园":"西城官园",
"怀柔":"怀柔镇",
"琉璃河":"京西南区域点",
"门头沟":"门头沟龙泉镇",
"密云":"密云镇",
"密云水库":"京东北区域点",
"南三环":"南三环交通点",
"农展馆":"朝阳农展馆",
"平谷":"平谷镇",
"前门":"前门交通点",
"顺义":"顺义新城",
"天坛":"东城天坛",
"通州":"通州新城",
"万柳":"海淀万柳",
"万寿西宫":"西城万寿西宫",
"西直门北":"西直门交通点",
"延庆":"延庆镇",
"亦庄":"亦庄开发区",
"永定门内":"永定门交通点",
"永乐店":"京东南区域点",
"榆垡":"京南区域点",
"云岗":"丰台云岗",
"植物园":"海淀北京植物园"}

pattern = re.compile(r'.*"Station":"([^"]*)","Pollutant":"([^"]*)","Value":"([^"]*)".*"Avg24h":"([^"]*)"')

def get_web_data():
	# read POST body
	con = open('post_body.txt', 'rb').read()
	# send POST request
	req = urllib2.Request('http://zx.bjmemc.com.cn/DataService.svc', data=con, headers={'Content-type': 'application/soap+msbin1'})
	r = urllib2.urlopen(req)
	# post_res is the data
	post_res = r.read()
	post_res = post_res[118:-4]

	return post_res

def parse_table(post_res):
	# parse data, write result into .csv file

	res = {}

	log_time = post_res[24:40]
	print "successfully parsed pollution data, time :", log_time

	ftxt = open(log_time.replace(':', '.')+'_raw.txt','w')
	ftxt.write(post_res.encode("gb2312"))
	ftxt.close()

	lines = post_res.split("},{")
	#print len(lines)
	for l in lines:
		match = pattern.match(l)
		if match:
			if not match.groups()[0] in res:
				res[match.groups()[0]] = {}
			res[match.groups()[0]][match.groups()[1]] = match.groups()[2]
			if match.groups()[1] == 'PM2.5' or match.groups()[1] == 'PM10':
				res[match.groups()[0]][match.groups()[1]+' avg'] = match.groups()[3]

	writer = csv.writer(file(log_time.replace(':', '.')+'.csv', 'wb'))
	writer.writerow([log_time, "SO2", "CO", "NO2", "PM10", "PM10 avg", "PM2.5", "PM2.5 avg", "O3"])

	name2ab = {}
	for i in ab2name:
		name2ab[ab2name[i]] = i

	for i in res:
		row = [name2ab[i].encode("gb2312")]
		if "SO2" in res[i]:
			row.append(res[i]["SO2"])
		else:
			row.append(" ")
		if "CO" in res[i]:
			row.append(res[i]["CO"])
		else:
			row.append(" ")
		if "NO2" in res[i]:
			row.append(res[i]["NO2"])
		else:
			row.append(" ")
		if "PM10" in res[i]:
			row.append(res[i]["PM10"])
			row.append(res[i]["PM10 avg"])
		else:
			row.append(" ")
		if "PM2.5" in res[i]:
			row.append(res[i]["PM2.5"])
			row.append(res[i]["PM2.5 avg"])
		else:
			row.append(" ")
		if "O3" in res[i]:
			row.append(res[i]["O3"])
		else:
			row.append(" ")
		writer.writerow(row)
