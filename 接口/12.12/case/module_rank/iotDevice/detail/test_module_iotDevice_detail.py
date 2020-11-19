# -*- coding: utf-8 -*-
# @Time : 2019-11-12 19:42:31

import pytest
import allure

from case import BaseCase
from bns.iot.iotapi import IotApi   # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
import testdata                     # 可随机化的简单参数
from case import utils              # 可复用的用例步骤

#### tmp use ####
api_admin = IotApi(username=None,password=None)
#### tmp use ####


@pytest.fixture(scope="function", name="关联_IOT设备信息")
def depend_iotDevice_info():
    with allure.step("前置条件: 注册IOT设备"):
        info = api_admin.scn_iotDevice_add()
        deviceId = info["deviceId"]

    yield info

    with allure.step("清理前置条件: 删除IOT设备"):
        api_admin.scn_iotDevice_delete(deviceId)


@allure.feature("IOT设备管理")
@allure.story("设备详情")
class TestIotdeviceDetail(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查看设备详情(self, 关联_IOT设备信息):

        with allure.step('准备用例入参'):

            deviceId = 关联_IOT设备信息["deviceId"]

        with allure.step('接口请求'):
            
            res_info = api_admin.bns_iotDevice_detail(
                
                deviceId=deviceId,
            
            )

        with allure.step('校验:接口响应信息'):
        
            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回数据'):

                actual_value = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data")

                expect_deviceCode = "'deviceCode': '{}'".format(关联_IOT设备信息["deviceCode"])
                self.assert_actual_contain_expect("查看返回值: deviceCode", actual_value, expect_deviceCode)

                expect_deviceBarCode = "'deviceBarCode': '{}'".format(关联_IOT设备信息["deviceBarCode"])
                self.assert_actual_contain_expect("查看返回值: deviceBarCode", actual_value, expect_deviceBarCode)

                expect_hardwareVersion = "'hardwareVersion': '{}'".format(关联_IOT设备信息["hardwareVersion"])
                self.assert_actual_contain_expect("查看返回值: hardwareVersion", actual_value, expect_hardwareVersion)

                expect_lensType = "'lensType': '{}'".format(关联_IOT设备信息["lensType"])
                self.assert_actual_contain_expect("查看返回值: lensType", actual_value, expect_lensType)

                expect_manufacturerTypeName = "'manufacturerTypeName': '瑞为'"
                self.assert_actual_contain_expect("查看返回值: manufacturerTypeName", actual_value, expect_manufacturerTypeName)

                expect_deviceTypeName = "'deviceTypeName': '店计'"
                self.assert_actual_contain_expect("查看返回值: deviceTypeName", actual_value, expect_deviceTypeName)

                # 刚在IOT注册完的设备, 去设备状态为: 已注册
                expect_onlineStatusName = "'onlineStatusName': '已注册'"
                self.assert_actual_contain_expect("查看返回值: onlineStatusName", actual_value, expect_onlineStatusName)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败查看设备详情_设备ID不存在(self):

        with allure.step('准备用例入参'):

            deviceId = "99999999"

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_detail(

                deviceId=deviceId,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = -4
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)