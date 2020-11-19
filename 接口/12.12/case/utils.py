# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 12:30
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : utils.py

# 将用例可复用的步骤封装成函数
import allure

from base.helper import JsonHelper
from base.helper import AllureHelper

def positive_check_snapLogic(api_admin, areaCode,
                             expect_snapType, expect_userType,
                             expect_snapRecordStatus,
                             expect_collectRecordStatus, expect_faceId):

    with allure.step('测试步骤：抓拍列表查询'):
        res_json = api_admin.scn_snap_list(areaCodesList=areaCode,res_accurate=False,expected_value=1)

        actual_snapType = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.snapType]",res_allowNone=True,res_firstOne=True)
        expect_snapType = expect_snapType
        AllureHelper.assert_equal("抓拍类型校验", expect_snapType, actual_snapType)

        actual_userType = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.userType]",res_allowNone=True,res_firstOne=True)
        expect_userType = expect_userType
        AllureHelper.assert_equal("访客的类型校验", expect_userType, actual_userType)

        actual_snapRecordStatus = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.snapRecordStatus]",res_allowNone=True,res_firstOne=True)
        expect_snapRecordStatus = expect_snapRecordStatus
        AllureHelper.assert_equal("抓拍节点-客流处理状态校验", expect_snapRecordStatus, actual_snapRecordStatus)

        actual_collectRecordStatus = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.collectRecordStatus]",res_allowNone=True,res_firstOne=True)
        expect_collectRecordStatus = expect_collectRecordStatus
        AllureHelper.assert_equal("汇总节点-客流处理状态", expect_collectRecordStatus, actual_collectRecordStatus)

        faceId = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.faceId]",res_allowNone=True,res_firstOne=True)
        actual_faceId = False if faceId =="0" else True
        expect_faceId = expect_faceId
        AllureHelper.assert_equal("人脸库faceId值校验", expect_faceId, actual_faceId)

def positive_check_snapLogicmatch(api_admin,areaCode,expect_snapType,expect_userType):
    with allure.step("校验：校验第二次上报图片的校验结果"):
        with allure.step("取出第二次上报图片的抓拍时间"):
            res_json1 = api_admin.scn_snap_list(areaCodesList=[areaCode], expected_value=2)
            snapTime_list = JsonHelper.parseJson_by_objectpath(res_json1, "$..*[@.snapTime]", res_allowNone=True)
            snapTime = snapTime_list[0] if snapTime_list[0] > snapTime_list[1] else snapTime_list[1]
            res_json = api_admin.scn_snap_list(startDateTime=snapTime, areaCodesList=[areaCode])

        with allure.step("校验:上报数据抓拍类型及访客类型处理结果"):
            actual_snapType = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.snapType]", res_allowNone=True, res_firstOne=True)
            expect_snapType = expect_snapType
            AllureHelper.assert_equal("抓拍类型校验", expect_snapType, actual_snapType)

            actual_userType = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.userType]", res_allowNone=True, res_firstOne=True)
            expect_userType = expect_userType
            AllureHelper.assert_equal("访客的类型校验", expect_userType, actual_userType)

def register_member(api_admin,areaCode,mallareaCode,memberlevelId):

    with allure.step("前置条件: 注册会员"):
        res_json = api_admin.scn_snap_list(areaCodesList=[areaCode])
        faceId = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.faceId]", res_allowNone=True, res_firstOne=True)
        featureImageUrl = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.featureImageUrl]", res_allowNone=True,res_firstOne=True)

        api_admin.scn_member_add(mallareaCode=mallareaCode, faceId=faceId, imagePath=featureImageUrl,memberlevelId=memberlevelId)

def register_employee(api_admin,areaCode,mallareaCode):

    with allure.step("前置条件: 注册店员"):
        res_json = api_admin.scn_snap_list(areaCodesList=[areaCode])
        faceId = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.faceId]", res_allowNone=True,res_firstOne=True)
        featureImageUrl = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.featureImageUrl]",res_allowNone=True, res_firstOne=True)

        api_admin.scn_employee_add(mallareaCode=mallareaCode, faceId=faceId, imagePath=featureImageUrl)

