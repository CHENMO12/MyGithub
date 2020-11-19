# -*- coding: utf-8 -*-
# @Time : 2019-11-21 15:39:56
from base.decorators import allure_attach
from bns.dkyj import BusinessApi


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_employee = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("新增店员")
    def bns_employee_add(self, headers=None, mallareaCode=None, employeename=None, phoneNo=None, faceId=None, imagePath=None, sex=None, age=None, remark=None):
        '''

        :param headers:
        :param mallareaCode: 门店编码
        :param employeename: 店员姓名
        :param phoneNo: 手机号码
        :param faceId: 人脸faceId
        :param imagePath: 图片路径
        :param sex: 性别
        :param age: 年龄
        :param remark: 备注
        :return:
        '''

        api_info = self._config_employee["add"]
        
        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]
        
        # 请求入参
        data = {
            http_data["mallareaCode"]: mallareaCode,
			http_data["employeename"]: employeename,
			http_data["phoneNo"]: phoneNo,
			http_data["faceId"]: faceId,
			http_data["imagePath"]: imagePath,
			http_data["sex"]: sex,
			http_data["age"]: age,
			http_data["remark"]: remark,
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
        
