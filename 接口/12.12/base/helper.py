# -*- coding: utf-8 -*-
# @Time    : 2019/6/24 10:55
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : helper.py

'''
    常用的工具类
'''
import csv
import time
import datetime
import random
import hashlib
import types
import os
import json
import string
import configparser
import base64
import math

import pymysql
import yaml
import objectpath
import allure

from base import logger
from base import exceptions
from base import validator
from base.exceptions import CsvContentException

log = logger.Logger()

_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
_DEFAULT_ENCODING_UTF8 = "utf-8"
PROJECT_ROOT = os.path.abspath("../")

class FileHelper():

    @staticmethod
    def create_filepath(filepath):
        """
        功能：如果文件路径不存在就创建
        :param filepath: 文件路径，需要是绝对路径
        :return:
        """

        if not os.path.isabs(filepath):
            raise exceptions.FileException("参数必须是绝对路径")

        path = filepath[0:filepath.rfind(os.sep)]

        if not os.path.isdir(path):
            try:
                os.makedirs(path)
                log.log_info("创建文件夹成功：{}".format(path))
            except:
                log.log_error("创建文件夹失败：{}".format(path))

        if not os.path.isfile(filepath):
            with open(filepath, mode='w', encoding='utf-8'):
                log.log_info("创建文件成功：{}".format(filepath))
                pass
        else:
            pass

    @staticmethod
    def delete_file(filepath):
        """
        功能：如果文件存在就删除该文件
        注意：仅限于删除一个文件
        :param filepath: 文件路径
        :return:
        """

        if os.path.isfile(filepath):
            try:
                os.remove(filepath)
                log.log_info("删除文件成功：{}".format(filepath))
            except Exception as e:
                raise exceptions.FileException("无法删除此文件：{}".format(filepath))

    @staticmethod
    def get_file_from_dir(file_dir, file_index=None):
        """
        功能：从一个文件夹内返回一个文件路径
        :param file_dir: 文件夹
        :param file_index: 文件索引(默认索引随机值，也可以指定索引)
        :return: 返回一个文件路径(绝对路径)
        """
        # TODO(dongjun): 如果随机从文件夹获取的还是文件夹，该如何返回？

        validator.check_file_isDir(file_dir)

        # 获取文件夹下内容列表
        dir_list = os.listdir(file_dir)

        if not dir_list:
            raise exceptions.FileException("文件夹内无文件：{}".format(file_dir))

        # 文件夹下的文件数量
        file_counts = len(dir_list)

        index_max = file_counts
        if file_index or file_index==0:
            # 校验 file_index：必须是正整数
            validator.check_int_gt_zero(file_index)
            # 校验：file_index不能超过文件列表的最大长度
            if file_index > index_max:
                raise exceptions.FileException("文件索引溢出，期望最大索引：{}，实际入参索引：{}".format(index_max, file_index))
            tmp_pic_name = dir_list[file_index - 1]

            if file_dir.endswith(os.sep):
                tmp_pic_path = file_dir + tmp_pic_name
            else:
                tmp_pic_path = file_dir + os.sep + tmp_pic_name
            return tmp_pic_path

        tmp_pic_name = random.choice(dir_list)
        if file_dir.endswith(os.sep):
            tmp_pic_path = file_dir + tmp_pic_name
        else:
            tmp_pic_path = file_dir + os.sep + tmp_pic_name
        return tmp_pic_path

    @staticmethod
    def load_folder_yaml_files(folder_path_or_pathList, file_suffix, recursive=True):
        '''
        功能：找到一个文件夹或文件夹列表下的所有指定后缀文件
        :param folder_path_or_pathList: 文件夹或文件夹列表
        :param file_suffix: 文件后缀，例如：".yaml"
        :param recursive: 是否递归查找
        :return:
        '''

        # 如果是文件夹列表
        if isinstance(folder_path_or_pathList, list):
            files = []
            for path in set(folder_path_or_pathList):
                files.extend(FileHelper.load_folder_yaml_files(path, recursive))
            return files

        # 如果是不存在的文件夹
        if not os.path.exists(folder_path_or_pathList):
            return []

        # 如果是一个文件夹
        file_list = []
        for dirpath, dirnames, filenames in os.walk(folder_path_or_pathList):
            filenames_list = []
            for filename in filenames:
                if not filename.endswith(file_suffix):
                    continue
                filenames_list.append(filename)
            for filename in filenames_list:
                file_path = os.path.join(dirpath, filename)
                file_list.append(file_path)
            if not recursive:
                break

        return file_list

    @staticmethod
    def get_files_from_folderOrFolderlist(folder_or_folderList, file_suffix, recursive=True):
        '''
        功能：找到一个文件夹或文件夹列表下的所有指定后缀文件
        :param folder_or_folderList: 文件夹或文件夹列表
        :param file_suffix: 文件后缀，例如：".yaml"
        :param recursive: 是否递归查找，默认进行递归循环
        :return:
        '''

        # 如果是文件夹列表
        if isinstance(folder_or_folderList, list):
            files = []
            for one_folder in set(folder_or_folderList):
                files.extend(FileHelper.get_files_from_folderOrFolderlist(one_folder, file_suffix, recursive))
            return files

        # 如果是不存在的文件夹
        if not os.path.exists(folder_or_folderList):
            return []

        # 如果是文件夹
        file_list = []
        for dirpath, dirnames, filenames in os.walk(folder_or_folderList):
            filenames_list = []
            for filename in filenames:
                if not filename.endswith(file_suffix):
                    continue
                filenames_list.append(filename)
            for filename in filenames_list:
                file_path = os.path.join(dirpath, filename)
                file_list.append(file_path)
            if not recursive:
                break

        return file_list

