# -*- coding: utf-8 -*-
# @Time : 2019-11-21 14:47:11
from base.decorators import allure_attach
from bns.dkyj import BusinessApi


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_member = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("新增会员")
    def bns_member_add(self, headers=None, mallareaCode=None, membername=None, phoneNo=None, membercardNo=None, memberlevelId=None, faceId=None, imagePath=None, sex=None, age=None):
        '''

        :param headers:
        :param mallareaCode: 门店编码
        :param membername: 会员姓名
        :param phoneNo: 手机号
        :param membercardNo: 会员卡号
        :param memberlevelId: 会员级别Id
        :param faceId: 人脸Id
        :param imagePath: 注册图片的地址
        :param sex: 性别
        :param age: 年龄
        :return:
        '''

        api_info = self._config_member["add"]
        
        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]
        
        # 请求入参
        data = {
            http_data["mallareaCode"]: mallareaCode,
			http_data["membername"]: membername,
			http_data["phoneNo"]: phoneNo,
			http_data["membercardNo"]: membercardNo,
			http_data["memberlevelId"]: memberlevelId,
			http_data["faceId"]: faceId,
			http_data["imagePath"]: imagePath,
			http_data["sex"]: sex,
			http_data["age"]: age,
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

    @allure_attach("查询注册状态")
    def bns_member_status(self, headers=None, shopAreaCode=None, faceId=None, userType=None):
        '''

        :param headers:
        :param shopAreaCode: 门店编码
        :param faceId: 人脸ID
        :param userType: 用户类型(1:会员;2:店员)
        :return:
        '''

        api_info = self._config_member["status"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["shopAreaCode"]: shopAreaCode,
            http_data["faceId"]: faceId,
            http_data["userType"]: userType,
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

