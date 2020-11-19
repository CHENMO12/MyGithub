# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 16:08
# @Author  : Huizi Cai
import allure
import pytest
import requests
import time
import json
import glob
import os
import random
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


# 总客流，未成单，已成单，未跟进，筛选客户
class TestSelectVipType:
    def setup_class(self):
        self.api = CommonApi()

    def setup_method(self):
        with allure.step('前置条件1：上传三条抓拍数据'):
            # 1.上传三条数据
            # 2.一条已成单，一条未成单
            upload.run()
            time.sleep(5)
            self.api.common_save_trace_info(required_isTrade=0)
            upload.run()
            time.sleep(5)
            self.api.common_save_trace_info(required_isTrade=1)
            upload.run()
            time.sleep(3)

    @allure.feature('接口关联业务逻辑')
    @allure.story('切换客户状态筛选')
    @allure.description("用例名称：总客流，未成单，已成单，未跟进，筛选客户")
    @allure.severity('blocker')
    def test_business_(self):
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
            response_phone = parseJson_by_objectpath(response.json(), "$.*.data.phone")
            # response_areaName = parseJson_by_objectpath(response.json(), "$.*.data.areaName")
            response_areaCode = parseJson_by_objectpath(response.json(), "$.*.data.areaCode")
            response_imagePath = parseJson_by_objectpath(response.json(), "$.*.data.imagePath")
            response_vipType1 = parseJson_by_objectpath(response1.json(), "$.*.data.vipType")
            response_vipType2 = parseJson_by_objectpath(response2.json(), "$.*.data.vipType")
            response_vipType3 = parseJson_by_objectpath(response3.json(), "$.*.data.vipType")
            attachText("", "接口返回的提示信息：{}".format(response_msg))
            attachText("", "接口返回的提示信息：{}".format(response_areaCode))
            # attachText("", "接口返回的提示信息：{}".format(response_areaName))
            attachText("", "接口返回的提示信息：{}".format(response_vipType1))
            attachText("", "接口返回的提示信息：{}".format(response_vipType2))
            attachText("", "接口返回的提示信息：{}".format(response_vipType3))
        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际状态码：{}".format(response_msg))
            attachText("", "期望状vipType：{}".format(-1))
            attachText("", "实际状vipType：{}".format(response_vipType1))
            attachText("", "期望状vipType：{}".format(2))
            attachText("", "实际状vipType：{}".format(response_vipType2))
            attachText("", "期望状vipType：{}".format(3))
            attachText("", "实际状vipType：{}".format(response_vipType3))
            assert expect_msg == response_msg
            assert len(response_phone) != 0
            assert -1 in response_vipType1
            assert 2 in response_vipType2
            assert 3 in response_vipType3


# 上传一张客流标记为非客户之后，统计数量减一
class TestMarkTypeCount:
    def setup_class(self):
        self.api = CommonApi()

    def setup_method(self):
        with allure.step('前置条件1：上传一条抓拍数据'):
            for _ in range(0, 1):
                upload.run()
            time.sleep(5)

    @allure.feature('接口关联业务逻辑')
    @allure.story('标记为非客户-总客流')
    @allure.description("用例名称：上传一张客流标记为非客户之后，统计数量减1")
    @allure.severity('blocker')
    def test_business_(self):
        response = self.api.common_snap_data_count()
        self.api.common_mark_snap_type()
        time.sleep(3)
        response1 = self.api.common_snap_data_count()
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            attachJson(response.json(), '接口的相关参数信息')
            attachJson(response1.json(), '接口的相关参数信息')
        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")
            response_msg1 = parseJson_by_objectpath(response1.json(), "$.message")
            response_count = parseJson_by_objectpath(response.json(), "$.*.data.sumCount")
            response_count1 = parseJson_by_objectpath(response1.json(), "$.*.data.sumCount")
            attachText("", "接口返回的提示信息：{}".format(response_msg))
            attachText("", "接口返回的提示信息：{}".format(response_msg1))
            attachText("", "接口返回的提示信息：{}".format(response_count))
            attachText("", "接口返回的提示信息：{}".format(response_count1))
        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "期望状态码：{}".format(response_msg))
            attachText("", "标记非效客户前的数量：{}".format(response_count))
            attachText("", "标记非效客户后的数量：{}".format(response_count1))
            assert expect_msg == response_msg
            assert response_count == response_count1 + 1