class YamlHelper():

    @staticmethod
    def load_yaml_file(yaml_file):
        '''
        功能：加载yaml文件
        :param yaml_file: yaml文件
        :return: 一个列表或字典
        '''
        # TODO(dongjun): 检查文件是否存在
        # TODO(dongjun): 检查文件是不是yaml文件

        with open(yaml_file, mode='r', encoding=_DEFAULT_ENCODING_UTF8) as stream:
            try:
                yaml_content = yaml.load(stream, Loader=yaml.FullLoader)
            except AttributeError:
                yaml_content = yaml.load(stream)

            # 文件内容不能为空
            if not yaml_content:
                err_msg = "文件内容为空: {}".format(yaml_file)
                raise exceptions.FileException(err_msg)

            # 文件内容不是 列表或字典
            elif not isinstance(yaml_content, (list, dict)):
                err_msg = "文件格式不正确: {}".format(yaml_file)
                raise exceptions.FileException(err_msg)

            return yaml_content

class JsonHelper():

    @staticmethod
    def json_format(json_dict):
        """
        功能：json字典 --> 带缩进格式的json字符串
        :param json_dict: json字典
        :return: 带缩进格式的json字符串
        """
        validator.check_paramType_dict(json_dict)
        return json.dumps(json_dict, sort_keys=True, indent=4, ensure_ascii=False)

    @staticmethod
    def parseJson_by_objectpath(json_dict, pattern, res_allowNone=False, res_firstOne=False):
        """
        功能: 输入表达式来提取json中的内容
        PS：关于表达式pattern的规则，请参考：http://objectpath.org/reference.html
        :param json_dict: 字典类型
        :param pattern: 提取信息表达式
        :param res_allowNone: 是否允许提取不到信息, 默认False
        :param res_firstOne:  如果返回的是一个非空列表, 是否返回列表的首个元素, 默认False
        :return: 返回提取到的内容 或 直接抛出异常
        """

        if not json_dict:
            raise Exception("objectpath解析json失败：待解析内容为空({})".format(json_dict))

        if not isinstance(json_dict, dict):
            raise Exception("objectpath解析json失败：待解析内容不是字典")

        try:
            tree = objectpath.Tree(json_dict)
            res = tree.execute(pattern)

            import itertools
            if isinstance(res, (types.GeneratorType,itertools.chain)) is True:
                res_list = list(res)
                if len(res_list) > 0:
                    if res_firstOne:
                        return res_list[0]
                    return res_list
                else:
                    if res_allowNone:
                        return False
                    raise Exception("json中提取不到信息：{}，此时传入的json内容为{}".format(pattern,json_dict))
            else:
                if res is None:
                    if res_allowNone:
                        return False
                    raise Exception("json中提取不到信息：{}，此时传入的json内容为{}".format(pattern, json_dict))
                return res
        except Exception as e:
            raise Exception("objectpath解析json失败: 提取表达式:{}, json内容为{}".format(pattern, json_dict))

