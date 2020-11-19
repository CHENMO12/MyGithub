# -*- coding: utf-8 -*-
# @Time : 2019-11-27 15:52:07
from base.decorators import allure_attach
from bns.iot import BusinessApi


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_iotUser = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("添加员工")
    def bns_iotUser_add(self, headers=None, userEmail=None, userName=None, userPhone=None, roleIdsList=None):
        '''
        功能：添加一个IOT员工
        :param headers: 传参选项，可不传使用默认
        :param userEmail:  员工邮箱，string，选填
        :param userName: 员工姓名，string，必填
        :param userPhone: 员工手机号，string，选填
        :param roleIds: 员工关联的角色id，[int]，必填。权限对应（1.平台管理员 2.版本管理员 3.技术支持 4.普通用户 5.技术支持经理）
        :return:
        '''

        api_info = self._config_iotUser["add"]
        
        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]
        
        # 请求入参
        data = {
            http_data["userEmail"]: userEmail,
			http_data["userName"]: userName,
			http_data["userPhone"]: userPhone,
			http_data["roleIdsList"]: roleIdsList,
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
        
    @allure_attach("编辑员工")
    def bns_iotUser_edit(self, headers=None, userEmail=None, userName=None, userPhone=None, roleIdsList=None, userId=None):
        # TODO: 请完成函数注释!!!
        api_info = self._config_iotUser["edit"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["userEmail"]: userEmail,
            http_data["userName"]: userName,
            http_data["userPhone"]: userPhone,
            http_data["roleIdsList"]: roleIdsList,
            http_data["userId"]: userId,
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            # TODO: 请确认url是否需要变化！！！
            request_url="{}{}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

    @allure_attach("删除员工")
    def bns_iotUser_delete(self, headers=None, userId=None):
        '''
        功能：删除一个IOT员工
        :param headers: 传参选项，可不传使用默认
        :param userId:  员工ID，string，必填
        :return:
        '''

        api_info = self._config_iotUser["delete"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["userId"]: userId,
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

    @allure_attach("员工列表")
    def bns_iotUser_list(self, headers=None, userName=None, pageNo=None, pageSize=None):
        '''
        功能：查找员工列表，获取员工信息——createTime/email/name/phone/roles/status
        :param headers: 传参选项，可不传使用默认
        :param userName: 员工姓名，string，选填
        :param pageNo: 分页页码，int，必填
        :param pageSize: 分页大小，int，必填
        :return:
        '''

        api_info = self._config_iotUser["list"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["userName"]: userName,
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