# 上传一张客流去跟进未成单，然后再次上传同一张客流去跟进已成单
class TestAddTraceAgain:
    def setup_class(self):
        self.api = CommonApi()

    def setup_method(self):
        with allure.step('前置条件1：上传一个客流上传两次...'):
            pass

    @allure.feature('会员识别')
    @allure.story('跟进-再次跟进')
    @allure.description("用例名称：初次到访-跟进-再次跟进")
    @allure.severity('blocker')
    def test_business_(self):
        WSI_MASK_PATH = 'F:\\模拟上传数据\\6000_picture'  # 存放图片的文件夹路径
        wsi_mask_paths = glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg'))
        path = random.choice(wsi_mask_paths)
        self.picturePath = path
        upload.run(picture=self.picturePath)
        time.sleep(5)
        self.api.common_save_trace_info(required_isTrade=0)
        time.sleep(5)
        response = self.api.common_datalist()
        time.sleep(5)
        upload.run(picture=path)
        time.sleep(5)
        response2 = self.api.common_datalist()
        time.sleep(5)
        self.api.common_save_trace_info(required_isTrade=1)
        response1 = self.api.common_datalist()
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            attachJson(response.json(), '接口的相关参数信息')
            attachJson(response1.json(), '接口的相关参数信息')
            attachJson(response2.json(), '接口的相关参数信息')

        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")
            response_personName = parseJson_by_objectpath(response.json(), "$.*.data.personName")[0]
            response_msg1 = parseJson_by_objectpath(response1.json(), "$.message")
            response_personName2 = parseJson_by_objectpath(response2.json(), "$.*.data.personName")[0]
            response_vipType = parseJson_by_objectpath(response.json(), "$.*.data.vipType")[0]
            response_vipType1 = parseJson_by_objectpath(response1.json(), "$.*.data.vipType")[0]
            attachText("", "接口返回的提示信息：{}".format(response_msg))
            attachText("", "接口返回的提示信息：{}".format(response_msg1))
            attachText("", "接口返回跟进后的客户姓名：{}".format(response_personName))
            attachText("", "接口返回下次来访识别的客户姓名：{}".format(response_personName2))

        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际返回参数：{}".format(response_vipType))
            attachText("", "期望返回参数：{}".format(2))
            attachText("", "实际返回参数：{}".format(response_vipType1))
            attachText("", "期望返回参数：{}".format(3))
            attachText("", "第一次跟进后的客户名：{}".format(response_personName))
            attachText("", "客户第二次来会员识别的客户名：{}".format(response_personName2))
            assert response_vipType == 2
            assert response_vipType1 == 3
            assert expect_msg == response_msg
            assert expect_msg == response_msg1
            assert response_personName2 == response_personName


# 迭代一关联
class TestRelateCustomer:
    def setup_class(self):
        self.api = CommonApi()

    def setup_method(self):
        with allure.step('前置条件1：上传两条抓拍数据'):
            for _ in range(0, 2):
                upload.run()
            time.sleep(5)

    @allure.feature('关联客户')
    @allure.story('迭代一')
    @allure.description("用例名称：关联客户，成单数+1，我的客户+1")
    @allure.severity('blocker')
    def test_relate_customer(self):
        response = self.api.common_snap_data_count()
        response_donecount01 = parseJson_by_objectpath(response.json(), "$.*.data.doneCount")
        response = self.api.common_relate_customer()
        expect_msg = "添加成功"
        with allure.step('步骤1：发送请求'):
            attachJson(response.json(), '接口的相关参数信息')
        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")

        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            attachText("", "实际返回参数：{}".format(response_msg))
            assert expect_msg == response_msg

        with allure.step('步骤4：后置条件：成单数+1，我的客户+1'):
            response = self.api.common_snap_data_count()
            response_donecount02 = parseJson_by_objectpath(response.json(), "$.*.data.doneCount")
            response = self.api.common_my_customer()
            response_personName01 = parseJson_by_objectpath(response.json(), "$.*.data.personName")
            attachText("", "期望返回成单数：{}".format(response_donecount01))
            attachText("", "实际返回成单数：{}".format(response_donecount02))
            attachText("", "期望返回客户姓名：{}".format(self.api.personName02))
            attachText("", "实际返回客户姓名：{}".format(response_personName01))
            assert response_donecount02 == response_donecount01 + 1
            assert self.api.personName02 in response_personName01


# 上传一张客流标记为无效客户后，恢复为客流，然后去跟进
class TestResumeCustomer:
    def setup_class(self):
        self.api = CommonApi()

    def setup_method(self):
        with allure.step('前置条件1：上传一条抓拍数据'):
            for _ in range(0, 1):
                upload.run()
            time.sleep(5)

    @allure.feature('接口关联业务逻辑')
    @allure.story('标记为无效客户客户-总客流')
    @allure.description("用例名称：上传一张客流标记为无效客户之后，恢复为客流，去跟进")
    @allure.severity('blocker')
    def test_business_(self):
        self.api.common_mark_snap_type(required_vipType=1)
        response = self.api.common_resume_first_customer()
        expect_msg = "请求成功"
        with allure.step('步骤1：发送请求'):
            attachJson(response.json(), '接口的相关参数信息')
            # attachJson(response1.json(), '接口的相关参数信息')
        with allure.step('步骤2：获取响应信息'):
            response_msg = parseJson_by_objectpath(response.json(), "$.message")

        with allure.step('步骤3：检查点校验'):
            attachText("", "期望状态码：{}".format(expect_msg))
            assert expect_msg == response_msg

        with allure.step('后置条件：去跟进'):
            expect_msg = "添加成功"
            with allure.step('步骤1：发送请求'):
                response = self.api.common_save_trace_info()
                attachJson(response.json(), '接口的相关参数信息')
            with allure.step('步骤2：获取响应信息'):
                response_msg = parseJson_by_objectpath(response.json(), "$.message")
            with allure.step('步骤3：检查点校验'):
                attachText("", "期望状态码：{}".format(expect_msg))
                attachText("", "实际状态码：{}".format(response_msg))
            assert expect_msg == response_msg