class MysqlHelper():

    _host = None
    _port = None
    _username = None
    _password = None
    _conn = None
    _cursor = None

    def __init__(self, host, username="root", password="123456", port=3306):

        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self._conn = self.get_conn()

        if self._conn:
            self._cursor = self._conn.cursor()
        else:
            raise Exception("mysql数据库无法连接")

    @staticmethod
    def read_sql(file_path, encoding=_DEFAULT_ENCODING_UTF8):
        """
        功能功能：从sql文件读取 SQL 脚本
        :param file: sql文件路径
        :param encoding:
        :return: sql信息
        """
        sql_file = open(file_path, "r", encoding=encoding)
        sql = sql_file.read()
        sql_file.close()
        return sql

    def __get_conn_info(self, msg):
        # 定义数据库的log信息格式
        log.log_info("""
            {}:
                [host]:{},
                [port]:{},
                [username]:{},
                [password]:{},
        """.format(msg, self._host, self._port, self._username, self._password))

    def get_conn(self):
        conn = None
        try:
            conn = pymysql.connect(
                host=self._host,
                port=self._port,
                user=self._username,
                password=self._password,
            )
        except Exception as e:
            self.__get_conn_info("mysql连接失败")
            log.log_error("连接异常提示：{}".format(e))
        else:
            return conn

    def query_sql(self, sql_cmd):
        """
        功能：sql查询
        :param sql_cmd: select语句
        :return: sql查询结果
        """
        # TODO(dongjun): 如果一次查询内容过多，可以做一个分页查询的功能

        try:
            self._cursor.execute(sql_cmd)
            sql_res = self._cursor.fetchall()
        except Exception as e:
            log.log_error("sql查询失败,异常提示：{}".format(e))
            log.log_error("sql查询失败,异常sql：{}".format(sql_cmd))
        else:
            return sql_res

    # 提交操作
    def exec_sql(self, sql_cmd):
        """
        功能：sql执行操作
        :param sql_cmd: 需要执行的sql语句：增删改
        :return: 返回一个布尔值。True代表执行成功，False代表执行失败
        """
        flag = False
        try:
            self._cursor.execute(sql_cmd)
            self._conn.commit()
            flag = True
        except Exception as e:
            flag = False
            self._conn.rollback()
            log.log_error("sql执行失败,异常提示：{}".format(e))
            log.log_error("sql执行失败,异常sql：{}".format(sql_cmd))
        else:
            return flag

    def close(self):

        if self._conn:
            try:
                if type(self._cursor) == 'object':
                    self._cursor.close()
                if type(self._conn) == 'object':
                    self._conn.close()
            except:
                raise ("关闭数据库连接异常, %s,%s" % (type(self._cursor), type(self._conn)))

