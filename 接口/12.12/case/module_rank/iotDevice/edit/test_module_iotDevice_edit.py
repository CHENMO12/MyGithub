# -*- coding: utf-8 -*-
# @Time : 2019-11-12 19:42:21

import pytest
import allure

from case import BaseCase
from bns.iot.iotapi import IotApi    # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
import testdata                     # 可随机化的简单参数
from case import utils              # 可复用的用例步骤

#### tmp use ####
api_admin = IotApi(username=None,password=None)
#### tmp use ####

@pytest.fixture(scope="function", name="待编辑_IOT设备信息")
def depend_iotDevice_info():
    with allure.step("前置条件: 注册IOT设备"):
        info = api_admin.scn_iotDevice_add()
        deviceId = info["deviceId"]

    yield info

    with allure.step("清理前置条件: 删除IOT设备"):
        api_admin.scn_iotDevice_delete(deviceId)

@allure.feature("IOT设备管理")
@allure.story("编辑设备")
class TestIotdeviceEdit(BaseCase):

    @pytest.fixture(scope="function", name="已使用_IOT设备信息")
    def depend_iotDevice_info(self):
        with allure.step("前置条件: 注册IOT设备"):
            info = api_admin.scn_iotDevice_add()
            deviceId = info["deviceId"]

        yield info

        with allure.step("清理前置条件: 删除IOT设备"):
            api_admin.scn_iotDevice_delete(deviceId)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功编辑IOT设备_编辑设备编码(self, 待编辑_IOT设备信息):

        with allure.step('准备用例入参'):
            
            deviceId = 待编辑_IOT设备信息["deviceId"]
            deviceType = 待编辑_IOT设备信息["deviceType"]
            manufacturerType = 待编辑_IOT设备信息["manufacturerType"]
            deviceCode = testdata.random_iotDevice_deviceCode()
            deviceBarCode = 待编辑_IOT设备信息["deviceBarCode"]
            hardwareVersion = 待编辑_IOT设备信息["hardwareVersion"]
            lensType = 待编辑_IOT设备信息["lensType"]

        with allure.step('接口请求'):
            
            res_info = api_admin.bns_iotDevice_edit(
                
                deviceid=deviceId,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				deviceCode=deviceCode,
				deviceBarCode=deviceBarCode,
				hardwareVersion=hardwareVersion,
				lensType=lensType,
            
            )

        with allure.step('校验:接口响应信息'):
        
            with allure.step('校验:接口状态码'):
                expect_code = 0
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

        with allure.step('校验:关联业务'):

            with allure.step('校验: 设备详情接口'):
                actual_value = api_admin.bns_iotDevice_detail(deviceId=deviceId)
                expect_value = deviceCode
                self.assert_actual_contain_expect("编辑后的值被[设备详情接口]包含", actual_value, expect_value)

            with allure.step('校验: 设备列表接口'):
                actual_value = api_admin.bns_iotDevice_list(pageNo=1, pageSize=20, deviceCodeOrBar=deviceCode)
                expect_value = deviceCode
                self.assert_actual_contain_expect("编辑后的值被[设备列表接口]包含", actual_value, expect_value)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功编辑IOT设备_编辑设备条码(self, 待编辑_IOT设备信息):

        with allure.step('准备用例入参'):

            deviceId = 待编辑_IOT设备信息["deviceId"]
            deviceType = 待编辑_IOT设备信息["deviceType"]
            manufacturerType = 待编辑_IOT设备信息["manufacturerType"]
            deviceCode = 待编辑_IOT设备信息["deviceCode"]
            deviceBarCode = testdata.random_iotDevice_deviceBarCode()
            hardwareVersion = 待编辑_IOT设备信息["hardwareVersion"]
            lensType = 待编辑_IOT设备信息["lensType"]

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_edit(

                deviceid=deviceId,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				deviceCode=deviceCode,
				deviceBarCode=deviceBarCode,
				hardwareVersion=hardwareVersion,
				lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 0
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

        with allure.step('校验:关联业务'):

            with allure.step('校验: 设备详情接口'):
                actual_value = api_admin.bns_iotDevice_detail(deviceId=deviceId)
                expect_value = deviceBarCode
                self.assert_actual_contain_expect("编辑后的值被[设备详情接口]包含", actual_value, expect_value)

            with allure.step('校验: 设备列表接口'):
                actual_value = api_admin.bns_iotDevice_list(pageNo=1, pageSize=20, deviceCodeOrBar=deviceCode)
                expect_value = deviceBarCode
                self.assert_actual_contain_expect("编辑后的值被[设备列表接口]包含", actual_value, expect_value)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功编辑IOT设备_编辑硬件版本(self, 待编辑_IOT设备信息):

        with allure.step('准备用例入参'):

            deviceId = 待编辑_IOT设备信息["deviceId"]
            deviceType = 待编辑_IOT设备信息["deviceType"]
            manufacturerType = 待编辑_IOT设备信息["manufacturerType"]
            deviceCode = 待编辑_IOT设备信息["deviceCode"]
            deviceBarCode = 待编辑_IOT设备信息["deviceBarCode"]
            hardwareVersion = testdata.random_iotDevice_hardwareVersion()
            lensType = 待编辑_IOT设备信息["lensType"]

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_edit(

                deviceid=deviceId,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				deviceCode=deviceCode,
				deviceBarCode=deviceBarCode,
				hardwareVersion=hardwareVersion,
				lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 0
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

        with allure.step('校验:关联业务'):

            with allure.step('校验: 设备详情接口'):
                actual_value = api_admin.bns_iotDevice_detail(deviceId=deviceId)
                expect_value = hardwareVersion
                self.assert_actual_contain_expect("编辑后的值被[设备详情接口]包含", actual_value, expect_value)

            with allure.step('校验: 设备列表接口'):
                actual_value = api_admin.bns_iotDevice_list(pageNo=1, pageSize=20, deviceCodeOrBar=deviceCode)
                expect_value = hardwareVersion
                self.assert_actual_contain_expect("编辑后的值被[设备列表接口]包含", actual_value, expect_value)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功编辑IOT设备_编辑镜头型号(self, 待编辑_IOT设备信息):

        with allure.step('准备用例入参'):

            deviceId = 待编辑_IOT设备信息["deviceId"]
            deviceType = 待编辑_IOT设备信息["deviceType"]
            manufacturerType = 待编辑_IOT设备信息["manufacturerType"]
            deviceCode = 待编辑_IOT设备信息["deviceCode"]
            deviceBarCode = 待编辑_IOT设备信息["deviceBarCode"]
            hardwareVersion = 待编辑_IOT设备信息["hardwareVersion"]
            lensType = testdata.random_iotDevice_lensType()

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_edit(

                deviceid=deviceId,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				deviceCode=deviceCode,
				deviceBarCode=deviceBarCode,
				hardwareVersion=hardwareVersion,
				lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 0
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

        with allure.step('校验:关联业务'):

            with allure.step('校验: 设备详情接口'):
                actual_value = api_admin.bns_iotDevice_detail(deviceId=deviceId)
                expect_value = "'lensType': '{}'".format(lensType)
                self.assert_actual_contain_expect("编辑后的值被[设备详情接口]包含", actual_value, expect_value)

            with allure.step('校验: 设备列表接口'):
                actual_value = api_admin.bns_iotDevice_list(pageNo=1, pageSize=20, deviceCodeOrBar=deviceCode)
                expect_value = "'lensType': '{}'".format(lensType)
                self.assert_actual_contain_expect("编辑后的值被[设备列表接口]包含", actual_value, expect_value)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败编辑IOT设备_设备编码已存在(self, 待编辑_IOT设备信息, 已使用_IOT设备信息):
        with allure.step('准备用例入参'):
            deviceId = 待编辑_IOT设备信息["deviceId"]
            deviceType = 待编辑_IOT设备信息["deviceType"]
            manufacturerType = 待编辑_IOT设备信息["manufacturerType"]
            deviceCode = 已使用_IOT设备信息["deviceCode"]
            deviceBarCode = 待编辑_IOT设备信息["deviceBarCode"]
            hardwareVersion = 待编辑_IOT设备信息["hardwareVersion"]
            lensType = 待编辑_IOT设备信息["lensType"]

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_edit(

                deviceid=deviceId,
                deviceType=deviceType,
                manufacturerType=manufacturerType,
                deviceCode=deviceCode,
                deviceBarCode=deviceBarCode,
                hardwareVersion=hardwareVersion,
                lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 3004
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败编辑IOT设备_设备条码已存在(self, 待编辑_IOT设备信息, 已使用_IOT设备信息):
        with allure.step('准备用例入参'):
            deviceId = 待编辑_IOT设备信息["deviceId"]
            deviceType = 待编辑_IOT设备信息["deviceType"]
            manufacturerType = 待编辑_IOT设备信息["manufacturerType"]
            deviceCode = 待编辑_IOT设备信息["deviceCode"]
            deviceBarCode = 已使用_IOT设备信息["deviceBarCode"]
            hardwareVersion = 待编辑_IOT设备信息["hardwareVersion"]
            lensType = 待编辑_IOT设备信息["lensType"]

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_edit(

                deviceid=deviceId,
                deviceType=deviceType,
                manufacturerType=manufacturerType,
                deviceCode=deviceCode,
                deviceBarCode=deviceBarCode,
                hardwareVersion=hardwareVersion,
                lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 3005
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)