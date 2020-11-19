# -*- coding: utf-8 -*-
# @Time : 2019-11-13 14:27:22
import sys
sys.path.append("../../")
import json

from base.decorators import allure_attach
from bns.dkyj import BusinessApi
import config


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_device = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("绑定设备")
    def bns_device_add(self, mallAreaCode, deviceCodeOrBar, areaCodesList, headers=None, deviceName=None):
        '''
        :param headers:
        :param deviceCodeOrBar: 设备编码/条码
        :param deviceName: 设备名称
        :param areaCodesList: 挂载节点(区域编码为列表形式)
        :return:
        '''

        self.set_headers("areaCode", mallAreaCode)

        api_info = self._config_device["add"]
        
        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]
        
        # 请求入参
        data = {
            http_data["deviceCodeOrBar"]: deviceCodeOrBar,
			http_data["deviceName"]: deviceName,
			http_data["areaCodesList"]: areaCodesList,
        }
        data = self.base_filter_data(data)
        
        # 请求地址
        response = self.business_request(

            request_url="{}{}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

    @allure_attach("设备列表")
    def bns_device_list(self, headers=None, deviceCodeOrBar=None, areaCodesList=None, deviceType=None,
                        onlineStatus=None, pageNo=None, pageSize=None):
        '''

        :param headers:
        :param deviceCodeOrBar: 设备编码/设备条码
        :param areaCodesList: 节点选择
        :param deviceType: 设备类型
        :param onlineStatus: 设备状态, 只包括在线离线, 2-在线,3-离线
        :param pageNo: 页码
        :param pageSize: 每页条数
        :return:
        '''

        api_info = self._config_device["list"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceCodeOrBar"]: deviceCodeOrBar,
            http_data["areaCodesList"]: areaCodesList,
            http_data["deviceType"]: deviceType,
            http_data["onlineStatus"]: onlineStatus,
            http_data["pageNo"]: pageNo,
            http_data["pageSize"]: pageSize,
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            request_url="{}{}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

    @allure_attach("解绑设备")
    def bns_device_umount(self, headers=None, deviceCode=None, areaCode=None):
        '''

        :param headers:
        :param deviceCode: 设备编码
        :param areaCode: 设备绑定的节点
        :return:
        '''

        api_info = self._config_device["umount"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceCode"]: deviceCode,
            http_data["areaCode"]: areaCode,
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(

            request_url="{}{}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

    @allure_attach("设备鉴权")
    def bns_device_auth(self, headers=None, deviceCode=None, data=None):
        '''
        :param headers:
        :param deviceCode: 设备编码
        :param data: 数据加密
        :return:
        '''

        api_info = self._config_device["auth"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceCode"]: deviceCode,
            http_data["data"]: data,
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            request_url="http://{}:8700{}".format(config.get_upload_host, http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response
