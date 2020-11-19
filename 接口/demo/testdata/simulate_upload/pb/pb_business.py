# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 17:27
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : pb_business.py

import os
import datetime
import time
import uuid
import random

from testdata.simulate_upload.pb import PacketModel_pb2
from testdata.simulate_upload.pb import get_seq_no
from testdata.simulate_upload.cryption import aes_cryption


# 输入：pb序列。返回经过AES加密后的pb序列
def aes_encryption(key,pb_serialize):
    ase = aes_cryption.ReAES(key)
    pb_serialize_aes_en = ase.encrypt(pb_serialize)
    return pb_serialize_aes_en

# 登录请求：赋值--pb序列化--AES加密
def login(key):
    login = PacketModel_pb2.Login()
    # 赋值
    login.base.seqno = get_seq_no.GetSeqNo().nextId()
    login.base.ver = 1
    login.msg = 'login'
    login.ip = '192.168.1.108'
    login.evState = 0
    login.type = 0
    login.hardwareVersion = 'V400003001'
    # 序列化 并转 十六进制字符串
    pb_serialize = login.SerializeToString()
    # pb_serialize = b''
    return aes_encryption(key,pb_serialize)
# 发送心跳
def beat(key):
    device_status = PacketModel_pb2.DeviceStatus()
    device_status.base.seqno = get_seq_no.GetSeqNo().nextId()
    device_status.base.ver = 1
    device_status.ip = '192.168.1.108'
    device_status.time = int(time.mktime(datetime.datetime.now().timetuple()))
    pb_serialize = device_status.SerializeToString()
    return aes_encryption(key, pb_serialize)
# 店计V4上报
def upload_v4_data(key,image_time,face_frame,body_frame,score,userStatus,capAngle,alarmId):
    upload_v4 = PacketModel_pb2.DankiV4ReportData()
    upload_v4.base.seqno = get_seq_no.GetSeqNo().nextId()
    upload_v4.base.ver = 1
    upload_v4.userStatus = userStatus    # 2（进店）,4（出店）
    upload_v4.capAngle = capAngle      # 0,1,3
    upload_v4.arithmetic = 1
    upload_v4.imageTime = image_time
    upload_v4.gender = 0
    upload_v4.age = 26
    upload_v4.alarmId = alarmId
    upload_v4.resideTime = 19
    upload_v4.faceFrame = face_frame
    upload_v4.bodyFrame = body_frame
    upload_v4.score = score
    pb_serialize = upload_v4.SerializeToString()
    return aes_encryption(key, pb_serialize)
