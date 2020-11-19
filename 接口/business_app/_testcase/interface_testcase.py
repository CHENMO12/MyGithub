# -*- coding: utf-8 -*-
# @Time    : 2019/7/5 11:23
# @Author  : Huizi Cai
import allure
import pytest
import requests
import time
import json
import hashlib
from business_app.smartShop_util.myrequest import MyRequest
from business_app.smartShop_util.mycommon import parseJson_by_objectpath, attachJson, attachText
from business_app.smartShop_util.mylog import MyLog
from business_app._config.config import Config
from business_app._api.config import *
from business_app._api.base_api import BaseApi
from business_app._api.common_api import CommonApi


class TestDataList:
    def setup_class(self):
        self.api = BaseApi()

    @allure.feature('抓拍列表数据')
    @allure.story('抓拍列表数据')
    @allure.description("用例名称：验证必填字段")
    @allure.severity('blocker')
    def test_required_field(self):
        expect_msg = "参数token:token不能为空"
        expect_msg2 = "参数areaCode:区域编码不能为空"
        with allure.step('步骤1：发送请求'):
            response = self.api.base_datalist(required_areaCode=self.api.areaCode)
            attachJson(response.json(), '接口的相关参数信息')
            response2 = self.api.base_datalist(required_token=self.api.token)
            attachJson(response2.json(), '接口的相关参数信息')
        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")
            response_msg2 = parseJson_by_objectpath(response2.json(), "$.message")
            attachText("", "接口返回的提示信息：{}".format(response_msg))
            attachText("", "接口返回的提示信息：{}".format(response_msg2))
        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际状态码：{}".format(response_msg))
            attachText("", "期望状态码：{}".format(expect_msg2))
            attachText("", "实际状态码：{}".format(response_msg2))
            assert expect_msg == response_msg
            assert expect_msg2 == response_msg2


