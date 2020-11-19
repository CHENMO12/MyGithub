# -*- coding: utf-8 -*-
# @Time : 2019-11-21 14:24:12
from base.decorators import allure_attach
from bns.dkyj import BusinessApi


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_memberlevel = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("新增会员级别")
    def bns_memberlevel_add(self, headers=None, brandCode=None, brandId=None, levelName=None):
        '''

        :param headers:
        :param brandCode: 品牌编码
        :param brandId: 品牌id
        :param levelName: 会员级别名称
        :return:
        '''

        api_info = self._config_memberlevel["add"]
        
        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]
        
        # 请求入参
        data = {
            http_data["brandCode"]: brandCode,
			http_data["brandId"]: brandId,
			http_data["levelName"]: levelName,
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

    @allure_attach("会员级别列表")
    def bns_memberlevel_list(self, headers=None, brandId=None):
        '''
        :param headers:
        :param brandId: 品牌id
        :return:
        '''

        api_info = self._config_memberlevel["list"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["brandId"]: brandId,
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

    @allure_attach("删除会员级别")
    def bns_memberlevel_delete(self, headers=None, brandId=None, memberlevelId=None):
        '''

        :param headers:
        :param brandId: 品牌id
        :param memberlevelId: 会员级别id
        :return:
        '''

        api_info = self._config_memberlevel["delete"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["brandId"]: brandId,
            http_data["memberlevelId"]: memberlevelId,
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
        
