# -*- coding: utf-8 -*-
# @Time : 2019-11-11 18:36:33
from base.decorators import allure_attach
from bns.iot import BusinessApi


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_iotDevice = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("设备列表")
    def bns_iotDevice_list(self, headers=None, pageNo=None, pageSize=None, areaCodesList=None, deviceStatus=None,
                           deviceCodeOrBar=None, deviceType=None, manufacturerType=None, lensType=None,
                           hardwareVersion=None, startDateTime=None, endDateTime=None):
        """
        :param headers:
        :param pageNo: 页码
        :param pageSize: 页大小
        :param areaCodesList: 区域列表
        :param deviceStatus: 设备状态
        :param deviceCodeOrBar: 设备编码或条码
        :param deviceType: 设备类型
        :param manufacturerType: 设备厂商
        :param lensType: 镜头型号
        :param hardwareVersion: 硬件版本号
        :param startDateTime: 开始注册时间
        :param endDateTime: 结束注册时间
        :return:
        """

        api_info = self._config_iotDevice["list"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["pageNo"]: pageNo,
            http_data["pageSize"]: pageSize,
            http_data["areaCodesList"]: areaCodesList,
            http_data["deviceStatus"]: deviceStatus,
            http_data["deviceCodeOrBar"]: deviceCodeOrBar,
            http_data["deviceType"]: deviceType,
            http_data["manufacturerType"]: manufacturerType,
            http_data["lensType"]: lensType,
            http_data["hardwareVersion"]: hardwareVersion,
            http_data["startDateTime"]: startDateTime,
            http_data["endDateTime"]: endDateTime,
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

    @allure_attach("编辑设备")
    def bns_iotDevice_edit(self, headers=None, deviceid=None, deviceType=None, manufacturerType=None, deviceCode=None,
                           deviceBarCode=None, hardwareVersion=None, lensType=None):
        """
        不可变参数: deviceid, deviceType, manufacturerType
        :param headers:
        :param deviceid: 设备id--不可编辑
        :param deviceType: 设备类型--不可编辑
        :param manufacturerType: 厂商类型--不可编辑
        :param deviceCode: 设备编码--可编辑
        :param deviceBarCode: 设备条码--可编辑
        :param hardwareVersion: 硬件版本--可编辑
        :param lensType: 镜头类型--可编辑
        :return:
        """

        api_info = self._config_iotDevice["edit"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceId"]: deviceid,
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
            request_url="{}{}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

    @allure_attach("设备详情")
    def bns_iotDevice_detail(self, headers=None, deviceId=None):
        """
        :param headers:
        :param deviceId: 设备id
        :return:
        """

        api_info = self._config_iotDevice["detail"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceId"]: deviceId,
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

    @allure_attach("申请删除设备")
    def bns_iotDevice_applyDelete(self, headers=None, deviceId=None, applyDesc=None, approver=None):
        """
        :param headers:
        :param deviceId: 设备id
        :param applyDesc: 设备下架理由
        :param approver: 审批人
        :return:
        """

        api_info = self._config_iotDevice["applyDelete"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceId"]: deviceId,
            http_data["applyDesc"]: applyDesc,
            http_data["approver"]: approver,
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

    @allure_attach("申请单列表")
    def bns_iotDevice_applyList(self, headers=None, pageNo=None, pageSize=None, applyStatus=None, applyType=None,
                                approver=None, creater=None):
        """
        :param headers:
        :param pageNo: 页码
        :param pageSize: 页大小
        :param applyStatus: 申请单状态: 0审批中，1审批通过，2审批未通过,3作废
        :param applyType: 申请单类型: 0版本上传，1设备删除，2批量升级,3导入升级
        :param approver: 审批人
        :param creater: 发起申请人
        :return:
        """

        api_info = self._config_iotDevice["applyList"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["pageNo"]: pageNo,
            http_data["pageSize"]: pageSize,
            http_data["applyStatus"]: applyStatus,
            http_data["applyType"]: applyType,
            http_data["approver"]: approver,
            http_data["creater"]: creater,
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

    @allure_attach("处理下架申请单")
    def bns_iotDevice_handleApply(self, headers=None, applyId=None, approver=None, approvalStatus=None,
                                  approvalSuggestion=None):
        """
        :param headers:
        :param applyId: 申请单id
        :param approver: 审批人
        :param approvalStatus: 设置审批状态: 1通过,2未通过
        :param approvalSuggestion:
        :return:
        """

        api_info = self._config_iotDevice["handleApply"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["applyId"]: applyId,
            http_data["approver"]: approver,
            http_data["approvalStatus"]: approvalStatus,
            http_data["approvalSuggestion"]: approvalSuggestion,
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

    @allure_attach("设备启用")
    def bns_iotDevice_enable(self, headers=None, deviceCodeList=None):
        '''
        :param headers:
        :param deviceCodeList: 设备编码组
        :return:
        '''

        api_info = self._config_iotDevice["enable"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["deviceCodeList"]: deviceCodeList,
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


