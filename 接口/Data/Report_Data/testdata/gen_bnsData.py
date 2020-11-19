# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 11:47
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : gen_bnsData.py

"""
    文件作用:
        存放可参数化的简单业务值

    命名规则:

        "{}_{}_{}".format(
            "模块key",           # 一个平台被分为多个模块
            "模块功能的详细描写",  # 如果不需要详细描述,可以不写
            "参数属性"           # 接口参数的属性说明
        )

    命名举例:

        例1: 对设备名字进行参数化,但设备有多种类型
        code:
            from base.helper import StringHelper
            def device_captureCamera_name():
                return "抓拍相机{}".format(StringHelper.get_random_normalString(5))

        例2: 对设备备注进行参数化
        code:
            from base.helper import StringHelper
            def device_remark():
                return "设备备注{}".format(StringHelper.get_random_normalString(5))

    使用场景:

        1. scn api 的封装
        2. 模块用例和场景用例
"""
import random
import datetime

from base.helper import StringHelper
from base.helper import JsonHelper
from testdata.addr import node_addr
from base.helper import TimeHelper
from base.helper import FileHelper
import os
import string

now_date = TimeHelper.get_time_from_timestamp()[:10]

################# 声明一些重要的路径或资源路径 #################
# 项目根目录
__project_rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 上报图片的目录
img1_dir = __project_rootdir + os.sep + 'testdata' + os.sep + 'upload_pics_1' + os.sep
# 上报像素图片的目录
pixel_img_dir = __project_rootdir + os.sep + 'testdata' + os.sep + 'upload_pics_facePixel' + os.sep


def random_queryMenu_id():
    return random.choice(range(0, 20))


def random_publicDevice_lensType():
    return random.choice([6, 8, 12, 16])


def random_Str():
    return random.choice(["CNY", "HKD", "USD", "EUR", "GBP"])


def random_str():
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return ran_str


def get_current_time(day=None):
    if day is None:
        today = datetime.date.today() + datetime.timedelta(days=1)
    else:
        today = datetime.date.today() + datetime.timedelta(days=day)

    return str(today)

def get_now_time():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    return now_time

if __name__ == '__main__':
    a = get_now_time()
    print(a)
