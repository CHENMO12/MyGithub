#!/usr/bin/python3.7
# @Time : 2020/5/27 0027 14:51 
# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 14:24
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : __init__.py

"""
    解决平台的登录问题
"""
from bns import BaseApi
from base.helper import JsonHelper, EncryptHelper
from base.logger import Logger
import config
import requests
import json


class BusinessApi(BaseApi):
    """
        平台登录逻辑分析：
            1.登录获取token,登录及后续接口需要在header中增加platformId="4"
            2.将token加入到header中初始化，其他接口调用时使用
    """
    _header = dict()


    def __init__(self, username=None, password=None,headers=None):

        if not username: username = config.get_b2b_username
        if not password: password = config.get_b2b_password
        if headers is None:
            self.headers = {"Content-Type": "application/json;charset=UTF-8"}
        self.username = username
        self.session=requests.session()
        self.log = Logger()
        if len(password) == 32:
            self.password = password
        else:
            self.password = "HGBnGUVR1HvaWkkniwVMvg=="

        self._config = self.base_yaml_info(curr_file=__file__, module_key="b2bUser")

        self._get_header()

    def bns_user_login(self, headers=None):
        '''
        用户登录
        :param headers: 传参选项，可不传使用默认
        :param userName: 登录名,string，必填
        :param userPasswd: 登录密码，string，必填
        :param randStr: 图形验证码的随机字符串，string，选填
        :param ticket: 图形验证的输入值，string，选填
        :return:
        '''

        api_info = self._config["login"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["userName"]: self.username,
            http_data["userPasswd"]: self.password,
            http_data["autoLogin"]: 1,

        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            request_url="{}{}".format(config.get_b2b_host, http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )
        return response

    def _get_header(self):

        # 获取接口信息
        res_login = self.bns_user_login()
        # 处理接口的信息
        access_token = JsonHelper.parseJson_by_objectpath(res_login, "$..token", res_firstOne=True)

        # 定义header
        self._header.setdefault('adminAccessToken', access_token)

    def business_request(self, request_url, request_method, request_type, request_data=None, headers=None):

        if headers is None:
            headers = self._header

        return self.base_request(request_method, request_type, request_url, request_data=request_data, auth=None,
                                 headers=headers)

    @property
    def get_headers(self):
        '''
        获取http的头部信息
        :return:
        '''

        return self._header

    def set_headers(self, key, value):
        '''
        设置http的头部信息, 可覆盖原有的key
        :return:
        '''
        self._header[key] = value



if __name__ == '__main__':
    a = BusinessApi()
    b = a.bns_user_login()
    print(b)