def positive_check_node(api, res_data):
    with allure.step("节点详情接口校验"):
        res_json1 = api.scn_node_detail(areaCode=res_data["areaCode"])
        res_data1 = JsonHelper.parseJson_by_objectpath(res_json1, "$.data")
        AllureHelper.assert_equal("上级节点编码校验", res_data["parentAreaCode"], res_data1["parentAreaCode"])
        AllureHelper.assert_equal("节点名称校验", res_data["name"], res_data1["name"])
        AllureHelper.assert_equal("节点编码校验", res_data["areaCode"], res_data1["areaCode"])
        AllureHelper.assert_equal("节点类型校验", res_data["areaType"], res_data1["areaType"])
        AllureHelper.assert_equal("节点等级校验", res_data["nodeLevel"], res_data1["nodeLevel"])
        AllureHelper.assert_equal("节点id校验", res_data["areaId"], res_data1["areaId"])
    with allure.step("节点列表接口校验"):
        res_json2 = api.scn_node_list(parentAreaCode=res_data["parentAreaCode"], name=res_data["name"])
        res_data2 = JsonHelper.parseJson_by_objectpath(res_json2, "$.data.list[0]")
        AllureHelper.assert_equal("上级节点编码校验", res_data["parentAreaCode"], res_data2["parentAreaCode"])
        AllureHelper.assert_equal("节点编码校验", res_data["areaCode"], res_data2["areaCode"])
        AllureHelper.assert_equal("节点名称校验", res_data["name"], res_data2["name"])
        AllureHelper.assert_equal("节点类型校验", res_data["areaType"], res_data2["areaType"])
        AllureHelper.assert_equal("节点等级校验", res_data["nodeLevel"], res_data2["nodeLevel"])
        AllureHelper.assert_equal("节点id校验", res_data["areaId"], res_data2["areaId"])
    with allure.step("节点树接口校验"):
        res_json3 = api.bns_node_tree(parentAreaCode=res_data["parentAreaCode"], nodeLevel=5)
        res_data3 = JsonHelper.parseJson_by_objectpath(res_json3,
                                                       "$.response_data.data[@.name is %s][0]" % res_data["name"])
        AllureHelper.assert_equal("上级节点编码校验", res_data["parentAreaCode"], res_data3["parentAreaCode"])
        AllureHelper.assert_equal("节点名称校验", res_data["name"], res_data3["name"])
        AllureHelper.assert_equal("节点编码校验", res_data["areaCode"], res_data3["areaCode"])
        AllureHelper.assert_equal("节点类型校验", res_data["areaType"], res_data3["areaType"])
        AllureHelper.assert_equal("节点等级校验", res_data["nodeLevel"], res_data3["nodeLevel"])
        AllureHelper.assert_equal("节点id校验", res_data["areaId"], res_data3["areaId"])
    with allure.step("节点树(有分组)接口校验"):
        res_json4 = api.bns_node_treeGroup(parentAreaCode=res_data["parentAreaCode"], nodeLevel=5)
        res_data4 = JsonHelper.parseJson_by_objectpath(res_json4,
                                                       "$.response_data.data[@.name is %s][0]" % res_data["name"])
        AllureHelper.assert_equal("上级节点编码校验", res_data["parentAreaCode"], res_data4["parentAreaCode"])
        AllureHelper.assert_equal("节点名称校验", res_data["name"], res_data4["name"])
        AllureHelper.assert_equal("节点编码校验", res_data["areaCode"], res_data4["areaCode"])
        AllureHelper.assert_equal("节点类型校验", res_data["areaType"], res_data4["areaType"])
        AllureHelper.assert_equal("节点等级校验", res_data["nodeLevel"], res_data4["nodeLevel"])
        AllureHelper.assert_equal("节点id校验", res_data["areaId"], res_data4["areaId"])

def snap_age_identification(response, expect_age_value, expect_deciceCode):
    with allure.step('校验:接口响应信息'):
        with allure.step('校验:查询数据为一条'):
            expect_value = 1
            actual_value = JsonHelper.parseJson_by_objectpath(response, "$..*[@.total]")[0]
            AllureHelper.assert_equal("接口查询返回条数", actual_value, expect_value)

        with allure.step('校验:查询结果中为该设备上报的抓拍数据'):
            expected_value = expect_deciceCode
            actual_value = JsonHelper.parseJson_by_objectpath(response, "$..*[@.deviceCode]")
            AllureHelper.assert_isContain("抓拍数据", expected_value, actual_value)

        with allure.step('校验:查询结果中年龄识别结果小于等于{}'.format(expect_age_value)):
            expected_value = expect_age_value
            actual_value = JsonHelper.parseJson_by_objectpath(response, "$..*[@.ageInit]")[0]
            AllureHelper.assert_except_ge_actual("年龄", expected_value, actual_value)

def snap_node_identification(response, expect_snapRecordStatus, expect_collectRecordStatus=None):
    with allure.step('校验:接口响应信息'):
        with allure.step('校验:查询数据为两条'):
            expect_value = 2
            actual_value = JsonHelper.parseJson_by_objectpath(response, "$..*[@.total]")[0]
            AllureHelper.assert_equal("接口查询返回条数", actual_value, expect_value)

        with allure.step('校验:查询结果中两条数据faceid相同'):
            expected_value = JsonHelper.parseJson_by_objectpath(response, "$..*[@.faceId]")[0]
            actual_value = JsonHelper.parseJson_by_objectpath(response, "$..*[@.faceId]")[1]
            AllureHelper.assert_equal("faceID查询的两条数据", actual_value, expected_value)

        with allure.step('校验:snapRecordStatus值'):

            actual_snapRecordStatus = \
                JsonHelper.parseJson_by_objectpath(response, "$.*.data.list.snapRecordStatus")[0]
            AllureHelper.assert_equal("抓拍节点下图片去重状态对应字段", expect_snapRecordStatus, actual_snapRecordStatus)
        if expect_collectRecordStatus is not None:
            with allure.step('校验:collectRecordStatus值'):

                actual_collectRecordStatus = \
                    JsonHelper.parseJson_by_objectpath(response, "$.*.data.list.collectRecordStatus")[0]
                AllureHelper.assert_equal("汇总节点下图片去重状态对应字段", expect_collectRecordStatus, actual_collectRecordStatus)
