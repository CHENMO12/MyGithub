# -*- coding: utf-8 -*-
# @Time : 2019-11-27 16:12:57
import sys
import allure
import pytest

from base.helper import JsonHelper
from bns.iot.iotUser.bns_api_iotUser import BnsApi
from case import BaseCase

_testData_list = BaseCase().csv_info(curr_file=__file__)

# 获取api操作对象, 默认权限为平台管理员
api_object_admin = BnsApi()


class TestIotuser(BaseCase):

    @pytest.mark.parametrize("test_data", _testData_list)
    def test_field_iotUser_add(self, test_data):

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
        
        userEmail = test_data["userEmail"]
        userName = test_data["userName"]
        userPhone = test_data["userPhone"]
        roleIdsList = test_data["roleIdsList"]
        
        with allure.step("步骤: 请求接口"):

            res_json = api_object_admin.bns_iotUser_add(
                userEmail=userEmail,
				userName=userName,
				userPhone=userPhone,
				roleIdsList=roleIdsList,
            )

        with allure.step("步骤: 提取接口的业务状态码"):
            
            actual_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")

        with allure.step("校验: 业务状态码是否正确"):

            self.assert_actual_equal_expect("业务状态码", actual_code, test_data["expect_code"])

        if test_data["expect_msg"]:

            with allure.step("步骤: 提取接口的提示信息"):

                actual_msg = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.message")

            with allure.step("校验: 提示信息是否正确"):

                self.assert_actual_contain_expect("提示信息", actual_msg, test_data["expect_msg"])

        if test_data["clean_data"]:

            with allure.step("步骤: 数据清理操作"):

                userInfo = api_object_admin.bns_iotUser_list(userName=userName)
                userId = JsonHelper.parseJson_by_objectpath(userInfo, "$..*[@.userId]", res_firstOne=True)

                api_object_admin.bns_iotUser_delete(userId=userId)
                
        generator_objs_list = test_data.get("generator_objs_list")
        if generator_objs_list:
            for generator_obj in generator_objs_list:
                try:
                    generator_obj.__next__()
                except StopIteration:
                    pass
