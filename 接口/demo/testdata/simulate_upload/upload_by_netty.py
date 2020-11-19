# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 18:00
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : upload_by_netty.py

import sys
sys.path.append("../..")

# from gevent import monkey;monkey.patch_all()
import gevent
import socket
import struct
import random
import time

from base.logger import Logger
from testdata.simulate_upload.pb import pb_business
from testdata.simulate_upload.pb import func_num_map
from base.helper import ImageHelper
from base.helper import TimeHelper
from base.helper import AllureHelper
from testdata import gen_bnsData
from bns.dkyj.api import Api


api = Api()
# 根据设备来获取ip和端口
def get_device_connInfo(deviceCode):
    # 通过设备鉴权接口来获取设备的ip和port
    auth_info = api.scn_device_auth(deviceCode)
    if not auth_info:
        exit('dev:%s 设备鉴权失败.' % deviceCode)
    socket_addr = (auth_info['ip'], auth_info['port'])
    aes_key = auth_info['randCode']
    return deviceCode,socket_addr,aes_key

class UploadNetty():

    def __init__(self, deviceCode, socket_addr, aes_key):

        self.deviceCode = deviceCode
        self.socket_addr = socket_addr
        self.aes_key = aes_key
        self.log = Logger()

        self.simulate_socket_conn()
        self.simulate_device_login()

        g1 = gevent.spawn(self.simulate_device_beat)
        g1.join()

    # 模拟socket：建立连接
    def simulate_socket_conn(self):
        # 建立socket连接
        self.conn = None
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(self.socket_addr)
            return self.conn
        except Exception as e:
            self.conn.close()
            exit("socket连接建立失败：{}".format(e))

    # 模拟socket：发送消息
    def send_message(self, send_msg):
        try:
            self.conn.sendall(send_msg)
            # res = self.conn.recv(8192)
            # print(res)
        except Exception as e:
            print("发送消息失败：{}".format(e))
            self.conn.close()

    # 模拟业务场景：设备登录
    def simulate_device_login(self):
        info_dict = dict()
        info_dict.setdefault('设备编码', self.deviceCode)
        pb_login_msg = pb_business.login(self.aes_key)
        dev_no_len = len(self.deviceCode)
        msg_aes_len = len(pb_login_msg)
        format = '>BIHIB%ds%ds' % (dev_no_len, msg_aes_len)
        send_msg = struct.pack(format, int('0x1A', 16), msg_aes_len, func_num_map.Login, 0, dev_no_len, self.deviceCode.encode('utf-8'), pb_login_msg)
        self.send_message(send_msg)
        self.log.log_info("设备上报登录信息：{}".format(info_dict))

    # 模拟业务场景：设备心跳
    def simulate_device_beat(self):
        pb_login_beat = pb_business.beat(self.aes_key)
        msg_aes_len = len(pb_login_beat)
        format = '>BIHI%ds' % (msg_aes_len)
        send_msg = struct.pack(format, int('0x1A', 16), msg_aes_len, func_num_map.DeviceStatus , 0, pb_login_beat)
        self.send_message(send_msg)

    # 模拟业务场景：设备上报图片
    def simulate_device_uploadPic(self, img_time=None, score=None, img_path=None, body_img_path=None, userStatus=None, capAngle=None):

        if img_time is None:
            img_time = TimeHelper.get_time(t=TimeHelper.get_time_from_timestamp(), offset=10)
        if score is None:
            score = str(random.randint(80, 190) / 100)
        if img_path is None:
            img_path = gen_bnsData.get_face_picture(index=1)
        face_frame = ImageHelper.pic_to_bytes(img_path)
        if body_img_path is None:
            body_frame = face_frame
        else:
            body_frame = ImageHelper.pic_to_bytes(body_img_path)
        if userStatus is None:
            userStatus = 2  # 默认进店
        if capAngle is None:
            capAngle = 0  # 默认正脸
        alarmId = gen_bnsData.get_alarmId(timestamp=TimeHelper.get_timestamp_from_time(assigned_time=img_time))

        pb_login_msg = pb_business.upload_v4_data(self.aes_key, img_time, face_frame, body_frame, float(score), userStatus, capAngle, alarmId)
        msg_aes_len = len(pb_login_msg)
        format = '>BIHI%ds' % (msg_aes_len)
        send_msg = struct.pack(format, int('0x1A', 16), msg_aes_len, func_num_map.DankiV4ReportData, 0, pb_login_msg)

        # 定义函数需要返回的信息
        info_dict = dict()
        info_dict.setdefault('img_time', img_time)
        info_dict.setdefault('score', score)
        info_dict.setdefault('alarmId', alarmId)
        info_dict.setdefault('userStatus', userStatus)
        info_dict.setdefault('capAngle', capAngle)
        # info_dict.setdefault('face_frame', face_frame)

        self.checkLoginInfo()

        self.send_message(send_msg)
        self.log.log_info("设备上报图片信息：{}".format(info_dict))

        self.checkReplyInfo()

        AllureHelper.attachJson(info_dict, "设备上报的信息")
        AllureHelper.attachPic(face_frame, "设备上报的图片")

        return info_dict

    def checkLoginInfo(self):
        start_time = time.time()
        while True:
            try:
                info_dict = dict()
                end_time = time.time()
                # 等待接收到11个字节
                res = self.conn.recv(11)
                # 获取信息：数据长度、功能号
                data_len = int.from_bytes(res[1:5], byteorder='big')
                func_num = int.from_bytes(res[5:7], byteorder='big')
                self.conn.recv(data_len)
                tmp_res = 'NETTY服务器回复功能号：%s' % func_num_map.functionNo_dict.get(func_num)
                AllureHelper.attachText(tmp_res,"NETTY服务器回复功能号")
                if func_num == 2:
                    info_dict.setdefault('设备登录', func_num_map.functionNo_dict.get(func_num))
                    self.log.log_info("收到设备登录信息回包：{}".format(info_dict))
                    break
                if func_num == 4:
                    info_dict.setdefault('设备心跳', func_num_map.functionNo_dict.get(func_num))
                    self.log.log_info("收到设备心跳信息回包：{}".format(info_dict))
                if end_time - start_time >= 120:
                    raise Exception("NETTY服务器2min超时未回复ReplyLogin")
            except Exception:
                raise Exception("NETTY服务器失败回复ReplyLogin")

    def checkReplyInfo(self):
        start_time = time.time()
        while True:
            try:
                info_dict = dict()
                end_time = time.time()
                # 等待接收到11个字节
                res = self.conn.recv(11)
                # 获取信息：数据长度、功能号
                data_len = int.from_bytes(res[1:5], byteorder='big')
                func_num = int.from_bytes(res[5:7], byteorder='big')
                self.conn.recv(data_len)
                tmp_res = 'NETTY服务器回复功能号：%s' % func_num_map.functionNo_dict.get(func_num)
                AllureHelper.attachText(tmp_res,"NETTY服务器回复功能号")
                if func_num == 12 :
                    info_dict.setdefault('设备上报', func_num_map.functionNo_dict.get(func_num))
                    self.log.log_info("收到设备上报图片回包：{}".format(info_dict))
                    break
                if end_time-start_time >=120:
                    raise Exception("NETTY服务器2min超时未回复ReplyReportData")
            except Exception:
                raise Exception("NETTY服务器失败回复ReplyReportData")


if __name__ == '__main__':

    deviceCode, socket_addr, aes_key = get_device_connInfo("49158z36167342")

    upload = UploadNetty(deviceCode, socket_addr, aes_key)

    upload.simulate_device_uploadPic()

