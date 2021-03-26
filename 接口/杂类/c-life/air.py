#!/usr/bin/python3.8
# @Time : 2021/03/24 18:06
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
    "tag": "7_17_51091_7567",
    "messageBody": '{"session_id":"FF00000001C4","from_cluster":"10.104.234.125:35861:%d","general_message":{"dataMode":0,"packet":null,"packetStart":null,"source":0,"developerID":"51091","msgId":null,"macAddress":"FF00000001C4","command":"0005","sendTo":null,"deviceType":7,"deviceSubType":17,"deviceBrand":null,"dataVersion":2,"packetSequence":null,"direction":null,"bussinessType":null,"data":{"Base_Inside_Value_Temp":22,"Base_Null_Value_WindSpeed":60,"productId":"7567","Base_Null_Mode_Null":0,"dataTimeStamp":%d,"Base_MinValue_Value_WindSpeed":60,"msgId":"294b0795-62eb-45d0-ae5e-0571702564f3","deviceId":153498,"Base_MaxValue_Value_WindSpeed":420,"CO2_Null_Value_Null":651,"Base_Null_Status_Null":1,"Base_Null_Status_ChildLock":0,"Base_Inside_Percent_Humidity":67,"PTC_Null_Status_Null":1,"PM25_Null_Value_Null":17,"record_time":%d}}}' % (
        t, t, t,)
}
headers = {"Content-Type": "application/json;charset=UTF-8"}

a = requests.post(url=url, data=json.dumps(data), headers=headers)
print(data)
print(a.text)
