# -*-coding: utf-8 -*-
#@Time     : 2019/12/12 10:37
#@Author   : zhongqingqing
#@FileName : bns_api_publicDevice.py
from base.decorators import allure_attach
from bns.public import BusinessApi


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

        self._config_publicDevice = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

        @allure_attach("公共服务注册设备")
        def bns_publicDevice_add(self, headers=None, deviceType=None, manufacturerType=None, deviceCode=None,
                                 deviceBarCode=None, hardwareVersion=None, lensType=None):
            '''
            :param self:
            :param headers:
            :param deviceType:
            :param manufacturerType:
            :param deviceCode:
            :param deviceBarCode:
            :param hardwareVersion:
            :param lensType:
            :return:
            '''

            api_info = self._config_publicDevice["add"]

            http_url = api_info["url"]
            http_port = api_info.get("port")
            http_method = api_info["method"]
            http_contentType = api_info["contentType"]
            http_data = api_info["data"]

            # 请求入参
            data = {
                http_data["deviceType"]: deviceType,
                http_data["manufacturerType"]: manufacturerType,
                http_data["deviceCode"]: deviceCode,
                http_data["deviceBarCode"]: deviceBarCode,
                http_data["hardwareVersion"]: hardwareVersion,
                http_data["lensType"]: lensType,
            }
            data = self.base_filter_data(data)

            # 请求地址
            response = self.business_request(
                # TODO: 请确认url是否需要变化！！！
                request_url="{}{}".format("https://192.168.100.154:8443", http_url),
                request_method=http_method,
                request_type=http_contentType,
                request_data=data,
                headers=headers
            )

            return response

    @allure_attach("公共服务设备注册")
    def bns_publicDevice_add(self, headers=None, deviceType=None, manufacturerType=None, deviceCode=None,
                          deviceBarCode=None, hardwareVersion=None, lensType=None):
        """
        :param headers:
        :param deviceType: 设备类型, 默认: 0
        :param manufacturerType: 厂商类型, 默认: 0
        :param deviceCode: 设备编码, 默认长度: 14
        :param deviceBarCode: 设备条码, 默认长度: 10
        :param hardwareVersion: 硬件版本, 默认: V500001001, V500002001, V500003001
        :param lensType: 镜头型号, 默认: 6, 8, 12, 16
        :return:
        """

        api_info = self._config_publicDevice["add"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceType"]: deviceType,
            http_data["manufacturerType"]: manufacturerType,
            http_data["deviceCode"]: deviceCode,
            http_data["deviceBarCode"]: deviceBarCode,
            http_data["hardwareVersion"]: hardwareVersion,
            http_data["lensType"]: lensType,
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            # 注册设备采用购物中心的iot平台
            request_url="{}{}".format("https://192.168.100.154:8443", http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

    @allure_attach("公共服务设备列表")
    def bns_publicDevice_list(self, headers=None, deviceBarCode=None, deviceCode=None, deviceType=None,
                              deviceTypeName=None, startTime=None, endTime=None, hardwareVersion=None,
                              isEnable=None, lensType=None, manufacturerType=None, manufacturerTypeName=None,
                              pageNo=None, pageSize=None):
        '''
        :param headers:
        :param deviceBarCode: 设备条码
        :param deviceCode: 设备编码
        :param deviceType: 设备类型
        :param deviceTypeName: 设备类型名称
        :param startTime: 查询开始时间
        :param endTime: 查询结束时间
        :param hardwareVersion: 硬件版本号
        :param isEnable: 是否被启用
        :param lensType: 镜头型号
        :param manufacturerType: 厂商
        :param manufacturerTypeName: 厂商名称
        :param pageNo: 页码值
        :param pageSize: 每页条数
        :return:
        '''

        api_info = self._config_publicDevice["list"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceBarCode"]: deviceBarCode,
            http_data["deviceCode"]: deviceCode,
            http_data["deviceType"]: deviceType,
            http_data["deviceTypeName"]: deviceTypeName,
            http_data["startTime"]: startTime,
            http_data["endTime"]: endTime,
            http_data["hardwareVersion"]: hardwareVersion,
            http_data["isEnable"]: isEnable,
            http_data["lensType"]: lensType,
            http_data["manufacturerType"]: manufacturerType,
            http_data["manufacturerTypeName"]: manufacturerTypeName,
            http_data["pageNo"]: pageNo,
            http_data["pageSize"]: pageSize,
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            request_url="{}{}".format("https://192.168.100.154:8443", http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

    @allure_attach("公共服务设备删除")
    def bns_publicDevice_delete(self, headers=None, deviceCode=None):
        '''
        :param headers:
        :param deviceCode: 设备编码
        :return:
        '''

        api_info = self._config_publicDevice["delete"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceCode"]: deviceCode,
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            request_url="{}{}".format("https://192.168.100.154:8443", http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

if __name__ == '__main__':
    api = BnsApi()
    res = api.bns_publicDevice_delete("VzB0GGPjLgGgcj")
    print(res)