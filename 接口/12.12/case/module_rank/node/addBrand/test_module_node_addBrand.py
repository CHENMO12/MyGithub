# -*- coding: utf-8 -*-
# @Time : 2019-12-03 14:09:13

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
    yield data

    with allure.step("清理前置条件: 删除一级合作方"):
        api.bns_node_delete(areaCode=data["firstPartnerData"]["areaCode"])


@allure.feature("节点管理")
@allure.story("添加二级合作方")
class TestNodeAddsecondpartner(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功添加品牌节点_一级合作方下添加(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
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
    def test_反测_失败添加品牌节点_年龄组中最大值小于最小值(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,3), (4,2),(2,90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
            )
        # res_data = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data")
        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5028
                expect_msg = "年龄分组不能断层"
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口message", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加品牌节点_年龄组中上一段的最大值与下一段的最小值不相邻(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,3), (5,90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
            )
        # res_data = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data")
        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5028
                expect_msg = "年龄分组不能断层"
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口message", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加品牌节点_年龄组没有从0开始(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(5,90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
            )
        # res_data = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data")
        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5028
                expect_msg = "年龄分组不能断层"
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口message", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加品牌节点_年龄组结束值小于90(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,89)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
            )
        # res_data = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data")
        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5028
                expect_msg = "年龄分组不能断层"
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口message", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加品牌节点_年龄组结束值大于90(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,91)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
            )
        # res_data = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data")
        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5028
                expect_msg = "年龄分组不能断层"
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口message", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功添加品牌节点_年龄分组中最大年龄和最小年龄相等(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0, 0), (1, 90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
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
    def test_正测_成功添加品牌节点_划分20个年龄分组(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,0), (1,1), (2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19, 90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
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
    def test_反测_失败添加品牌节点_划分21个年龄分组(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,0), (1,1), (2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19, 19),(20, 90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
            )
        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5029
                expect_msg = "年龄分组不能超过20个"
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口message", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功添加品牌节点_划分10个年龄分组(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,0), (1,1), (2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9, 90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["firstPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
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
    def test_正测_成功添加品牌节点_二级合作方下添加(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0,90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["secondPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
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
    def test_正测_成功添加品牌节点_三级合作方下添加(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            brandName = testdata.random_node_brandName()
            ageGroups = [(0, 90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["thirdPartnerData"]["areaCode"],
                brandName=brandName,
                ageGroups=ageGroups
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
    def test_正测_成功添加品牌节点_名称在另一个三级合作方下已使用(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            thirdPartnerName = testdata.random_node_thirdPartnerName()
            brandName = depend_nodeInfo["brandData"]["brandName"]
            ageGroups = [(0, 90)]

        with allure.step('接口请求'):
            res_info = api.bns_node_addThirdPartner(
                parentAreaCode=depend_nodeInfo["secondPartnerData"]["areaCode"],
                partnerName=thirdPartnerName
            )
            areaCode = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.data.areaCode")
        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=areaCode,
                brandName=brandName,
                ageGroups=ageGroups
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
    def test_正测_失败添加品牌节点_节点名称已使用(self, depend_nodeInfo):
        ageGroups = [(0, 90)]
        with allure.step('接口请求'):
            res_info = api.bns_node_addBrand(
                parentAreaCode=depend_nodeInfo["thirdPartnerData"]["areaCode"],
                brandName=depend_nodeInfo["brandData"]["brandName"],
                ageGroups=ageGroups
            )

        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 5013
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
