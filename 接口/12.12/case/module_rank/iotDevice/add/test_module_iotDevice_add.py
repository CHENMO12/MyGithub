# -*- coding: utf-8 -*-
# @Time : 2019-11-12 19:41:15

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

@pytest.fixture(scope="function", name="已使用_IOT设备信息")
def depend_iotDevice_info():
    with allure.step("前置条件: 注册IOT设备"):
        info = api_admin.scn_iotDevice_add()
        deviceId = info["deviceId"]

    yield info

    with allure.step("清理前置条件: 删除IOT设备"):
        api_admin.scn_iotDevice_delete(deviceId)

@allure.feature("IOT设备管理")
@allure.story("注册设备")
class TestIotdeviceAdd(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功注册1台设备_瑞为店计设备(self):

        with allure.step('准备用例入参'):
            
            deviceType = 0
            manufacturerType = 0
            deviceCode = testdata.random_iotDevice_deviceCode()
            deviceBarCode = testdata.random_iotDevice_deviceBarCode()
            hardwareVersion = testdata.random_iotDevice_hardwareVersion()
            lensType = testdata.random_iotDevice_lensType()

        with allure.step('接口请求'):
            
            res_info = api_admin.bns_iotDevice_add(
                
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
            # 每个关联业务写成一个step
            pass   

        with allure.step('清理用例'):

            list_info = api_admin.bns_iotDevice_list(pageNo=1, pageSize=20, deviceCodeOrBar=deviceCode)
            deviceId = JsonHelper.parseJson_by_objectpath(list_info, "$..*[@.id]", res_firstOne=True)
            api_admin.scn_iotDevice_delete(deviceId=deviceId)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败注册1台设备_设备编码已存在(self, 已使用_IOT设备信息):

        with allure.step('准备用例入参'):
            deviceType = 0
            manufacturerType = 0
            deviceCode = 已使用_IOT设备信息["deviceCode"]
            deviceBarCode = testdata.random_iotDevice_deviceBarCode()
            hardwareVersion = testdata.random_iotDevice_hardwareVersion()
            lensType = testdata.random_iotDevice_lensType()

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_add(

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
    def test_反测_失败注册1台设备_设备条码已存在(self, 已使用_IOT设备信息):

        with allure.step('准备用例入参'):
            deviceType = 0
            manufacturerType = 0
            deviceCode = testdata.random_iotDevice_deviceCode()
            deviceBarCode = 已使用_IOT设备信息["deviceBarCode"]
            hardwareVersion = testdata.random_iotDevice_hardwareVersion()
            lensType = testdata.random_iotDevice_lensType()

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_add(

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

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败注册1台设备_版本号不存在(self):

        with allure.step('准备用例入参'):
            deviceType = 0
            manufacturerType = 0
            deviceCode = testdata.random_iotDevice_deviceCode()
            deviceBarCode = testdata.random_iotDevice_deviceBarCode()
            hardwareVersion = "D598653642"
            lensType = testdata.random_iotDevice_lensType()

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_add(

                deviceType=deviceType,
                manufacturerType=manufacturerType,
                deviceCode=deviceCode,
                deviceBarCode=deviceBarCode,
                hardwareVersion=hardwareVersion,
                lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 3010
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败注册1台设备_镜头类型不存在(self,):

        with allure.step('准备用例入参'):
            deviceType = 0
            manufacturerType = 0
            deviceCode = testdata.random_iotDevice_deviceCode()
            deviceBarCode = testdata.random_iotDevice_deviceBarCode()
            hardwareVersion = testdata.random_iotDevice_hardwareVersion()
            lensType = "9547684"

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_add(

                deviceType=deviceType,
                manufacturerType=manufacturerType,
                deviceCode=deviceCode,
                deviceBarCode=deviceBarCode,
                hardwareVersion=hardwareVersion,
                lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 3011
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败注册1台设备_设备类型不存在(self,):

        with allure.step('准备用例入参'):
            deviceType = 9547684
            manufacturerType = 0
            deviceCode = testdata.random_iotDevice_deviceCode()
            deviceBarCode = testdata.random_iotDevice_deviceBarCode()
            hardwareVersion = testdata.random_iotDevice_hardwareVersion()
            lensType = "9547684"

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_add(

                deviceType=deviceType,
                manufacturerType=manufacturerType,
                deviceCode=deviceCode,
                deviceBarCode=deviceBarCode,
                hardwareVersion=hardwareVersion,
                lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 3018
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败注册1台设备_厂商类型不存在(self,):

        with allure.step('准备用例入参'):
            deviceType = 0
            manufacturerType = 9547684
            deviceCode = testdata.random_iotDevice_deviceCode()
            deviceBarCode = testdata.random_iotDevice_deviceBarCode()
            hardwareVersion = testdata.random_iotDevice_hardwareVersion()
            lensType = "9547684"

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_add(

                deviceType=deviceType,
                manufacturerType=manufacturerType,
                deviceCode=deviceCode,
                deviceBarCode=deviceBarCode,
                hardwareVersion=hardwareVersion,
                lensType=lensType,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                expect_code = 3018
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

