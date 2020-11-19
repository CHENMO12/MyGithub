import requests
import json
import random
import hashlib


def str2_md5(dic):
    # 去掉空格
    string = json.dumps(dic).replace(': ', ':').replace(', ', ',')
    print(string)
    m = hashlib.md5()
    m.update(string.encode(encoding='utf-8'))
    return m.hexdigest()


url = "http://192.168.89.251:8080/equipmentAppAction!addEquipment.action"
data = {}
data['phoneNo']="partner26"
data['password']='123456'
data['areacode']='002-000-004'
data['nodename']='072202'
data['equipmentno']='072202'
data['type']= '0'
data['gateway']="001"
data['vi']='004003002001000'
# data['gatewaycode']='002-000-003-000'
data['key']=str2_md5(data)

print(str2_md5(data))
# # print(data)

response = requests.post(url=url, data=data).text
rp = json.loads(response)
print(rp)
