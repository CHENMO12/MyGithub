# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 16:47
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : validator.py

import os
import types
import datetime

from base.exceptions import ParamTypeException, FileException, DictException


def check_paramType_str(*args):
    '''
    作用：校验参数是否为字符串,可以校验多个
    :param param: 待校验的参数

        usage:
            check_paramType_str("12","223",12)
    '''
    for param in args:
        if not isinstance(param, str):
            raise ParamTypeException("参数类型必须为字符串:{}".format(param))

def check_paramType_int(*args):
    '''
    作用：校验参数是否为整数,可以校验多个
    :param param: 待校验的参数
    '''
    for param in args:
        if not isinstance(param, int):
            raise ParamTypeException("参数类型必须为整数:{}".format(param))

def check_paramType_dict(*args):
    '''
    作用：校验参数是否为字典,可以校验多个
    :param param: 待校验的参数
    '''
    for param in args:
        if not isinstance(param, dict):
            raise ParamTypeException("参数类型必须为字典:{}".format(param))

def check_paramType_list(*args):
    '''
    作用：校验参数是否为列表,可以校验多个
    :param param: 待校验的参数
    '''
    for param in args:
        if not isinstance(param, list):
            raise ParamTypeException("参数类型必须为列表:{}".format(param))

def check_paramType_boolean(*args):
    '''
    作用：校验参数是否为布尔值,可以校验多个
    :param param: 待校验的参数
    '''
    for param in args:
        if not isinstance(param, bool):
            raise ParamTypeException("参数类型必须为布尔值:{}".format(param))

def check_file_isExist(file_path):
    """
    功能: 校验文件是否存在
    :param file_path: 文件路径
    :return: 如果文件路径不存在,则直接抛出异常
    """

    # 校验：字符串参数
    check_paramType_str(file_path)

    # 校验：1个有效文件夹
    if os.path.exists(file_path):
        raise FileException("文件路径已存在:{}".format(file_path))

def check_file_isDir(file_dir):
    """
    功能：校验参数是一个有效的文件夹
    :param file_dir: 文件夹路径字符串
    :return:
    """

    # 校验：字符串参数
    check_paramType_str(file_dir)

    # 校验：1个有效文件夹
    if not os.path.isdir(file_dir):
        raise FileException("参数必须是一个有效的文件夹:{}".format(file_dir))

def check_file_isFile(file_path):
    """
    功能：校验参数是一个有效的文件路径
    :param file_path: 文件路径字符串
    :return:
    """

    # 校验：字符串参数
    check_paramType_str(file_path)

    # 校验：1个有效文件夹
    if not os.path.isfile(file_path):
        raise FileException("参数必须是一个有效的文件路径:{}".format(os.path.abspath(file_path)))

def check_int_gt_zero(param_int):
    """
    功能：校验参数是大于零的整数
    :param param_int: 待校验的参数
    :return:
    """

    # 校验: 整数
    check_paramType_int(param_int)

    # 校验: > 0
    if param_int <= 0 :
        raise FileException("参数不能为负数或零：{}".format(param_int))

def check_existKey_dict(des_dict, *args):
    """
    作用：校验key值是否存在于字典des_dict中
    :param des_dict: 一个字典
    :param args: 期望存在的字典key
    :return:
    """
    for key in args:
        if key not in des_dict.keys():
            raise DictException("key值：{}不存在于字典：{}".format(key, des_dict))




def is_testcase_json(json_data_structure):
    # 验证：是不是一个字典
    # 是否包含key：teststeps
    # teststeps这个key下的的value是不是一个list
    pass


def is_testcases_json(json_data_structure):
    # 根据定义好的多个用例数据格式来进行校验
    pass


def is_testcase_path(path):
    '''
    功能：如果入参是文件路径，校验文件是否存在
         如果入参是文件路径列表，校验列表中每个路径是否存在
    :param path: 文件路径或文件路径列表
    :return: 返回布尔值
    '''

    # 入参不是字符串或列表，返回False
    if not isinstance(path,(str,list)):
        return False

    # 入参是列表，列表中有路径不存在时，返回False
    if isinstance(path, list):
        for p in path:
            if not is_testcase_path(p):
                return False

    # 入参是文件路径，路径不存在时，返回False
    if isinstance(path, str):
        if not os.path.exists(path):
            return False

    return True


def is_function(item):
    return isinstance(item,types.FunctionType)


############ 基础校验：校验参数的数据类型

def checkParam_dataType_int(params):
    '''
    :param params: 必须为整数
    :return:
    '''

    if not isinstance(params, int):
        raise Exception("参数类型必须为整数:{}".format(params))

def checkParam_dataType_float(params):
    '''
    :param params: 必须为浮点数
    :return:
    '''

    if not isinstance(params, float):
        raise Exception("参数类型必须为小数:{}".format(params))

def checkParam_dataType_str(params):
    '''
    :param params: 必须为字符串
    :return:
    '''

    if not isinstance(params, str):
        raise Exception("参数类型必须为字符串:{}".format(params))

def checkParam_dataType_list(params):
    '''
    :param params: 必须为列表
    :return:
    '''

    if not isinstance(params, list):
        raise Exception("参数类型必须为列表:{}".format(params))
#############################################################

def checkParam_time_format(time_parms, time_format):
    '''
    满足某种时间格式的字符串
    :param time_parms: 必须符合time_format的时间格式
    :param time_format: 已定义的时间格式
    :return:
    '''

    # 校验：字符串类型
    checkParam_dataType_str(time_parms)
    checkParam_dataType_str(time_format)

    # 校验：时间格式是否正确
    try:
        datetime.datetime.strptime(time_parms, time_format)
    except Exception as e:
        raise Exception("参数格式必须为:{}".format(time_format))

def checkParam_int_positiveOrZero(digit_parms):
    '''
    :param digit_parms: 必须为非负整数
    :return:
    '''

    # 校验：整数类型
    checkParam_dataType_int(digit_parms)
    # 校验：必须大于等于0
    if digit_parms < 0:
        raise Exception("参数必须为非负整数:{}".format(digit_parms))


def checkParam_int_positive(digit_parms):
    '''
    :param digit_parms: 必须为正整数
    :return:
    '''

    # 校验：整数类型
    checkParam_dataType_int(digit_parms)
    # 校验：必须大于等于0
    if digit_parms <= 0:
        raise Exception("参数必须为正整数:{}".format(digit_parms))

def checkParam_file_isDir(dir_path):
    '''
    :param dir_path: 必须为1个有效的文件夹
    :return:
    '''

    # 校验：字符串类型
    checkParam_dataType_str(dir_path)
    # 校验：必须是1个有效的文件夹
    if not os.path.isdir(dir_path):
        raise Exception("参数必须是一个有效的文件夹:{}".format(dir_path))























