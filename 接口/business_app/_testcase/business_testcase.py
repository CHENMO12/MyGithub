# -*- coding: utf-8 -*-
# @Time    : 2019/7/5 11:24
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
from business_app._api.common_api import CommonApi
from business_app._testcase.data_upload import UploadByNetty

config = Config()
upload = UploadByNetty(config.get_device, config.get_web_domain)


# 客户列表
class TestDataList:
    def setup_class(self):
        self.api = CommonApi()
        self.config = Config()

    def setup_method(self):
        with allure.step('前置条件1：上传一条抓拍数据'):
            for _ in range(0, 1):
                upload.run()
            time.sleep(5)

    @allure.feature('抓拍信息列表')
    @allure.story('抓拍信息列表')
    @allure.description("用例名称：验证回复内容,以及筛选Typevip查询")
    @allure.severity('blocker')
    def test_required_field(self):
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            response = self.api.common_datalist()
            attachJson(response.json(), '接口的相关参数信息')
            response1 = self.api.common_datalist(optional_dataType=1)
            attachJson(response1.json(), '接口的相关参数信息')
            response2 = self.api.common_datalist(optional_dataType=2)
            attachJson(response2.json(), '接口的相关参数信息')
            response3 = self.api.common_datalist(optional_dataType=3)
            attachJson(response3.json(), '接口的相关参数信息')
        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")
            response_areaCode = parseJson_by_objectpath(response.json(), "$.*.data.areaCode")
            response_imagePath = parseJson_by_objectpath(response.json(), "$.*.data.imagePath")

            attachText("", "接口返回的提示信息：{}".format(response_msg))
            attachText("", "接口返回的提示信息：{}".format(response_areaCode))

        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际状态码：{}".format(response_msg))
            attachText("", "返回区域编码：{}".format(response_areaCode))
            attachText("", "返回图片地址：{}".format(response_imagePath))
            assert expect_msg == response_msg
            assert len(response_areaCode) != 0
            assert len(response_imagePath) != 0


class TestSaveTraceInfo:
    def setup_class(self):
        # self.api = BaseApi()
        self.common = CommonApi()
        self.config = Config()

    def setup_method(self):
        with allure.step('前置条件1：上传一条抓拍数据'):
            for _ in range(0, 1):
                upload.run()
            time.sleep(5)

    @allure.feature('去跟进客户')
    @allure.story('去跟进客户')
    @allure.description("用例名称：去跟进客户,验证返回内容")
    @allure.severity('blocker')
    def test_required_field(self):
        expect_msg = "添加成功"
        with allure.step('步骤1：发送请求'):
            response = self.common.common_save_trace_info()
            attachJson(response.json(), '接口的相关参数信息')
        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")
        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际状态码：{}".format(response_msg))
        assert expect_msg == response_msg


# 添加跟进信息
class TestAddTraceInfo:
    def setup_class(self):
        # self.api = BaseApi()
        self.common = CommonApi()
        self.config = Config()

    @allure.feature('添加跟进信息')
    @allure.story('添加跟进信息')
    @allure.description("用例名称：验证新添加的跟进信息")
    @allure.severity('blocker')
    def test_required_field(self):
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            response = self.common.common_add_trace_info()
            attachJson(response.json(), '接口的相关参数信息')

        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")

        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际状态码：{}".format(response_msg))

        assert expect_msg == response_msg


# 我的客户
class TestMyCustomer:
    def setup_class(self):
        # self.api = BaseApi()
        self.common = CommonApi()
        self.config = Config()

    def setup_method(self):
        with allure.step('前置条件1：已跟进一个客户'):
            for _ in range(0, 1):
                upload.run()
            time.sleep(5)
            self.input_personName = random_str()
            res_json = self.common.common_save_trace_info(optional_personName=self.input_personName)
            attachJson(res_json, "接口详细信息")

    @allure.feature('我的客户')
    @allure.story('我的客户')
    @allure.description("用例名称：新跟进一个客户，查看我的客户列表更新")
    @allure.severity('blocker')
    def test_required_field(self):
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            response = self.common.common_my_customer()
            attachJson(response.json(), '接口的相关参数信息')

            with allure.step('步骤2：获取响应信息'):
                response_personName = parseJson_by_objectpath(response.json(), "$.*.data.personName")
                response_msg = parseJson_by_objectpath(response.json(), "$.message")

            with allure.step('步骤3：检查点校验'):
                attachText("", "输入客户姓名：{}".format(self.input_personName))
                attachText("", "返回客户姓名：{}".format(response_personName))
                attachText("", "期望状态码：{}".format(expect_msg))
                attachText("", "实际状态码：{}".format(response_msg))

            assert expect_msg == response_msg
            assert self.input_personName in response_personName


