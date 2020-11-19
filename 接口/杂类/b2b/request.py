import requests
import json

url = "http://192.168.1.93:3003/admin/login"
data = {"username": "100272",
        "password": "HGBnGUVR1HvaWkkniwVMvg==",
        "autoLogin": 1}
headers = {"Content-Type": "application/json;charset=UTF-8"}

a = requests.post(url=url, data=json.dumps(data), headers=headers)
print(a.text)
