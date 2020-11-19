# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 17:27
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : commonTime.py

import hashlib

def str2md5(str):
    '''
    字符串进行md5加密
    :param str: 输入任一字符串
    :return:
    '''
    return hashlib.md5(str.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    print(str2md5(str2md5("Reconova$123")+"151638247"))