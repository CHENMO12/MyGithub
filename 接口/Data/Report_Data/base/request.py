# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 15:17
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : myrequest.py

import uuid
import ssl
from enum import Enum

import requests
import urllib3
from requests_toolbelt.multipart.encoder import MultipartEncoder

from base import exceptions
from base.logger import Logger
from base.helper import TimeHelper


class Request(object):

    class Method(Enum):
        '''
            请求动作类型
        '''
        GET = 1
        POST = 2
        PUT = 3
        DELETE = 4

    def __init__(self,session=False,verbose=False):

        # 解决控制台输出 InsecureRequestWarning 的问题
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.log = Logger()

        self.headers = {}

        self.verbose = verbose
        self.info = dict()

        if session:
            self.request = requests.session()
        else:
            self.request = requests

    def send_request(self, request_method, request_type, request_url, request_data=None, auth=None, headers=None, cookies=None):
        '''
        功能：http请求的基础方法，支持不同的请求方法，请求类型
        :param request_method: 请求方法
        :param request_type: 请求内容类型
        :param request_url: 请求URL
        :param request_data: 请求数据
        :return:
        '''

        ssl._create_default_https_context = ssl._create_unverified_context

        if self.verbose:
            self.log.log_info("接口请求地址：{}".format(request_url))
        self.info['request_addrPath'] = "/" + "/".join(request_url.split("/")[3:])

        try:
            if self.verbose:
                self.log.log_info("接口请求数据：{}".format(request_data))
            self.info['request_data'] = request_data

            if request_method == "post" and request_type == "urlencoded":
                response = requests.post(url=request_url, data=request_data, headers=headers, auth=auth, cookies=cookies, verify=False)

            elif request_method == "post" and request_type == "json":
                response = requests.post(url=request_url, json=request_data, headers=headers, auth=auth, cookies=cookies, verify=False)

            elif request_method == "put" and request_type == "json":
                response = requests.put(url=request_url, json=request_data, headers=headers, auth=auth, cookies=cookies, verify=False)

            elif request_method == "delete" and request_type == "json":
                response = requests.delete(url=request_url, json=request_data, headers=headers, auth=auth, cookies=cookies, verify=False)

            elif request_method == "post" and request_type == "file":

                data = MultipartEncoder(
                    fields=request_data,
                    boundary="%s" % uuid.uuid4()
                )
                response = self.request.post(url=request_url, data=data, headers=headers, auth=auth, cookies=cookies, verify=False)

            elif request_method == "get" and request_type == "urlencoded":
                response = requests.get(url=request_url, params=request_data, headers=headers, auth=auth, cookies=cookies, verify=False)

            elif request_method == "get" and request_type == "json":
                response = requests.get(url=request_url, params=request_data, headers=headers, auth=auth, cookies=cookies, verify=False)

            else:
                raise exceptions.HttpRequestException("当前的请求方法：{}，请求类型：{}".format(request_method,request_type))

        except Exception as e:
            self.log.log_error("http请求异常：{}".format(e))
            raise exceptions.HttpRequestException("http请求异常")

        self.info['request_header'] = headers
        return self.__setting_response_format(response)

    def __setting_response_format(self, response):

        response_code = response.status_code

        self.info['response_code'] = response_code
        self.info['response_time'] = response.elapsed.total_seconds()
        self.info['local_time'] = TimeHelper.get_time_from_timestamp()
        self.info['response_data'] = response.text
        self.info['response_header'] = dict(response.headers)

        # 进行http的状态码的检测
        '''
            200 请求成功
            401 接口未授权
            404 接口请求地址不存在
            500 接口服务器内部错误
            502 请求失败：接口服务器运行错误：服务是否启动，端口是否可用，网络能否ping通
        '''
        # if response_code == 200 or 201:
        if response_code == 200:

            response_ContentType = response.headers.get("Content-Type")

            if "application/json" in response_ContentType:
                try:
                    self.info['response_data'] = response.json()
                except Exception:
                    self.log.log_error(self.info)
                    raise exceptions.HttpResponseException("请求类型是json，但接口返回内容却不是json格式")
            elif "image" in response_ContentType:
                self.info['response_data'] = response.content
            else:
                self.log.log_warning("响应内容类型不是json也不是image，是其他类型：{}".format(response_ContentType))
                self.info['response_data'] = response.text

            if self.verbose:
                self.log.log_info("接口响应信息：{}".format(self.info['response_data']))

            return self.info

        self.log.log_warning("请求请求地址：{}".format(self.info['request_addrPath']))
        self.log.log_warning("请求响应的http状态码：{}".format(response_code))
        try:
            self.info['response_data'] = response.json()
        except :
            self.info['response_data'] = response.text

        return self.info

if __name__ == '__main__':
    pass
















