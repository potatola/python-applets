# coding: UTF-8

import urllib
import urllib2
import re
import csv
import json
import time

pattern = re.compile(r'.*observe24h_data = ([^;]*);')
pattern_pressure = re.compile(r'.*hours_airpressure = ([^;]*);')

def get_weather_data(loc_num):
    print "Try fetch weather data from the website..."
    while True:
        try:
            url = 'http://www.weather.com.cn/weather/10101'+loc_num+'00.shtml'
            req_header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            req_timeout = 5
            req = urllib2.Request(url,None,req_header)
            web_file = urllib2.urlopen(req,None,req_timeout)

            #web_file = urllib.urlopen('http://www.weather.com.cn/weather/10101'+loc_num+'00.shtml')
            web_content = web_file.readlines()
            
            for content in web_content:
                #print content
                match = pattern.match(content)
                if match:
                    return match.groups()[0]
            
            # f = open("data.txt", 'wb')
            # for l in web_content:
                # f.write(l)
            # f.close()
            # exit()
            print "No data matched, retry!"
            time.sleep(3)
            
        except Exception, e:
            print "Exception, retry!"
            time.sleep(1)
    

def get_pressure_data():
    while True:
        try:
            print "Try fetch pressure data from the website..."
            web_file = urllib.urlopen('http://www.nmc.cn/publish/forecast/ABJ/beijing.html#fragment-1#userconsent##userconsent#')
            web_content = web_file.readlines()
            
            for content in web_content:
                match = pattern_pressure.match(content)
                if match:
                    res = match.groups()[0]
                    res = res.replace(',,', ',0,').replace('[,', '[0,')
                    return res
            
            print "No data matched, retry!"
            time.sleep(1)
            
        except:
            print "Exception, retry!"
            time.sleep(1)
                
def capture_location(loc_num, pressure_data):
    print "Dealing location with number: ", loc_num
    weather_data = get_weather_data(loc_num)
    dt = json.loads(weather_data)
    curr_time = dt['od']['od0']
    location = dt['od']['od1']

    pr = json.loads(pressure_data)

    i_pr = reversed(pr)

    with open(curr_time + '_' + loc_num + '.csv', 'wb') as f:
        table_title = [u'时间', 'AQI', u'温度', u'相对湿度', u'降水', u'风向', u'风力', '23', u'气压']
        table_title = [t.encode("gb2312") for t in table_title]
        writer = csv.writer(f)
        writer.writerow(table_title)

        dt['od']['od2'].pop()
        for log in dt['od']['od2']:
            writer.writerow([log['od21'], log['od28'], log['od22'], log['od27'], log['od26'], log['od24'].encode("gb2312"), log['od25'], log['od23'], next(i_pr)])
            

pressure_data = get_pressure_data()
for i in range(1, 16):
    loc_num = "%0.2d" % i
    capture_location(loc_num, pressure_data)