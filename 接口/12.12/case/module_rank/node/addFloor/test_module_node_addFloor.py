# -*- coding: utf-8 -*-
# @Time : 2019-12-04 19:31:24

import pytest
import allure

from case import BaseCase
from bns.dkyj.node.scn_api_node import ScnApi    # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
import testdata                     # 可随机化的简单参数
from case import utils              # 可复用的用例步骤
from testdata.fixed_bnsData import CollectTypeId, LogicTypeId

#### tmp use ####
api = ScnApi(username=None,password=None)
#### tmp use ####

@pytest.fixture(scope="function")
def depend_nodeInfo():
    data = {}
    with allure.step("前置条件: 添加一级合作方"):
        data["firstPartnerData"] = api.scn_node_addFirstPartner()
    with allure.step("前置条件: 添加品牌节点"):
        data["brandData"] = api.scn_node_addBrand(parentAreaCode=data["firstPartnerData"]["areaCode"])
    with allure.step("前置条件: 添加门店节点"):
        data["shopData"] = api.scn_node_addShop(parentAreaCode=data["brandData"]["areaCode"])
    with allure.step("前置条件: 添加楼层节点"):
        data["floorData"] = api.scn_node_addFloor(parentAreaCode=data["shopData"]["areaCode"])
    with allure.step("前置条件: 添加门店汇总节点"):
        data["shopCollectData"] = api.scn_node_addCollect(parentAreaCode=data["shopData"]["areaCode"], collectTypeId=CollectTypeId.shopcollect.value)
    with allure.step("前置条件: 添加楼层汇总节点"):
        data["floorCollectData"] = api.scn_node_addCollect(parentAreaCode=data["shopData"]["areaCode"], collectTypeId=CollectTypeId.floorcollect.value)
    with allure.step("前置条件: 添加其他汇总节点"):
        data["otherCollectData"] = api.scn_node_addCollect(parentAreaCode=data["shopData"]["areaCode"], collectTypeId=CollectTypeId.othercollect.value)
    with allure.step("前置条件: 添加进店抓拍节点"):
        data["intoshop_logicData"] = api.scn_node_addLogic(parentAreaCode=data["shopData"]["areaCode"], logicTypeId=LogicTypeId.intoshop.value)
    with allure.step("前置条件: 添加店外抓拍节点"):
        data["outshop_logicData"] = api.scn_node_addLogic(parentAreaCode=data["shopData"]["areaCode"], logicTypeId=LogicTypeId.outshop.value)
    with allure.step("前置条件: 添加收银台抓拍节点"):
        data["cashier_logicData"] = api.scn_node_addLogic(parentAreaCode=data["shopData"]["areaCode"], logicTypeId=LogicTypeId.cashier.value)
    with allure.step("前置条件: 添加楼层抓拍节点"):
        data["floor_logicData"] = api.scn_node_addLogic(parentAreaCode=data["shopData"]["areaCode"], logicTypeId=LogicTypeId.floor.value)
    with allure.step("前置条件: 添加热力抓拍节点"):
        data["heatmap_logicData"] = api.scn_node_addLogic(parentAreaCode=data["shopData"]["areaCode"], logicTypeId=LogicTypeId.heatmap.value)
    yield data

    with allure.step("清理前置条件: 删除一级合作方"):
        api.bns_node_delete(areaCode=data["firstPartnerData"]["areaCode"])


@allure.feature("节点管理")
@allure.story("添加楼层")
class TestNodeAddfloor(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功添加楼层节点_在门店下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["shopData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

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
            pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_节点名称已使用(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            parentAreaCode = depend_nodeInfo["shopData"]["areaCode"]
            floorName = depend_nodeInfo["floorData"]["floorName"]

        with allure.step('接口请求'):
            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
                floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 5013
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功添加楼层节点_名称在另一个门店下已使用(self, depend_nodeInfo):
        with allure.step('准备用例入参'):
            shopName = testdata.random_node_shopName()
            floorName = depend_nodeInfo["floorData"]["floorName"]

        with allure.step('接口请求'):
            res_info = api.scn_node_addShop(
                parentAreaCode=depend_nodeInfo["brandData"]["areaCode"],
                shopName=shopName
            )
            parentAreaCode = res_info["areaCode"]
        with allure.step('接口请求'):
            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
                floorName=floorName,
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
    def test_反测_失败添加楼层节点_在门店汇总下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["shopCollectData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_在楼层汇总下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["floorCollectData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_在其他汇总下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["otherCollectData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_在进店抓拍节点下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["intoshop_logicData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_在店外抓拍节点下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["outshop_logicData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_在收银台抓拍节点下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["cashier_logicData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_在楼层抓拍节点下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["floor_logicData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_在热力抓拍节点下创建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["heatmap_logicData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

    @allure.severity(allure.severity_level.NORMAL)
    def test_反测_失败添加楼层节点_楼层节点下建楼层(self, depend_nodeInfo):

        with allure.step('准备用例入参'):

            parentAreaCode = depend_nodeInfo["floorData"]["areaCode"]
            floorName = testdata.random_node_floorName()

        with allure.step('接口请求'):

            res_info = api.bns_node_addFloor(
                parentAreaCode=parentAreaCode,
				floorName=floorName,

            )
        with allure.step('校验:接口响应信息'):

            with allure.step('校验:接口状态码'):

                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.message")
                expect_code = 5015
                expect_msg = '区域类型不正确'
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口响应信息", actual_msg, expect_msg)

        with allure.step('清理用例'):
            pass
