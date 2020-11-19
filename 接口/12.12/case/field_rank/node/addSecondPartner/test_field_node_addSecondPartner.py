# -*- coding: utf-8 -*-
# @Time : 2019-12-03 14:09:13
import sys
import allure
import pytest

from base.helper import JsonHelper
from case import BaseCase
from bns.dkyj.node.bns_api_node import BnsApi

_testData_list = BaseCase().csv_info(curr_file=__file__)

# 获取api操作对象, 默认权限为平台管理员
api_object_admin = BnsApi()


class TestNode(BaseCase):

    @pytest.mark.parametrize("test_data", _testData_list)
    def test_field_node_addSecondPartner(self, test_data):

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
        
        parentAreaCode = test_data["parentAreaCode"]
        partnerName = test_data["partnerName"]
        
        with allure.step("步骤: 请求接口"):

            res_json = api_object_admin.bns_node_addSecondPartner(
                parentAreaCode=parentAreaCode,
				partnerName=partnerName,
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
                
                # TODO: 调用删除接口
                pass
                
        generator_objs_list = test_data.get("generator_objs_list")
        if generator_objs_list:
            for generator_obj in generator_objs_list:
                try:
                    generator_obj.__next__()
                except StopIteration:
                    pass
