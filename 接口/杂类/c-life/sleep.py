#!/usr/bin/python3.8
# @Time : 2021/03/24 10:54
# @Author: Huizi
# !/usr/bin/python3.8
# @Time : 2021/03/24 9:05
# @Author: Huizi
import requests
import json

import time

NowTime = time.localtime()  # 获取当前时间
nowtime = time.strftime("%Y-%m-%d", NowTime)
print(nowtime)
url = "https://itest.clife.net/v1/web/edubehavior/sleep/save"

data = {
    "deviceNo": "00232sa2",
    "studentId": "18916561256449",
    "date": nowtime,
    "sleepDuration": 70,
    "wakeDuration": "10",
    "wakeNumber": "1",
    "source": "1"
}
headers = {"Content-Type": "application/json;charset=UTF-8",}
a = requests.post(url=url, data=json.dumps(data), headers=headers,verify=True)
print(data)
print(a.text)