# 修改我的客户
class TestChangeCustomerInfo:
    def setup_class(self):
        # self.api = BaseApi()
        self.common = CommonApi()
        self.config = Config()

    @allure.feature('修改我的客户')
    @allure.story('修改我的客户')
    @allure.description("用例名称：修改我的客户名称电话，查看更新后结果")
    @allure.severity('blocker')
    def test_required_field(self):
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            response = self.common.common_change_customer_info()
            time.sleep(2)
            response2 = self.common.common_my_customer()
            attachJson(response.json(), '接口的相关参数信息')
            attachJson(response2.json(), '接口的相关参数信息')

        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")
            response_personName = parseJson_by_objectpath(response2.json(), "$.*.data.personName")
            response_phone = parseJson_by_objectpath(response2.json(), "$.*.data.phone")

        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际状态码：{}".format(response_msg))
            attachText("", "期望返回客户姓名：{}".format(self.common.personName02))
            attachText("", "实际返回客户姓名：{}".format(response_personName))
            attachText("", "期望返回客户电话：{}".format(self.common.phone02))
            attachText("", "实际返回客户电话：{}".format(response_phone))

        assert expect_msg == response_msg
        assert self.common.personName02 in response_personName
        assert self.common.phone02 in response_phone


# 客流统计
class TestDataCount:
    def setup_class(self):
        # self.api = BaseApi()
        self.common = CommonApi()
        self.config = Config()

    @allure.feature('客流统计')
    @allure.story('客流统计')
    @allure.description("用例名称：查看客流统计数量")
    @allure.severity('blocker')
    def test_required_field(self):
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            response = self.common.common_snap_data_count()
            attachJson(response.json(), '接口的相关参数信息')

        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")
            response_doingcount = parseJson_by_objectpath(response.json(), "$.*.data.doingCount")
            response_donecount = parseJson_by_objectpath(response.json(), "$.*.data.doneCount")
            response_nocount = parseJson_by_objectpath(response.json(), "$.*.data.noCount")
            response_sumcount = parseJson_by_objectpath(response.json(), "$.*.data.sumCount")

        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际状态码：{}".format(response_msg))
            attachText("", "返回跟进数量：{}".format(response_doingcount))
            attachText("", "返回未跟进数量：{}".format(response_nocount))
            attachText("", "返回成单数量：{}".format(response_donecount))
            attachText("", "返回总客流数量：{}".format(response_sumcount))
            assert expect_msg == response_msg
            assert response_sumcount > 0
            assert response_doingcount > 0
            assert response_nocount > 0
            assert response_donecount > 0
            assert response_sumcount >= response_donecount + response_nocount + response_doingcount


# 标记为非客户
class TestMarkSnapType:
    def setup_class(self):
        # self.api = BaseApi()
        self.common = CommonApi()
        self.config = Config()

    def setup_method(self):
        with allure.step('前置条件1：上传一条抓拍数据'):
            for _ in range(0, 1):
                upload.run()
            time.sleep(5)

    def teardown_method(self):
        pass

    @allure.feature('标记为非客户')
    @allure.story('标记为非客户')
    @allure.description("用例名称：上传一张客流标记为非客户")
    @allure.severity('blocker')
    def test_required_field(self):
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            response = self.common.common_mark_snap_type()
            attachJson(response.json(), '接口的相关参数信息')
        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")
        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际状态码：{}".format(response_msg))
            assert expect_msg == response_msg

# 店员业绩
    class TestClerkTradeList:
        def setup_class(self):
            # self.api = BaseApi()
            self.common = CommonApi()
            self.config = Config()

        def setup_method(self):
            pass

        def teardown_method(self):
            pass

        @allure.feature('查看所有店员的业绩')
        @allure.story('查看所有店员的业绩')
        @allure.description("用例名称：查看所有店员的业绩")
        @allure.severity('blocker')
        def test_required_field(self):
            expect_msg = "请求成功"
            with allure.step('步骤1：发送请求'):
                response = self.common.common_clerk_tradelist()
                attachJson(response.json(), '接口的相关参数信息')
            with allure.step('步骤2：获取响应信息'):
                response_msg = parseJson_by_objectpath(response.json(), "$.message")
            with allure.step('步骤3：检查点校验'):
                attachText("", "期望状态码：{}".format(expect_msg))
                attachText("", "实际状态码：{}".format(response_msg))
                assert expect_msg == response_msg