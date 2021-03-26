import requests
import json
import time

t = time.time()
# print (int(t))                  #秒级时间戳
t = int(round(t * 1000))  # 毫秒级时间戳

url = "http://10.6.14.3:12581/topic/sendTopicMessage.do"

data = {
    "topic": "RUN_DATA_TOPIC",
    "key": "key",
    "tag": "117_1_51091_8371",
    "messageBody": '{"session_id":"FF00000016C3","from_cluster":"10.104.142.167:35861: %d","general_message":{"dataMode":0,"packet":null,"packetStart":null,"source":0,"developerID":"51091","msgId":null,"macAddress":"FF00000016C3","command":"0005","sendTo":null,"deviceType":117,"deviceSubType":1,"deviceBrand":null,"dataVersion":2,"packetSequence":null,"direction":null,"bussinessType":null,"data":{"Base_Null_Status_Null":{"result":"NYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY","access":"Y","eyeImgId":"","statusType":1,"handImgId":"","temperature":"37.4 ℃","mouthImgId":"","authSign":"6d84d52ba0f4e84cc495372f6e676ea5","cardNo":"3131521132","robotResult":"UUY","token":"WR01060519120102"},"code":0,"productId":"8371","dataTimeStamp":1616641165182,"msgId":"dac84958-6649-4229-a8ea-289e3a8ab174","_user_id":"","deviceId":"1321312312556","record_time":%d,"errorMsg":""}}}' % (t,t)}
headers = {"Content-Type": "application/json;charset=UTF-8"}

a = requests.post(url=url, data=json.dumps(data), headers=headers)
print(data)
print(a.text)
