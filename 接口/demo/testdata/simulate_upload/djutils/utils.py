# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 17:10
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : utils.py

import string
import random
import base64
import datetime
import time

# 随机字符串，包含：aA0
def random_string_aA0(count):
    src_digits = string.digits  # string_数字
    src_uppercase = string.ascii_uppercase  # string_大写字母
    src_lowercase = string.ascii_lowercase  # string_小写字母
    digits_num = random.randint(1, 6)
    uppercase_num = random.randint(1, 8 - digits_num - 1)
    lowercase_num = count - (digits_num + uppercase_num)
    # 生成字符串
    password = random.sample(src_digits, digits_num) + random.sample(src_uppercase, uppercase_num) + random.sample(src_lowercase, lowercase_num)
    # 打乱字符串
    random.shuffle(password)
    # 列表转字符串
    return ''.join(password)
# 图片base64码
def get_pic_base64(pic_name):
    with open(pic_name,'rb') as fp:
        return base64.b64encode(fp.read()).decode("utf-8")
# 图片字节码
def get_pic_bytes(pic_name):
    with open(pic_name,'rb') as fp:
        return fp.read()
# 获取当前：date time
def get_now_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 获取当前时间戳
def get_timestamp():
    return int(time.time())
# 超前于当前时间m 秒
def get_time_advance_nowtime(add_sec):
    timestamp = get_timestamp()
    des_timestamp = timestamp + add_sec
    local_time = time.localtime(des_timestamp)
    time_data = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return time_data