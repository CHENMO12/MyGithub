# -*- coding: utf-8 -*-
# @Time : 2019-11-12 19:42:26
import sys
import allure
import pytest

from base.helper import JsonHelper
from bns.iot.iotDevice.bns_api_iotDevice import BnsApi
from case import BaseCase

_testData_list = BaseCase().csv_info(curr_file=__file__)

# 获取api操作对象, 默认权限为平台管理员
api_object_admin = BnsApi()


class TestIotdevice(BaseCase):

    @pytest.mark.parametrize("test_data", _testData_list)
    def test_field_iotDevice_list(self, test_data):

        first_layer = test_data["first_layer"]
        sencod_layer = test_data["sencod_layer"]
        third_layer = test_data["third_layer"]

        if first_layer:
            allure.dynamic.epic(first_layer)
        if sencod_layer:
            allure.dynamic.feature(sencod_layer)
        if third_layer:
            allure.dynamic.story(third_layer)
        
        module_key = sys._getframe().f_code.co_name.split("_")[2]
        test_data = self.parse_csv_param(test_data, module_key)
        
        pageNo = test_data["pageNo"]
        pageSize = test_data["pageSize"]
        areaCodesList = test_data["areaCodesList"]
        deviceStatus = test_data["deviceStatus"]
        deviceCodeOrBar = test_data["deviceCodeOrBar"]
        deviceType = test_data["deviceType"]
        manufacturerType = test_data["manufacturerType"]
        lensType = test_data["lensType"]
        hardwareVersion = test_data["hardwareVersion"]
        startDateTime = test_data["startDateTime"]
        endDateTime = test_data["endDateTime"]
        
        with allure.step("步骤: 请求接口"):

            res_json = api_object_admin.bns_iotDevice_list(
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

        with allure.step("步骤: 提取接口的业务状态码"):
            
            actual_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")

        with allure.step("校验: 业务状态码是否正确"):

            self.assert_actual_equal_expect("业务状态码", actual_code, test_data["expect_code"])

        if test_data["clean_data"]:

            with allure.step("步骤: 数据清理操作"):
                
                # TODO: 调用删除接口
                pass
                
        generator_objs_list = test_data.get("generator_objs_list")
        if generator_objs_list:
            for generator_obj in generator_objs_list:
                try:
                    generator_obj.__next__()
                except StopIteration:
                    pass
