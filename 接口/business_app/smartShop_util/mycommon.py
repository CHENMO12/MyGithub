# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 17:27
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : commonTime.py

'''
    包含内容：
        1. JSON解析
        2. 随机字符串获取
        3. 获取常用时间格式
'''

import allure
import objectpath
import types
import time
import datetime
import json
import random
import string
import hashlib

############## JSON解析 ###################################
def attachJson(res_json, desc):
    try:
        format_data = json.dumps(res_json, sort_keys=True, indent=4, ensure_ascii=False)
        allure.attach(format_data, desc, allure.attachment_type.JSON)
    except Exception as e:
        attachText(res_json,desc)

def attachText(res_json,desc):
    allure.attach(str(res_json), desc, allure.attachment_type.TEXT)

def parseJson_by_objectpath(json_obj,pattern,allows_null=False):
    # 默认情况下，json的解析不允许返回空值，allows_null=False
    try:
        tree = objectpath.Tree(json_obj)
        res = tree.execute(pattern)
        gen = isinstance(res,types.GeneratorType)
        if gen is True:
            return list(res)
        else:
            if res is None:
                if allows_null:
                    return False
                else:
                    exit("json中提取不到信息：{}".format(pattern))
            return res
    except Exception as e:
        exit("objecctpath的pattern格式有错误:{}".format(pattern))
        # print(e)
        # return False
# res = parseJson_by_objectpath({"a":1},"$.a")
# print(res)

############## 随机字符串获取 ###############################
# 随机电话号码
def random_phoneno():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]
    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]
    # 最后八位数字
    suffix = random.randint(9999999, 100000000)
    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)

# 随机的数字组合
def random_digit(length):
    slcNum = [random.choice(string.digits) for i in range(length)]
    random.shuffle(slcNum)
    getPwd = ''.join([i.lower() for i in slcNum])
    return getPwd

# 随机数字+小写字母
def random_string(length):
    Ofnum = random.randint(1, length)
    Ofletter = length - Ofnum
    slcNum = [random.choice(string.digits) for i in range(Ofnum)]
    slcLetter = [random.choice(string.ascii_letters) for i in range(Ofletter)]
    slcChar = slcLetter + slcNum
    random.shuffle(slcChar)
    getPwd = ''.join([i.lower() for i in slcChar])
    return getPwd


############## 获取常用时间格式 #############################
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 获取时间: 默认获取当前时间
def get_time_from_timestamp(timestamp=None):
    if timestamp is None:
        return datetime.datetime.now().strftime(TIME_FORMAT)
    local_time = time.localtime(timestamp)
    time_data = time.strftime(TIME_FORMAT, local_time)
    return time_data

# 获取时间戳：默认获取当前时间戳
def get_timestamp_from_time(t=None):
    if t is None:
        return int(time.time())
    t = time.strptime(t, TIME_FORMAT)
    return int(time.mktime(t))

def get_time(t,offset=None):
    '''
    输入：time，offset
    返回：time
    :param t:
    :param offset:
    :return:
    '''
    timestamp = get_timestamp_from_time(t)
    new_timestamp = int(timestamp)+int(offset)
    return get_time_from_timestamp(timestamp=new_timestamp)

def get_timeList(t,interval,total_count,sample_count):
    '''
    输入：time，interval，count
    返回：根据count的随机列表
    :param t:
    :param interval:
    :param total_count:
    :param sample_count:
    :return:
    '''
    timestamp = get_timestamp_from_time(t)
    tmp_list = []
    for _ in range(int(total_count)):
        tmp_list.append(timestamp)
        timestamp += int(interval)
    res_list = random.sample(tmp_list,int(sample_count))
    res = []
    for _ in res_list:
        res.append(get_time_from_timestamp(_))
    res.sort()
    return res

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()



if __name__ == '__main__':
    # print(get_time_from_timestamp())
    # print(get_timestamp_from_time())

    res_json = "{'request_data': {'condition': {'areaType': [], 'areaCode': '00KK', 'name': ''}}, 'response_code': 200, 'response_data': {'message': '成功', 'code': 0, 'data': {'pageSize': 10, 'pageNo': 1, 'total': 1, 'list': [{'areaId': 2760, 'parentAreaCode': '00KK', 'areaCode': '00KK-0001', 'name': '品牌28616', 'areaType': 200, 'createTime': '2019-05-28 16:15:44'}]}}, 'response_time': 0.018326}"
    import json

    res_json = json.loads(res_json)
    parseJson_by_objectpath(res_json,"$.response_data")



