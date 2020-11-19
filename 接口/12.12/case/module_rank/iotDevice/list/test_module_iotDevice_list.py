# -*- coding: utf-8 -*-
# @Time : 2019-11-12 19:42:26

import pytest
import allure

from case import BaseCase
from bns.iot.iotapi import IotApi    # 业务api的调用入口
from base.helper import JsonHelper, TimeHelper  # json信息提取
import testdata                     # 可随机化的简单参数
from case import utils              # 可复用的用例步骤

#### tmp use ####
api_admin = IotApi(username=None,password=None)
#### tmp use ####


@pytest.fixture(scope="class", name="已注册_IOT设备")
def depend_iotDevice_info():
    with allure.step("前置条件: 注册IOT设备"):
        info = api_admin.scn_iotDevice_add()
        deviceId = info["deviceId"]

    yield info

    with allure.step("清理前置条件: 删除IOT设备"):
        api_admin.scn_iotDevice_delete(deviceId)


@allure.feature("IOT设备管理")
@allure.story("设备列表")
class TestIotdeviceList(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_设备编码(self, 已注册_IOT设备):

        with allure.step('准备用例入参'):
            
            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceCode"]
            deviceType = None
            manufacturerType = None
            lensType = None
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):
            
            res_info = api_admin.bns_iotDevice_list(
                
                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,
            
            )

        with allure.step('校验:接口响应信息'):
        
            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @pytest.mark.skip("目前版本不支持模糊查询")
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_模糊查询设备编码(self, 已注册_IOT设备):

        with allure.step('准备用例入参'):

            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceCode"][2:]
            deviceType = None
            manufacturerType = None
            lensType = None
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_设备条码(self, 已注册_IOT设备):

        with allure.step('准备用例入参'):

            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceBarCode"]
            deviceType = None
            manufacturerType = None
            lensType = None
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @pytest.mark.skip("目前版本不支持模糊查询")
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_模糊查询设备条码(self, 已注册_IOT设备):

        with allure.step('准备用例入参'):

            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceBarCode"][2:]
            deviceType = None
            manufacturerType = None
            lensType = None
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_复合查询_设备条码和设备类型(self, 已注册_IOT设备):

        with allure.step('准备用例入参'):

            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceBarCode"]
            deviceType = 0
            manufacturerType = None
            lensType = None
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_复合查询_设备编码和厂商类型(self, 已注册_IOT设备):
        with allure.step('准备用例入参'):
            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceCode"]
            deviceType = None
            manufacturerType = 0
            lensType = None
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
                pageSize=pageSize,
                areaCodesList=areaCodesList,
                deviceStatus=deviceStatus,
                deviceCodeOrBar=deviceCodeOrBar,
                deviceType=deviceType,
                manufacturerType=manufacturerType,
                lensType=lensType,
                hardwareVersion=hardwareVersion,
                startDateTime=startDateTime,
                endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_复合查询_设备编码和镜头型号(self, 已注册_IOT设备):
        with allure.step('准备用例入参'):
            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceCode"]
            deviceType = None
            manufacturerType = None
            lensType = 已注册_IOT设备["lensType"]
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
                pageSize=pageSize,
                areaCodesList=areaCodesList,
                deviceStatus=deviceStatus,
                deviceCodeOrBar=deviceCodeOrBar,
                deviceType=deviceType,
                manufacturerType=manufacturerType,
                lensType=lensType,
                hardwareVersion=hardwareVersion,
                startDateTime=startDateTime,
                endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_复合查询_设备编码和硬件版本(self, 已注册_IOT设备):
        with allure.step('准备用例入参'):
            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceCode"]
            deviceType = None
            manufacturerType = None
            lensType = None
            hardwareVersion = 已注册_IOT设备["hardwareVersion"]
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
                pageSize=pageSize,
                areaCodesList=areaCodesList,
                deviceStatus=deviceStatus,
                deviceCodeOrBar=deviceCodeOrBar,
                deviceType=deviceType,
                manufacturerType=manufacturerType,
                lensType=lensType,
                hardwareVersion=hardwareVersion,
                startDateTime=startDateTime,
                endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_复合查询_设备编码和注册时间(self, 已注册_IOT设备):

        with allure.step('准备用例入参'):
            pageNo = 1
            pageSize = 20
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = 已注册_IOT设备["deviceCode"]
            deviceType = None
            manufacturerType = None
            lensType = None
            hardwareVersion = None
            startDateTime = TimeHelper.get_custom_time(-3600)
            endDateTime = TimeHelper.get_custom_time(3600)

        with allure.step('接口请求'):
            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
                pageSize=pageSize,
                areaCodesList=areaCodesList,
                deviceStatus=deviceStatus,
                deviceCodeOrBar=deviceCodeOrBar,
                deviceType=deviceType,
                manufacturerType=manufacturerType,
                lensType=lensType,
                hardwareVersion=hardwareVersion,
                startDateTime=startDateTime,
                endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口返回的业务信息条数'):
                expect_count = 1
                actual_count = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.total")
                self.assert_actual_equal_expect("校验筛选查询后列表中内容条数", actual_count, expect_count)

            with allure.step('校验:接口返回的业务信息内容'):
                expect_content = 已注册_IOT设备["deviceCode"]
                actual_content = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list")
                self.assert_actual_contain_expect("校验筛选查询后列表应包含内容", actual_content, expect_content)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_设备类型为店计(self):

        with allure.step('准备用例入参'):
            pageNo = 1
            pageSize = 50
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = None
            deviceType = 0
            manufacturerType = None
            lensType = None
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口内容返回的设备类型'):

                deviceType_list = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list.deviceType")
                actual_count = len(list(set(deviceType_list)))
                expect_count = 1
                self.assert_actual_equal_expect("校验筛选查询后列表中每条业务内容的设备类型均相同", actual_count, expect_count)

                actual_value = deviceType_list.pop()
                expect_value = 0
                self.assert_actual_equal_expect("校验筛选查询后列表中设备类型的值与期望一致", actual_value, expect_value)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_厂商类型为瑞为(self):

        with allure.step('准备用例入参'):
            pageNo = 1
            pageSize = 50
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = None
            deviceType = None
            manufacturerType = 0
            lensType = None
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口内容返回的厂商类型'):

                manufacturerType_list = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list.manufacturerType")
                actual_count = len(list(set(manufacturerType_list)))
                expect_count = 1
                self.assert_actual_equal_expect("校验筛选查询后列表中每条业务内容的厂商类型均为相同", actual_count, expect_count)

                actual_value = manufacturerType_list.pop()
                expect_value = 0
                self.assert_actual_equal_expect("校验筛选查询后列表中厂商类型的值与期望一致", actual_value, expect_value)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_镜头类型(self, 已注册_IOT设备):

        with allure.step('准备用例入参'):
            pageNo = 1
            pageSize = 50
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = None
            deviceType = None
            manufacturerType = None
            lensType = 已注册_IOT设备["lensType"]
            hardwareVersion = None
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口内容返回的镜头类型'):

                manufacturerType_list = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list.lensType")
                actual_count = len(list(set(manufacturerType_list)))
                expect_count = 1
                self.assert_actual_equal_expect("校验筛选查询后列表中每条业务内容的镜头类型均相同", actual_count, expect_count)

                actual_value = manufacturerType_list.pop()
                expect_value = lensType
                self.assert_actual_equal_expect("校验筛选查询后列表中镜头类型的值与期望一致", actual_value, expect_value)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_硬件版本(self, 已注册_IOT设备):

        with allure.step('准备用例入参'):
            pageNo = 1
            pageSize = 50
            areaCodesList = None
            deviceStatus = None
            deviceCodeOrBar = None
            deviceType = None
            manufacturerType = None
            lensType = None
            hardwareVersion = 已注册_IOT设备["hardwareVersion"]
            startDateTime = None
            endDateTime = None

        with allure.step('接口请求'):

            res_info = api_admin.bns_iotDevice_list(

                pageNo=pageNo,
				pageSize=pageSize,
				areaCodesList=areaCodesList,
				deviceStatus=deviceStatus,
				deviceCodeOrBar=deviceCodeOrBar,
				deviceType=deviceType,
				manufacturerType=manufacturerType,
				lensType=lensType,
				hardwareVersion=hardwareVersion,
				startDateTime=startDateTime,
				endDateTime=endDateTime,

            )

        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

            with allure.step('校验:接口内容返回的设备类型'):
                hardwareVersion_list = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.list.hardwareVersion")
                actual_count = len(list(set(hardwareVersion_list)))
                expect_count = 1
                self.assert_actual_equal_expect("校验筛选查询后列表中每条业务内容的硬件版本均为相同", actual_count, expect_count)

                actual_value = hardwareVersion_list.pop()
                expect_value = hardwareVersion
                self.assert_actual_equal_expect("校验筛选查询后列表中硬件版本的值与期望一致", actual_value, expect_value)

    @pytest.mark.skip("需关联区域模块")
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_区域选择_选择一个区域(self):
        pass

    @pytest.mark.skip("需关联区域模块, 需模拟设备登录")
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询设备列表_设备状态_在线或离线(self):
        pass