class TimeHelper():

    @staticmethod
    def get_time_from_timestamp(timestamp=None, time_format=None):
        """
        功能：将一个时间戳转为指定时间格式的时间，默认转为的时间格式为：%Y-%m-%d %H:%M:%S
            场景1：获取当前时间，时间格式为：%Y-%m-%d %H:%M:%S
                get_time_from_timestamp()
            场景2：获取当前时间，时间格式为：%H:%M:%S
                get_time_from_timestamp(time_format="%H:%M:%S")
            场景3：根据指定时间戳来获取时间，时间格式为：%Y-%m-%d %H:%M:%S
                get_time_from_timestamp(timestamp=1569850832)
        :param timestamp: 待转换为时间的时间戳，默认为当前时间戳
        :param time_format: 待转换成的时间格式，默认时间格式：%Y-%m-%d %H:%M:%S
        :return: 返回一个指定格式的时间
        """


        if time_format is None:
            time_format = _TIME_FORMAT
        validator.check_paramType_str(time_format)

        if timestamp is None:
            return datetime.datetime.now().strftime(time_format)

        validator.check_paramType_int(timestamp)
        local_time = time.localtime(timestamp)
        time_data = time.strftime(time_format, local_time)
        return time_data

    @staticmethod
    def get_timestamp_from_time(assigned_time=None, magnitude="s"):
        """
        功能：将一个形如"2019-10-10 09:00:00"的时间转为时间戳
            场景1：获取当前秒级时间戳
                get_timestamp_from_time()
            场景2：获取当前毫秒级时间戳
                get_timestamp_from_time(magnitude="ms")
            场景3：获取指定时间(2019-10-10 09:00:00)对应的秒级时间戳
                get_timestamp_from_time(assigned_time="2019-10-10 09:00:00")
        :param assigned_time: 需要转为时间戳的时间，时间格式要求：2019-10-10 09:00:00
        :param magnitude: 时间戳数量级：秒(s)、毫秒(ms)、微妙(us)
        :return: 返回一个时间戳
        """

        validator.check_paramType_str(magnitude)
        if magnitude == "s":
            factor = 1
        elif magnitude == "ms":
            factor = 1000
        elif magnitude == "us":
            factor = 1000000
        else:
            raise exceptions.ListOptionsException("不期望的magnitude值：{}".format(magnitude))

        if assigned_time is None:
            return int(time.time()*factor)

        validator.check_paramType_str(assigned_time)
        t = time.strptime(assigned_time, _TIME_FORMAT)
        return int(time.mktime(t)*factor)

    @staticmethod
    def get_custom_time(timestamp_offset, assigned_time=None):
        """
        功能：获取一个相对时间(相对于某个时间超前或滞后)
            场景1：获取超前于当前时间10s的时间
                get_custom_time(timestamp_offset=10)
            场景2：获取滞后于当前时间10s的时间
                get_custom_time(timestamp_offset=-10)
            场景2：获取超前于"2019-10-01 09:09:09"时间20s的时间
                get_custom_time(timestamp_offset=20, assigned_time="2019-10-01 09:09:09")
        :param assigned_time: 参数时间点，默认为当前时间(格式：%Y-%m-%d %H:%M:%S)
        :param timestamp_offset: 秒级时间戳偏移量(正整数表示超前m秒，负整数表示滞后m秒)
        :return: 返回一个时间，时间格式为：%Y-%m-%d %H:%M:%S
        """

        validator.check_paramType_int(timestamp_offset)

        if assigned_time is None:
            assigned_time = TimeHelper.get_time_from_timestamp()
        validator.check_paramType_str(assigned_time)

        # TODO: 通过正则来校验参数格式为：%Y-%m-%d %H:%M:%S
        timestamp = TimeHelper.get_timestamp_from_time(assigned_time)
        new_timestamp = timestamp + timestamp_offset
        return TimeHelper.get_time_from_timestamp(timestamp=new_timestamp)

    @staticmethod
    def get_time(t, offset=None):
        '''
        输入：time，offset
        返回：time
        :param t:
        :param offset:
        :return:
        '''
        timestamp = TimeHelper.get_timestamp_from_time(t)
        new_timestamp = int(timestamp) + int(offset)
        return TimeHelper.get_time_from_timestamp(timestamp=new_timestamp)

class EncryptHelper():

    @staticmethod
    def md5(str):
        """
        功能：将一个字符串进行md5加密
        :param str: 待加密的字符串
        :return: md5值
        """

        validator.check_paramType_str(str)

        m = hashlib.md5()
        m.update(str.encode("utf8"))
        return m.hexdigest()

