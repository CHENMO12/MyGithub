#!/usr/bin/python3.7
# @Time : 2020/8/4 0004 14:33
from lxml import etree
import requests
import json
import time
import datetime
import pymysql


# current_time = datetime.datetime.now().strftime("%Y-%m-%d")
url = "https://www.qiushibaike.com/hot"
header = {"Content-Type": "application/json;charset=UTF-8",
          }

html = requests.get(url=url, headers=header).text  # 返回html
res = etree.HTML(html)
cont = res.xpath('//div[@class="content"]/span/text()') #定位html
# mark = res.xpath('//div[@class="main-text"]')
for _ in cont:
    if _ != "查看全文":
        print(_)
        with open('./xiaohua.txt', 'a', encoding='utf-8', errors='ignore') as f:
            f.write(_+"\n")

