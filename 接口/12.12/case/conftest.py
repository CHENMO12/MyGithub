# -*- coding: utf-8 -*-
# @Time    : 2019/8/30 13:56
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : conftest.py

import pytest
import allure

from bns.b2b.api import Api    # 业务api的调用入口

from testdata import fixed_bnsData
from base.helper import JsonHelper

api_admin = Api(username=None,password=None)
iot_api_admin = IotApi(username=None,password=None)
public_api_admin = PublicApi(username=None,password=None)

# iot的技术支持api
@pytest.fixture(scope="module")
def iot_api_technicalSupport():

    with allure.step('IOT平台管理员：注册技术支持账号'):

        info = iot_api_admin.scn_iotUser_add_techSupoort()
        userPhone = info["userPhone"]
        userPassword = info["userPassword"]
        userId = info["userId"]

    with allure.step('登录技术支持账号'):

        iot_api_technicalSupport = IotApi(username=userPhone, password=userPassword)

    yield iot_api_technicalSupport

    with allure.step('删除技术支持账号'):
        iot_api_admin.bns_iotUser_delete(userId=userId)

# dkyj的技术支持api
@pytest.fixture(scope="module")
def api_technicalSupport():

    with allure.step('店客云及平台管理员：注册技术支持账号'):

        info = api_admin.scn_operateUser_add_techSupport()
        userPhone = info["userPhone"]
        userId = info["userId"]

    with allure.step('登录技术支持账号'):

        api_technicalSupport = Api(username=userPhone, password="Dj123456")

    yield api_technicalSupport

    with allure.step('删除技术支持账号'):

        api_admin.bns_operateUser_delete(userId=userId)

@pytest.fixture(scope="function", name="关联_IOT设备信息")
def depend_iotDevice_info():
    with allure.step("前置条件1: 注册IOT设备"):
        info = public_api_admin.scn_publicDevice_add()
        deviceCode = info["deviceCode"]

    with allure.step("前置条件2: 启用设备"):
        iot_api_admin.bns_iotDevice_enable(deviceCodeList=[deviceCode])
        list_info = iot_api_admin.bns_iotDevice_list(deviceCodeOrBar=deviceCode)
        deviceId = JsonHelper.parseJson_by_objectpath(list_info,"$..*[@.id]")[0]

    yield info
    with allure.step("清理前置条件:审批下架设备申请"):
        iot_api_admin.scn_iotDevice_apply(deviceId)
    with allure.step("在公共服务中删除设备"):
        public_api_admin.bns_publicDevice_delete(deviceCode)

@pytest.fixture(scope="function", name="关联_品牌节点")
def depend_brandNode():
    with allure.step("前置条件: 添加品牌节点"):
        info = api_admin.scn_node_addBrand(parentAreaCode="0002")
        areaCode = info["areaCode"]

    yield info

    with allure.step("清理前置条件: 删除品牌节点"):
        api_admin.bns_node_delete(areaCode=areaCode)

@pytest.fixture(scope="function", name="关联_门店节点")
def depend_shopNode(关联_品牌节点):
    with allure.step("前置条件: 添加门店节点"):
        info = api_admin.scn_node_addShop(parentAreaCode=关联_品牌节点["areaCode"])
        areaCode = info["areaCode"]

    yield info

    with allure.step("清理前置条件: 删除门店节点"):
        api_admin.bns_node_delete(areaCode=areaCode)

@pytest.fixture(scope="function", name="关联_门店节点2")
def depend_shopNode2(关联_品牌节点):
    with allure.step("前置条件: 添加门店节点"):
        info = api_admin.scn_node_addShop(parentAreaCode=关联_品牌节点["areaCode"])
        areaCode = info["areaCode"]

    yield info

    with allure.step("清理前置条件: 删除门店节点"):
        api_admin.bns_node_delete(areaCode=areaCode)


@pytest.fixture(scope="function", name="关联_抓拍子节点_进店")
def depend_logicNode(关联_门店节点):
    with allure.step("前置条件: 添加抓拍子节点"):
        info = api_admin.scn_node_addLogic(parentAreaCode=关联_门店节点["areaCode"],logicTypeId=fixed_bnsData.LogicTypeId.intoshop.value)
        areaCode = info["areaCode"]

    yield info

    with allure.step("清理前置条件: 删除抓拍子节点"):
        api_admin.bns_node_delete(areaCode=areaCode)

@pytest.fixture(scope="function", name="关联_设备绑定节点")
def depend_addDevice(关联_IOT设备信息, 关联_门店节点, 关联_抓拍子节点_进店):
    with allure.step("前置条件: 设备绑定节点"):
        info = api_admin.scn_device_add(mallAreaCode=关联_门店节点["areaCode"],deviceCodeOrBar = 关联_IOT设备信息["deviceCode"],areaCodesList = [关联_抓拍子节点_进店["areaCode"]])
        deviceCodeOrBar = info["deviceCodeOrBar"]

    yield info

    with allure.step("清理前置条件: 设备解绑"):
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar, areaCode=关联_抓拍子节点_进店["areaCode"])