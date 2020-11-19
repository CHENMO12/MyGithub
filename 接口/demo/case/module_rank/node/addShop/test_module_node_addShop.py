# -*- coding: utf-8 -*-
# @Time : 2019-12-04 14:32:17

import pytest
import allure

from case import BaseCase
from bns.dkyj.node.scn_api_node import ScnApi  # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
import testdata  # 可随机化的简单参数
from case import utils  # 可复用的用例步骤

#### tmp use ####
api = ScnApi(username=None, password=None)


#### tmp use ####

@pytest.fixture(scope="function")
def depend_nodeInfo():
    data = {}
    with allure.step("前置条件: 添加一级合作方"):
        data["firstPartnerData"] = api.scn_node_addFirstPartner()
    with allure.step("前置条件: 添加二级合作方"):
        data["secondPartnerData"] = api.scn_node_addSecondPartner(parentAreaCode=data["firstPartnerData"]["areaCode"])
    with allure.step("前置条件: 添加二级合作方"):
        data["thirdPartnerData"] = api.scn_node_addThirdPartner(parentAreaCode=data["secondPartnerData"]["areaCode"])
    with allure.step("前置条件: 添加品牌节点"):
        data["brandData"] = api.scn_node_addBrand(parentAreaCode=data["thirdPartnerData"]["areaCode"])
    with allure.step("前置条件: 添加门店节点"):
        data["shopData"] = api.scn_node_addShop(parentAreaCode=data["brandData"]["areaCode"])
    yield data

    with allure.step("清理前置条件: 删除一级合作方"):
        api.bns_node_delete(areaCode=data["firstPartnerData"]["areaCode"])


@allure.feature("节点管理")
@allure.story("添加门店")
class TestNodeAddshop(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功添加门店_仅填必填项(self, depend_nodeInfo):

        with allure.step('准备用例入参'):
            parentAreaCode = depend_nodeInfo["brandData"]["areaCode"]
            shopName = testdata.random_node_shopName()
            province, city, district = testdata.get_random_addNode_mallAddr()
            clerkSimType = 1
            customerSimType = 1
            repeatDate = 30
            skipTime = 3600
            trailSkipTime = 3600

        with allure.step('接口请求'):
            
            res_info = api.bns_node_addShop(
                parentAreaCode=parentAreaCode,
				shopName=shopName,
				province=province,
				city=city,
				district=district,
				clerkSimType=clerkSimType,
				customerSimType=customerSimType,
				repeatDate=repeatDate,
				skipTime=skipTime,
				trailSkipTime=trailSkipTime,
            )
            res_data = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data")
        with allure.step('校验:接口响应信息'):
        
            with allure.step('校验:接口状态码'):
        
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

        with allure.step('校验:关联业务'):
            utils.positive_check_node(api, res_data)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功添加门店节点_名称在另一个品牌下已使用(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            shopName = depend_nodeInfo["shopData"]["shopName"]
            province, city, district = testdata.get_random_addNode_mallAddr()
            clerkSimType = 1
            customerSimType = 1
            repeatDate = 30
            skipTime = 3600
            trailSkipTime = 3600

        with allure.step('接口请求'):
            res_info = api.scn_node_addBrand(
                parentAreaCode=depend_nodeInfo["thirdPartnerData"]["areaCode"],
                brandName=brandName
            )
            parentAreaCode = res_info["areaCode"]
        with allure.step('接口请求'):
            res_info = api.bns_node_addShop(
                parentAreaCode=parentAreaCode,
                shopName=shopName,
                province=province,
                city=city,
                district=district,
                clerkSimType=clerkSimType,
                customerSimType=customerSimType,
                repeatDate=repeatDate,
                skipTime=skipTime,
                trailSkipTime=trailSkipTime,
            )
            res_data = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data")
        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

        with allure.step('校验:关联业务'):
            utils.positive_check_node(api, res_data)

        with allure.step('清理用例'):
            api.bns_node_delete(areaCode=res_data["areaCode"])

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加门店节点_节点名称已使用(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            parentAreaCode = depend_nodeInfo["brandData"]["areaCode"]
            shopName = depend_nodeInfo["shopData"]["shopName"]
            province, city, district = testdata.get_random_addNode_mallAddr()
            clerkSimType = 1
            customerSimType = 1
            repeatDate = 30
            skipTime = 3600
            trailSkipTime = 3600
        with allure.step('接口请求'):
            res_info = api.bns_node_addShop(
                parentAreaCode=parentAreaCode,
                shopName=shopName,
                province=province,
                city=city,
                district=district,
                clerkSimType=clerkSimType,
                customerSimType=customerSimType,
                repeatDate=repeatDate,
                skipTime=skipTime,
                trailSkipTime=trailSkipTime,
            )
        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 5013
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)