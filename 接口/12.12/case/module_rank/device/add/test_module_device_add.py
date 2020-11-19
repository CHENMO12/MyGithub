# -*- coding: utf-8 -*-
# @Time : 2019-11-14 15:17:59

import pytest
import allure

from case import BaseCase
from bns.dkyj.api import Api    # 业务api的调用入口
from bns.iot.iotapi import IotApi   # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
import testdata                     # 可随机化的简单参数
from case import utils              # 可复用的用例步骤
from testdata import fixed_bnsData

#### tmp use ####
api_admin = Api(username=None,password=None)
iot_api_admin = IotApi(username=None,password=None)
#### tmp use ####

@pytest.fixture(scope="function", name="关联_IOT设备信息")
def depend_iotDevice_info():
    with allure.step("前置条件: 注册IOT设备"):
        info = iot_api_admin.scn_iotDevice_add()
        deviceId = info["deviceId"]

    yield info

    with allure.step("清理前置条件: 删除IOT设备"):
        iot_api_admin.scn_iotDevice_delete(deviceId)

@pytest.fixture(scope="function",name="关联_品牌节点")
def depend_brandNode():
    with allure.step("前置条件: 添加品牌节点"):
        info = api_admin.scn_node_addBrand(parentAreaCode="0002")
        areaCode = info["areaCode"]

    yield info

    with allure.step("清理前置条件: 删除品牌节点"):

        api_admin.bns_node_delete(areaCode=areaCode)
        
@pytest.fixture(scope="function",name="关联_门店节点")
def depend_shopNode(关联_品牌节点):

    with allure.step("前置条件: 添加门店节点"):
        info = api_admin.scn_node_addShop(parentAreaCode=关联_品牌节点["areaCode"])
        areaCode = info["areaCode"]

    yield info

    with allure.step("清理前置条件: 删除门店节点"):

        api_admin.bns_node_delete(areaCode=areaCode)

@pytest.fixture(scope="function",name="关联_抓拍子节点_进店")
def depend_logicNode(关联_门店节点):

    with allure.step("前置条件: 添加抓拍子节点"):
        info = api_admin.scn_node_addLogic(parentAreaCode=关联_门店节点["areaCode"],logicTypeId = fixed_bnsData.LogicTypeId.intoshop.value)
        areaCode = info["areaCode"]

    yield info

    with allure.step("清理前置条件: 删除抓拍子节点"):

        api_admin.bns_node_delete(areaCode=areaCode)


@allure.feature("设备相关")
@allure.story("绑定设备")
class TestDeviceAdd(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功添加设备_绑定在抓拍子节点(self, 关联_IOT设备信息, 关联_抓拍子节点_进店, 关联_门店节点):

        with allure.step('准备用例入参'):
            mallAreaCode = 关联_门店节点["areaCode"]
            deviceCodeOrBar = 关联_IOT设备信息["deviceCode"]
            deviceName = testdata.random_device_deviceName()
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):

            res_info = api_admin.bns_device_add(
                mallAreaCode=mallAreaCode,
                deviceCodeOrBar=deviceCodeOrBar,
				deviceName=deviceName,
				areaCodesList=areaCodesList,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:添加设备接口状态码'):

                expect_code = 0
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:设备列表接口'):

                actual_value = api_admin.bns_device_list(pageNo=1,pageSize=10,deviceCodeOrBar=deviceCodeOrBar)
                expect_value = deviceCodeOrBar
                self.assert_actual_contain_expect("绑定设备后的值被[设备列表接口]包含",actual_value, expect_value)

        with allure.step('解绑设备'):
            api_admin.bns_device_umount(deviceCode=deviceCodeOrBar,areaCode=关联_抓拍子节点_进店["areaCode"])
    