class AllureHelper():

    @staticmethod
    def attachText(res_json, desc):
        allure.attach(str(res_json), desc, allure.attachment_type.TEXT)

    @staticmethod
    def attachJson(res_json, desc):

        try:
            format_data = json.dumps(res_json, sort_keys=True, indent=4, ensure_ascii=False)
            allure.attach(format_data, desc, allure.attachment_type.JSON)
        except Exception as e:
            AllureHelper.attachText(res_json, desc)

    @staticmethod
    def attachPic(pic_bytes, desc):
        allure.attach(pic_bytes, desc, allure.attachment_type.PNG)

    @staticmethod
    def extract_business_code(res_json,pattern_code):
        return JsonHelper.parseJson_by_objectpath(res_json,"$.response_data.{}".format(pattern_code))

    @staticmethod
    def assert_equal(desc_msg, except_var, actual_var):
        with allure.step('结果校验：{}'.format(desc_msg)):
            AllureHelper.attachText("", "期望{}：{}".format(desc_msg, except_var))
            AllureHelper.attachText("", "实际{}：{}".format(desc_msg, actual_var))
            assert except_var == actual_var
        return (except_var, actual_var)

    @staticmethod
    # 期望结果不等某个值
    def assert_notEqual(desc_msg, expect_var, actual_var):
        with allure.step('结果校验：{}'.format(desc_msg)):
            AllureHelper.attachText("", "期望{}：不等于 {}".format(desc_msg, expect_var))
            AllureHelper.attachText("", "实际{}：{}".format(desc_msg, actual_var))
            assert expect_var != actual_var
        return (expect_var, actual_var)

    @staticmethod
    def assert_isContain(desc_msg, expect_var, actual_var):
        desc_msg = "{}应该被包含".format(desc_msg)
        with allure.step('结果校验：{}'.format(desc_msg)):
            AllureHelper.attachText("", "期望关键信息：{}".format(expect_var))
            AllureHelper.attachText("", "实际输出信息：{}".format(actual_var))
            assert expect_var in str(actual_var)

    @staticmethod
    def assert_isNotContain(desc_msg, expect_var, actual_var):
        desc_msg = "{}不应被包含".format(desc_msg)
        with allure.step('结果校验：{}'.format(desc_msg)):
            AllureHelper.attachText("", "期望关键信息：不包含 {}".format(expect_var))
            AllureHelper.attachText("", "实际输出信息：{}".format(actual_var))
            assert expect_var not in str(actual_var)

    @staticmethod
    def assert_except_le_actual(desc_msg, except_int, actual_int):

        validator.checkParam_dataType_str(desc_msg)
        validator.checkParam_dataType_int(except_int)
        validator.checkParam_dataType_int(actual_int)

        desc_msg = "{}".format(desc_msg)
        with allure.step('结果校验：{}'.format(desc_msg)):
            AllureHelper.attachText("", "期望数字大于等于： {}".format(except_int))
            AllureHelper.attachText("", "实际数字：{}".format(actual_int))
            assert except_int <= actual_int

    @staticmethod
    def assert_except_ge_actual(desc_msg, except_int, actual_int):

        validator.checkParam_dataType_str(desc_msg)
        validator.checkParam_dataType_int(except_int)
        validator.checkParam_dataType_int(actual_int)

        desc_msg = "{}".format(desc_msg)
        with allure.step('结果校验：{}'.format(desc_msg)):
            AllureHelper.attachText("", "期望数字小于等于：{}".format(except_int))
            AllureHelper.attachText("", "实际数字：{}".format(actual_int))
            assert except_int >= actual_int

    @staticmethod
    def assert_timeRange(desc_msg, expect_time, actual_time, offset_sec=None, time_format=None):
        '''
        功能：实际时间是否在当前时间允许的误差范围内
        :param actual_time: 待校验的时间
        :param offset_sec: 时间误差偏移量
        :return:
        '''

        # 默认参数定义
        if not offset_sec:
            offset_sec = 5
        if time_format is None:
            time_format = "%Y-%m-%d %H:%M:%S"

        # 入参校验：actual_time
        validator.checkParam_time_format(actual_time,time_format)
        # 入参校验：expect_time
        validator.checkParam_time_format(expect_time,time_format)
        # 入参校验：offset_sec
        validator.checkParam_int_positiveOrZero(offset_sec)

        # 获取期望的时间戳范围
        expect_timestamp = TimeHelper.get_timestamp_from_time(expect_time)
        floor_actual_timestamp = expect_timestamp - offset_sec
        ceil_actual_timestamp = expect_timestamp + offset_sec

        # 获取到实际的时间戳
        actual_timestamp = TimeHelper.get_timestamp_from_time(actual_time)

        with allure.step('结果校验：{}, 其允许时间误差范围是 {}秒'.format(desc_msg,offset_sec)):
            AllureHelper.attachText("", "期望时间点：{}".format(TimeHelper.get_time_from_timestamp(expect_timestamp)))
            AllureHelper.attachText("", "实际时间点：{}".format(actual_time))
            assert actual_timestamp >= floor_actual_timestamp and actual_timestamp <= ceil_actual_timestamp

