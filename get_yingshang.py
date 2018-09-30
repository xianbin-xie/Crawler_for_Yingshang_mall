
# coding: utf-8

# In[ ]:


# Author Morning67373 xianbin.xie@tum.de
# Created on 30-09-2018
# Created by Python 3



import requests
import csv
import re
from bs4 import BeautifulSoup
import time

# 请在这这填入城市的代码和每个城市的页数 比如上海是309，北京是301，不清楚代码的去赢商网上看看url
city_num = '309'
city_name = 'shanghai'
page = 19

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Upgrade-Insecure-Requests': '1'
}
cookies = {
    '_ga': 'GA1.2.1581249721.1533695488', 
    'Hm_lvt_f48055ef4cefec1b8213086004a7b78d': '1535521842,1535607727,1537939299',
    '_gid': 'GA1.2.188514725.1538104948',
    'Hm_lpvt_f48055ef4cefec1b8213086004a7b78d': '1538106046'
}


def get_task_list(url):
    task_list = []
    
    try:
        res = requests.get(url, headers = headers, cookies = cookies)
        soup = BeautifulSoup(res.text, 'lxml')

        for l in soup.find_all(class_ = 'fl l-name-h3'):
            item = {}
            item['title'] = l.a['title']
            item['url'] = l.a['href']
            task_list.append(item)


        return task_list
    
    except Exception as e:
        print(e)
        return []

def get_detail(url):
    mall = {}
    
    try:
        res = requests.get(url, headers =headers, cookies = cookies)
        soup = BeautifulSoup(res.text, 'lxml')

        mall['url'] = url
        mall['name'] = soup.find_all(class_ = 'd-brand-tit')[0].contents[0]
        mall['开业状态'] = soup.find_all(class_ = 'd-inf-tit')[0].contents[0]           # 开业状态
        mall['招商状态'] = soup.find_all(class_ = 'd-inf-tit')[1].contents[0]       # 招商状态

        # 项目类型、开业时间、商业建筑面积、建筑楼层、连锁项目、所在城市、项目地址
        for item in soup.find_all(class_ = 'd-inf-status')[0].find_all('li'):
            mall[item.find_all('span')[0].contents[0]] = item.find_all('span')[1].contents[0]

        mall['更新时间'] = soup.find_all(class_ = 'd-update-time')[0].contents[0]

        if len(soup.find_all(class_ = 'd-property-value')) > 0:
            mall['开发商'] = soup.find_all(class_ = 'd-property-value')[0].contents[0]
            mall['开发商上市'] = soup.find_all(class_ = 'd-property-value')[1].contents[0]

        # 项目简介、硬件设施、开发商简介
        i = 0
        for item in soup.find_all(class_ = 'd-con-warp p24')[2].find_all(class_ = 'd-sub-tit'):
            if item.contents[0] != '开发商属性':
                mall[item.contents[0]] = str(soup.find_all(class_ = 'd-con-warp p24')[2].find_all(class_ = 'd-show')[i].find_all('p'))
                i = i + 1

        return mall
    
    except Exception as e:
        print(e)
        return {}


# 获取任务列表
task_list_all = []
for p in range(page):
    url = 'http://bizsearch.winshangdata.com/xiangmu/s' + city_num + '-c0-t0-r0-g0-x0-d0-z0-n0-m0-l0-q0-b0-y0-pn' + str(p+1) + '.html'
    print(url)
    
    task_list = get_task_list(url = url)
    
    if len(task_list) > 0:
        for item in task_list:
            task_list_all.append(item)
    
    else:
        time.sleep(5)
        task_list = get_task_list(url = url)
        for item in task_list:
            task_list_all.append(item)

# 储存任务列表
heading = ['title', 'url']
with open('task_list' + city_name + '.csv', 'w', newline = '') as f:
    f_writer = csv.DictWriter(f, heading)
#     f_writer.writeheader()
    f_writer.writerows(task_list_all)

    
# 获取详细页面
malls = []
for task in task_list_all:
    url = task['url']
    print(url)
    
    mall = get_detail(url)
    if len(mall) > 0:
        malls.append(mall)
    else:
        time.sleep(5)
        malls.append(get_detail(url))

# 储存详细信息
keys = ['url', 'name', '开业状态', '招商状态', '项目类型', '开业时间', '商业建筑面积', '商业楼层', '连锁项目', '所在城市', '项目地址', '更新时间', '开发商', '开发商上市', '项目简介', '硬件设施', '开发商简介']
with open('mall_' + city_name + '.csv', 'w', newline = '', encoding = 'utf-8') as f:
    f_writer = csv.DictWriter(f, keys)
    f_writer.writeheader()
    f_writer.writerows(malls)

