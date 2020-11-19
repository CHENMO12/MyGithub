# -*- coding: utf-8 -*-
# @Time    : 2019/7/5 16:54
# @Author  : Huizi Cai
import hashlib
import json
import base64
import datetime
import random
import string


def str_md5(str):
    '''
    字符串进行md5加密
    :param str: 输入任一字符串
    :return:
    '''
    return hashlib.md5(str.encode('utf-8')).hexdigest()


def str2_md5(dic):
    '''
    字典进行md5加密
    :param str: 输入任字典
    :return:
    '''
    string = json.dumps(dic).replace(': ', ':').replace(', ', ',')
    print(string)
    m = hashlib.md5()
    m.update(string.encode(encoding='utf-8'))
    return (m.hexdigest())


def image_base64(image_path):
    with open(image_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        image_base64 = base64_data.decode()

    return image_base64


def get_current_time():
    dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
    return dateTime


def random_str():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    return salt


def random_num():
    order = "".join(random.choice("0123456789") for i in range(11))
    return order


def get_num(resopnse):
    for i in range(0, 100):
        if len(resopnse[i]):
            return i


def get_num02(resopnse):
    for i in range(0, 100):
        if resopnse[i] != 0:
            return resopnse[i]


a = get_current_time()
print(a)
