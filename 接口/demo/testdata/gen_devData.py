# -*- coding: utf-8 -*-
# @Time    : 2019/10/26 19:43
# @Author  : 34801 
# @Email   : yuelei@reconova.cn
# @File    : gen_deviceData
from base.helper import TimeHelper
from testdata.simulate_upload import upload_by_netty


def simulate_device_upload_pic(deviceCode, img_time=None, score=None, img_path=None, body_img_path=None, userStatus=None, capAngle=None):
    '''
    功能：模拟设备向云端上报图片
    :return:
    '''
    deviceCode, socket_addr, aes_key = upload_by_netty.get_device_connInfo(deviceCode)
    upload = upload_by_netty.UploadNetty(deviceCode, socket_addr, aes_key)

    upload.simulate_device_uploadPic(img_time=img_time, score=score, img_path=img_path, body_img_path=body_img_path, userStatus=userStatus, capAngle=capAngle)

def simulate_device_login(device_no):
    '''
    功能：模拟设备向云端上报图片
    :return:
    '''

    device_no, socket_addr, aes_key = upload_by_netty.get_device_connInfo(device_no)
    upload_by_netty.UploadNetty(device_no, socket_addr, aes_key)

if __name__ == '__main__':
    dev_code = "gmz4K81Wpjl8fN"
    simulate_device_upload_pic(dev_code, img_time=TimeHelper.get_custom_time(timestamp_offset=8000), score=1.2)