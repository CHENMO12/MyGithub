# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 17:31
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : upload_data.py

from socket import socket, AF_INET, SOCK_STREAM
from business_app._config.config import Config
import json
import datetime
import time
import uuid
import base64
import random
import os
import glob


# from djconfig import cons

class UploadByNetty(object):
    def __init__(self, deviceID,host):
        self.msgid = uuid.uuid4().__str__() + random.randint(1, 1000000).__str__()
        try:

            self.conn = socket(AF_INET, SOCK_STREAM)
            self.conn.connect((host, 9999))
        except ConnectionRefusedError as e:
            print('create socket connection failed: ' % e)
            exit(1)
        self.init(deviceID)

    def init(self, deviceID):
        self.devID = deviceID

        # 登录
        self.deviceLogin()
        # 心跳
        self.heartBeat()

    def sendMessage(self, message):
        sendMessage = json.dumps(message) + "$_"
        sendMessage = sendMessage.encode("utf-8")
        # print("sendMessage:", sendMessage)
        try:
            self.conn.send(sendMessage)
        except Exception as e:
            print('send msg faild:%s,msg content is：%s' % (e, sendMessage))
        ret = self.conn.recv(8192).decode("utf-8")
        # print("ret:", ret)

    def deviceLogin(self, deviceIP="192.168.1.108"):

        dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        loginMessage = {
            "datetime": dateTime,
            "cmdtype": "login",
            "data": {
                "msg": "login",
                "ip": deviceIP,
                "evState": 0,
                "hardwareVersion": "V400003001",
                "type": 0},
            "msgid": self.msgid,
            "equno": self.devID
        }
        self.sendMessage(loginMessage)

    def heartBeat(self, deviceIP="192.168.1.108"):
        currentTime = datetime.datetime.now()
        heartBeatMessage = {
            "msgid": self.msgid,
            "equno": self.devID,
            "data": {
                "id": deviceIP,
                "time": time.mktime(currentTime.timetuple())  # 时间戳
            },
            "datetime": currentTime.strftime("%Y-%m-%d %H:%M:%S"),
            "cmdtype": "deviceStatus"
        }
        self.sendMessage(heartBeatMessage)

    def reportData(self, pictureFile, img_time=None, xks=None, body_pictureFile=None):
        # 获取照片的base64编码
        fp = open(pictureFile, 'rb')
        faceFrame = base64.b64encode(fp.read()).decode("utf-8")
        fp.close()

        bodyFrame = ''
        if body_pictureFile is not None:
            fp = open(body_pictureFile, 'rb')
            bodyFrame = base64.b64encode(fp.read()).decode("utf-8")
            fp.close()
        # 构造数据

        self.currentTime = datetime.datetime.now()

        if img_time is None:
            img_time = self.currentTime.strftime("%Y-%m-%d %H:%M:%S")


        if xks:
            alarmId = str(uuid.uuid4()) + str(random.randint(1, 100000))
            reportDataMessage = {
                "msgid": self.msgid,
                "equno": self.devID,
                "data": {
                    "alarmId": alarmId,
                    "imageTime": img_time,
                    "personId": 0,
                    "gender": 0,
                    "age": 24,
                    "faceFrame": faceFrame,
                    "bodyFrame": faceFrame,
                    "resideTime": 10,
                    "capAngle": 0,
                    "arithmetic": 1,
                    "userStatus": 2,
                    "score": 1.6,
                    "trackNo": alarmId[:30],
                    "leaveTime": img_time,
                    "enterTime": img_time,
                    "isLeaveCap": 1,
                    "similarTrackNo": '2',
                },
                "datetime": img_time,
                "cmdtype": "reportdata"
            }
        else:
            reportDataMessage = {
                "msgid": self.msgid,
                "equno": self.devID,
                "data": {
                    "alarmId": str(uuid.uuid4()) + str(random.randint(1, 100000)),
                    "imageTime": img_time,
                    "personId": 0,
                    "gender": 1,
                    "age": 48,
                    "faceFrame": faceFrame,
                    "bodyFrame": bodyFrame,
                    "resideTime": 10,
                    "capAngle": 0,
                    "arithmetic": 1,
                    "userStatus": 0,
                    "score": 1.6,
                    "trackNo": str(random.randint(1, 100000))
                },
                "datetime": img_time,
                "cmdtype": "reportdata"
            }
        self.sendMessage(reportDataMessage)

        return img_time

    def upload_data(self, pictureFile,body_pictureFile=None, img_time=None, xks=None):
        return self.reportData(pictureFile, img_time=img_time, xks=xks, body_pictureFile=body_pictureFile)

    def run(self, picture=None):
        # upload = UploadByNetty('DJ93336222763018673843')
        # upload = UploadByNetty("DJ38a28cd90d80", "47.96.86.247")
        # day_count == 0 表示上传今天的数据，表示从第几天开始上传数据
        # pic_count 为每天需要上传的客流数 * 400
        if picture is None:
            WSI_MASK_PATH = 'F:\\模拟上传数据\\6000_picture'  # 存放图片的文件夹路径
            # picture = 'F:\接口自动化测试\\business_app\_api\image\\name1.jpg'  # 存放图片的文件夹路径
            # body_pictureFile = 'F:\\模拟上传数据\\name10_all.jpg'  # 存放图片的文件夹路径
            picture = random.sample(glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg')), 1)
            b = 0
            for i in picture:
                if b != 1:
                    self.upload_data(i)
                    b += 1
                    time.sleep(5)
        else:
            self.upload_data(picture)

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    config = Config()
    upload = UploadByNetty(config.device_num, config.url)
    upload.run("F:\接口自动化测试\\business_app\_api\image\\name8.jpg")
    # # day_count == 0 表示上传今天的数据，表示从第几天开始上传数据
    #
    # # pic_count 为每天需要上传的客流数 * 400
    # WSI_MASK_PATH = 'F:\\模拟上传数据\\6000_picture'  # 存放图片的文件夹路径
    # # picture = 'F:\接口自动化测试\\business_app\_api\image\\name1.jpg'  # 存放图片的文件夹路径
    # # body_pictureFile = 'F:\\模拟上传数据\\name10_all.jpg'  # 存放图片的文件夹路径
    # picture = random.sample(glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg')),1)
    # b=0
    # for i in picture:
    #     if b != 1:
    #         print(i)
    #         upload.upload_data(i)
    #         # upload2.upload_data(i, day_count, d)
    #         print("ok...")
    #         print("****************")
    #         b += 1
