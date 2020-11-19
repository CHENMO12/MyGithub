# -*- coding: utf-8 -*-
# @Time : 2019-12-04 14:32:17
import sys
import allure
import pytest

from base.helper import JsonHelper
from case import BaseCase
from bns.dkyj.node.bns_api_node import BnsApi
from bns.dkyj.node.scn_api_node import ScnApi

_testData_list = BaseCase().csv_info(curr_file=__file__)

# 获取api操作对象, 默认权限为平台管理员
api_object_admin = BnsApi()
api = ScnApi(username=None, password=None)

@pytest.fixture(scope="function")
def depend_nodeInfo():
    with allure.step("前置条件: 添加一级合作方"):
        partner_areaCode = api.scn_node_addFirstPartner(res_accurate=True)
    with allure.step("前置条件: 添加品牌节点"):
        brand_areaCode = api.scn_node_addBrand(parentAreaCode=partner_areaCode, res_accurate=True)
    yield brand_areaCode

    with allure.step("清理前置条件: 删除一级合作方"):
        api.bns_node_delete(areaCode=partner_areaCode)

class TestNode(BaseCase):
    @pytest.mark.parametrize("test_data", _testData_list)
    def test_field_node_addShop(self, test_data, depend_nodeInfo):

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

        if test_data["parentAreaCode"] == "d":
            test_data["parentAreaCode"] = depend_nodeInfo
        parentAreaCode = test_data["parentAreaCode"]
        shopName = test_data["shopName"]
        province = test_data["province"]
        city = test_data["city"]
        district = test_data["district"]
        clerkSim = test_data["clerkSim"]
        clerkSimType = test_data["clerkSimType"]
        customerSim = test_data["customerSim"]
        customerSimType = test_data["customerSimType"]
        groupId = test_data["groupId"]
        repeatDate = test_data["repeatDate"]
        skipTime = test_data["skipTime"]
        trailSkipTime = test_data["trailSkipTime"]
        
        with allure.step("步骤: 请求接口"):

            res_json = api_object_admin.bns_node_addShop(
                parentAreaCode=parentAreaCode,
				shopName=shopName,
				province=province,
				city=city,
				district=district,
				clerkSim=clerkSim,
				clerkSimType=clerkSimType,
				customerSim=customerSim,
				customerSimType=customerSimType,
				groupId=groupId,
				repeatDate=repeatDate,
				skipTime=skipTime,
				trailSkipTime=trailSkipTime,
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
                pass
                
        generator_objs_list = test_data.get("generator_objs_list")
        if generator_objs_list:
            for generator_obj in generator_objs_list:
                try:
                    generator_obj.__next__()
                except StopIteration:
                    pass