class StringHelper():

    @staticmethod
    def get_random_phoneno():
        """
        功能：随机生成一个手机号
        :return: 一个手机号码
        """
        headList = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                    "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
                    "186", "187", "188", "189"]
        return (random.choice(headList) + "".join(random.choice("0123456789") for i in range(8)))

    @staticmethod
    def get_random_normalString(length=5):
        """
        功能：随机返回一个普通字符串，字符串可能包含：大小写字母，数字
        :param length: 字符串的长度，默认长度为5
        :return: 一个字符串
        """

        validator.check_paramType_int(length)

        charset_str = string.ascii_letters+string.digits
        return "".join(random.choice(charset_str) for _ in range(length))

    @staticmethod
    def get_random_letterString(length=5):
        """
        功能：随机返回一个普通字符串，字符串可能包含：大小写字母
        :param length: 字符串的长度，默认长度为5
        :return: 一个字符串
        """

        validator.check_paramType_int(length)

        charset_str = string.ascii_letters
        return "".join(random.choice(charset_str) for _ in range(length))

    @staticmethod
    def get_random_numberString(length=5):
        """
        功能：随机返回一个数字字符串
        :param length: 字符串的长度，默认长度为5
        :return: 一个数字字符串
        """

        validator.check_paramType_int(length)
        # TODO(dongjun): 校验length为大于0的数

        digits_str = string.digits

        if length == 1:
            return random.choice(digits_str)

        header_str = digits_str[1:]
        return random.choice(header_str) + "".join(random.choice(digits_str) for _ in range(length-1))

    @staticmethod
    def get_random_fixedRange_digit(start_int:int, end_int:int):
        '''
        功能: 指定数字范围内, 随机获取一个数字
        :param start_int: 数字范围的起始值
        :param end_int: 数字范围的结束值
        :return:
        '''

        validator.check_paramType_int(start_int, end_int)

        return random.randint(start_int, end_int)

    @staticmethod
    def get_random_email():
        """
        功能：随机生成一个邮箱
        :return: 一个邮箱
        """
        email_suffix_list = ["@qq.com", "@163.com", "@126.com","@reconova.cn"]
        email_suffix = random.choice(email_suffix_list)

        _lenth = random.randint(4,10)
        email_prefix = StringHelper.get_random_normalString(_lenth)
        return email_prefix + email_suffix

    # TODO(dongjun): 判断一个字符串是不是web域名

    # TODO(dongjun): 判断一个字符串是不是合法的ip+端口

        # 随机的数字组合
        # @staticmethod
        # def random_digit(length):
        #     slcNum = [random.choice(string.digits) for i in range(length)]
        #     random.shuffle(slcNum)
        #     getPwd = ''.join([i.lower() for i in slcNum])
        #     return getPwd

        # 随机数字+小写字母

    @staticmethod
    def random_string(length):
        Ofnum = random.randint(1, length)
        Ofletter = length - Ofnum
        slcNum = [random.choice(string.digits) for i in range(Ofnum)]
        slcLetter = [random.choice(string.ascii_letters) for i in range(Ofletter)]
        slcChar = slcLetter + slcNum
        random.shuffle(slcChar)
        getPwd = ''.join([i.lower() for i in slcChar])
        return getPwd

    # 随机的数字组合
    @staticmethod
    def random_digit(start_int,end_int):

        # 入参校验：start_int
        if not isinstance(start_int, int):
            raise exceptions.ParamNotIntType("参数不是int类型：{}".format(start_int))
        # 入参校验：end_int
        if not isinstance(end_int, int):
            raise exceptions.ParamNotIntType("参数不是int类型：{}".format(end_int))

        return random.randint(start_int,end_int)

