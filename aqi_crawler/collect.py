# coding: UTF-8

import re
import os 
import sys
import time
import csv

if len(sys.argv) == 2:
    root = sys.argv[1]
else:
    root = './'

locs = ['南三环','门头沟','云岗','农展馆','北部新区','官园','植物园','西直门北','定陵','八达岭','天坛','密云水库','奥体中心','东高村','房山','丰台花园','亦庄','东四环','昌平','怀柔','平谷','古城','万柳','榆垡','通州','永定门内','琉璃河','顺义','永乐店','前门','大兴','万寿西宫','延庆','密云','东四']
locs = [x.decode('utf-8').encode('gb2312') for x in locs]

pollutions = ['SO2','CO','NO2','PM10','PM10 avg','PM2.5','PM2.5 avg','O3']
cwriters = []
for p in pollutions:
    cwriter = csv.writer(open('output/'+p+'.csv', 'wb'))
    cwriter.writerow(['日期'.decode('utf-8').encode('gb2312'), '时间'.decode('utf-8').encode('gb2312')] + locs)
    cwriters += [cwriter]

for fn in os.listdir(root):
    if fn[-3:] != 'csv':
        continue
    #raw_input('pause:')
    ts = fn[:-4]
    if ts[-1] == '.':
        ts = ts[:-1]
    if ts.count('.') == 1:
        ts += '.0'
    ti = time.strptime(ts,'%Y-%m-%d %H.%M.%S')
    print time.strftime('%Y-%m-%d', ti), time.strftime('%H:%M:%S', ti)

    with open(os.path.join(root, fn), 'rb') as csvfile:
        creader = csv.reader(csvfile)
        creader.next()

        loc_val = {}
        pol_val = []
        for i in range(len(pollutions)):
            pol_val += [[]]
        for row in creader:
            loc_val[row[0]] = row[1:]

        for loc in locs:
            if loc in loc_val:
                val = loc_val[loc]
                while len(val) < 8:
                    val += ['']
                for i in range(8):
                    pol_val[i] += [val[i]]
            else:
                for i in range(8):
                    pol_val[i] += ['']

        for i in range(8):
            cw = cwriters[i]
            cw.writerow([time.strftime('%Y-%m-%d', ti), time.strftime('%H:%M:%S', ti)] + pol_val[i])