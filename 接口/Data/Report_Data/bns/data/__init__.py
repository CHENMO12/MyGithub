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
from config import get_data_host
import config
import requests
import json


class BusinessApi(BaseApi):
    """
        平台登录逻辑分析：
            1.登录获取token,登录及后续接口需要在header中增加platformId="4"
            2.将token加入到header中初始化，其他接口调用时使用
    """

    def __init__(self, username=None, password=None,headers=None,user_type=None,grant_type=None):

        if not username: username = config.get_data_username
        if not password: password = config.get_data_password
        if not user_type: user_type = 1
        if not grant_type: grant_type = password
        if headers is None:
            self.headers = {"Content-Type": "application/json;charset=UTF-8"}
        self.username = username
        self.session = requests.session()
        self.log = Logger()
        if len(password) == 32:
            self.password = password
        else:

            self.password = "6L0dcKga/jz2iJ94rYpnCw=="

        self._config = self.base_yaml_info(curr_file=__file__, module_key="dataUser")

        self._get_header()

    def bns_user_login(self):
        '''
        用户登录
        :param headers: 传参选项，可不传使用默认
        :param userName: 登录名,string，必填
        :param userPasswd: 登录密码，string，必填
        :param autoLogin: 自动登入，选填

        :return:
        '''
        baseapi = BaseApi()
        api_info = baseapi.base_yaml_info(curr_file=__file__, module_key="dataUser")["login"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["userName"]: self.username,
            http_data["userPasswd"]: self.password,
            http_data["user_type"]: 1,
            http_data["grant_type"]: 'password',

        }
        data = baseapi.base_filter_data(data)

        # 请求地址
        response = self.session.post(
            url="{}/sso/sso/oauth/token".format(config.get_data_host),
            data=json.dumps(data),
            headers=self.headers
        )
        return response.headers

    def _get_header(self):

        # # # 获取接口信息
        res_login = self.bns_user_login()
        # 处理接口的信息
        access_cookie = res_login['Set-Cookie']
        # 定义header
        self.headers['Cookie'] = access_cookie[:40]



if __name__ == '__main__':
    a = BusinessApi()