class ConfigHelper():

    def __init__(self, file_path):

        self.file_path = file_path
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("请确保配置文件存在！")

        self.cfg = self._read_cfg()

    def _read_cfg(self):
        read_cfg = configparser.ConfigParser()
        read_cfg.read(self.file_path, encoding=_DEFAULT_ENCODING_UTF8)
        return read_cfg

    def get_value(self, title, key):
        try:
            value = self.cfg.get(title, key)
        except:
            value = None
        return value

    def set_value(self, title, key, value):
        self.cfg.set(title, key, value)
        with open(self.file_path, "w+") as f:
            return self.cfg.write(f)

class ListHelper():

    @staticmethod
    def split_bigList(big_list, small_list_len):
        '''
        功能：依据指定小列表长度，将1个大列表拆分成多个小列表
        :param big_list: 大列表
        :param small_list_len: 每个小列表的长度
        :return:
        '''

        validator.check_paramType_list(big_list)
        validator.check_int_gt_zero(small_list_len)

        list_of_groups = zip(*(iter(big_list),) *small_list_len)
        end_list = [list(i) for i in list_of_groups]
        count = len(big_list) % small_list_len
        end_list.append(big_list[-count:]) if count != 0 else end_list
        return end_list

class ImageHelper():

    @staticmethod
    def pic_to_base64(pic_path):
        """
        功能：将1张图片转base64码
        :param pic_path: 图片的绝对路径
        :return: 图片的base64码
        """
        with open(pic_path, 'rb') as fp:
            return base64.b64encode(fp.read()).decode("utf-8")

    @staticmethod
    def pic_to_bytes(pic_path):
        """
        功能：将1张图片转字节码
        :param pic_path: 图片的绝对路径
        :return: 图片的字节码
        """
        with open(pic_path, 'rb') as fp:
            return fp.read()

    @staticmethod
    def base64_to_pic(base64_str, pic_name):
        """
        功能：将base64码转图片
        :param base64_str: 图片的base64编码
        :param pic_name: 图片的名称
        :return:
        """
        with open(pic_name, "wb") as f:
            f.write(base64.b64decode(base64_str))

class DictHelper():
    pass

class CsvHelper():

    @staticmethod
    def load_csv_file(filepath, encoding=_DEFAULT_ENCODING_UTF8):
        """
        读csv文件返回一个列表
        csv内容转换逻辑说明：
            1. 所有内容都会自动去左右空格；
            2. 如果csv内容为空，返回None
            3. 如果csv内容为字典字符串, 返回一个字典
            4. 如果csv内容为列表字符串, 返回一个列表
            5. 如果csv内容为False,false,f,F，返回False
            6. 如果csv内容为True,true,t,T，返回True
            7. 如果csv内容为e,empty，返回空字符串""
        :param filepath: csv文件
        :param encoding: 默认使用utf8
        :return: 返回一个字典元素的列表
        """
        # TODO(dongjun): 将一个数值字符串转成实际的数值(正整数，负整数，正小数，负小数)
        data_ret = []
        with open(filepath, encoding=encoding, mode='r') as csv_file:
            csv_dict = csv.DictReader(csv_file)

            for row in csv_dict:
                row_dict = {}
                for key in row.keys():
                    tmp_value =  row.get(key)

                    if not tmp_value:
                        row_dict[key] = None
                        continue

                    tmp_value = tmp_value.strip()

                    row_dict[key] = tmp_value
                data_ret.append(row_dict)

        return data_ret

if __name__ == '__main__':
    pass