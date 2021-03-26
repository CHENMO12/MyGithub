#!/usr/bin/python3.8
# @Time : 2021/03/24 9:05
# @Author: Huizi
import requests
import json
import time
import datetime

t = time.time()
# print (int(t))                  #秒级时间戳
t = int(round(t * 1000))  # 毫秒级时间戳

url = "http://10.6.14.3:12581/topic/sendTopicMessage.do"

data = {
    "topic": "RUN_DATA_TOPIC",
    "key": "key",
    "tag": "154_1_51091_11481",
    "messageBody": '{"session_id":"FF00000016C0","from_cluster":"10.254.82.27:35861:%d","general_message":{"dataMode":0,"packet":null,"packetStart":null,"source":0,"developerID":"51091","msgId":null,"macAddress":"FF00000016C0","command":"0105","sendTo":null,"deviceType":154,"deviceSubType":1,"deviceBrand":null,"dataVersion":1,"packetSequence":null,"direction":null,"bussinessType":null,"data":{"Base_Null_Value_Effluent":"2400","deviceId":1321312312552,"Base_Null_String_UserID":"3131521135","productId":11481}}}'% t
}
headers = {"Content-Type": "application/json;charset=UTF-8"}

a = requests.post(url=url, data=json.dumps(data), headers=headers)
print(data)
print(a.text)
