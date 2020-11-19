# -*- coding: utf-8 -*-
# @Time : 2019-11-18 17:17:37

import pytest
import allure
import time

from case import BaseCase
from bns.dkyj.api import Api  # 业务api的调用入口
from bns.iot.iotapi import IotApi  # 业务api的调用入口
from bns.public.publicapi import PublicApi  # 公共服务api的调用入口
from base.helper import JsonHelper  # json信息提取
import testdata  # 可随机化的简单参数
from case import utils  # 可复用的用例步骤
from testdata import fixed_bnsData
from testdata import gen_bnsData
from testdata import gen_devData

api_admin = Api(username=None, password=None)
iot_api_admin = IotApi(username=None, password=None)
public_api_admin = PublicApi(username=None, password=None)


@pytest.fixture(scope="function", name="关联_IOT设备信息")
def depend_iotDevice_info():
    with allure.step("前置条件1: 注册IOT设备"):
        info = public_api_admin.scn_publicDevice_add()
        deviceCode = info["deviceCode"]

    with allure.step("前置条件2: 启用设备"):
        iot_api_admin.bns_iotDevice_enable(deviceCodeList=[deviceCode])
        list_info = iot_api_admin.bns_iotDevice_list(deviceCodeOrBar=deviceCode, pageNo=1, pageSize=20)
        deviceId = JsonHelper.parseJson_by_objectpath(list_info, "$..*[@.id]")[0]

    yield info
    with allure.step("清理前置条件:审批下架设备申请"):
        iot_api_admin.scn_iotDevice_apply(deviceId)
    with allure.step("在公共服务中删除设备"):
        public_api_admin.bns_publicDevice_delete(deviceCode=deviceCode)


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


@pytest.fixture(scope="function", name="关联_抓拍子节点_进店")
def depend_logicNode(关联_门店节点):
    with allure.step("前置条件: 添加抓拍子节点"):
        with allure.step("前置条件: 添加抓拍子节点"):
            info = api_admin.scn_node_addLogic(parentAreaCode=关联_门店节点["areaCode"],
                                               logicTypeId=fixed_bnsData.LogicTypeId.intoshop.value)
            areaCode = info["areaCode"]

    yield info

    with allure.step("清理前置条件: 删除抓拍子节点"):
        api_admin.bns_node_delete(areaCode=areaCode)


@pytest.fixture(scope="function", name="关联_设备绑定节点")
def depend_addDevice(关联_IOT设备信息, 关联_门店节点, 关联_抓拍子节点_进店):
    with allure.step("前置条件: 设备绑定节点"):
        info = api_admin.scn_device_add(mallAreaCode=关联_门店节点["areaCode"], deviceCodeOrBar=关联_IOT设备信息["deviceCode"],
                                        areaCodesList=[关联_抓拍子节点_进店["areaCode"]])
        deviceCodeOrBar = info["deviceCodeOrBar"]

    yield info

    with allure.step("清理前置条件: 设备解绑"):
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar, areaCode=关联_抓拍子节点_进店["areaCode"])


@pytest.fixture(scope="function", name="关联_新增会员级别")
def depend_addmemberlevel(关联_品牌节点):
    with allure.step("前置条件: 添加会员级别"):
        api_admin.scn_memberlevel_add(brandCode=关联_品牌节点["areaCode"], brandId=关联_品牌节点["areaId"])
        res_json = api_admin.bns_memberlevel_list(brandId=关联_品牌节点["areaId"])
        levelId = JsonHelper.parseJson_by_objectpath(res_json, "$..*[@.levelId]", res_allowNone=True, res_firstOne=True)

    yield levelId

    with allure.step("清理前置条件: 删除会员级别"):
        api_admin.bns_memberlevel_delete(brandId=关联_品牌节点["areaCode"], memberlevelId=levelId)


@pytest.fixture(scope="function", name="关联_抓拍子节点_进店_去重时间为0")
def depend_new_logicNode(关联_门店节点):
    with allure.step("前置条件: 添加抓拍子节点"):
        with allure.step("前置条件: 添加抓拍子节点"):
            info = api_admin.scn_node_addLogic(parentAreaCode=关联_门店节点["areaCode"],
                                               logicTypeId=fixed_bnsData.LogicTypeId.intoshop.value, skipTime=0,
                                               skipType=-1)
            areaCode = info["areaCode"]

    yield info
    # 删除品牌节点
    with allure.step("清理前置条件: 删除抓拍子节点"):
        api_admin.bns_node_delete(areaCode=areaCode)


@pytest.fixture(scope="function", name="关联_设备绑定节点_去重时间为0")
def depend_new_addDevice(关联_IOT设备信息, 关联_门店节点, 关联_抓拍子节点_进店_去重时间为0):
    with allure.step("前置条件: 设备绑定节点"):
        info = api_admin.scn_device_add(mallAreaCode=关联_门店节点["areaCode"], deviceCodeOrBar=关联_IOT设备信息["deviceCode"],
                                        areaCodesList=[关联_抓拍子节点_进店_去重时间为0["areaCode"]])
        deviceCodeOrBar = info["deviceCodeOrBar"]

    yield info
    # 设备解绑
    with allure.step("清理前置条件: 设备解绑"):
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar, areaCode=关联_抓拍子节点_进店_去重时间为0["areaCode"])


@pytest.fixture(scope="function", name="关联_门店汇总节点")
def depend_collectNode(关联_门店节点):
    with allure.step("前置条件: 添加门店节点"):
        info = api_admin.scn_node_addCollect(parentAreaCode=关联_门店节点["areaCode"])
        areaCode = info["areaCode"]

    yield areaCode


@pytest.fixture(scope="function", name="关联_IOT设备信息_添加两台设备")
def depend_iotDevice_infotwo():
    with allure.step("前置条件: 注册IOT设备"):
        info_1 = public_api_admin.scn_publicDevice_add()
        info_2 = public_api_admin.scn_publicDevice_add()

        deviceCode1 = info_1["deviceCode"]
        deviceCode2 = info_2["deviceCode"]

    with allure.step("前置条件2: 启用设备"):
        iot_api_admin.bns_iotDevice_enable(deviceCodeList=[deviceCode1, deviceCode2])
        info1 = iot_api_admin.bns_iotDevice_list(deviceCodeOrBar=deviceCode1, pageNo=1, pageSize=20)
        info2 = iot_api_admin.bns_iotDevice_list(deviceCodeOrBar=deviceCode2, pageNo=1, pageSize=20)
        deviceId1 = JsonHelper.parseJson_by_objectpath(info1, "$..*[@.id]")
        deviceId2 = JsonHelper.parseJson_by_objectpath(info2, "$..*[@.id]")

    yield [info_1, info_2]

    with allure.step("在公共服务中删除设备"):
        public_api_admin.bns_publicDevice_delete(deviceCode=deviceCode1)
        public_api_admin.bns_publicDevice_delete(deviceCode=deviceCode2)


@pytest.fixture(scope="function", name="关联_门店下创建两个抓拍节点_绑定节点")
def depend__logicNode_two(关联_IOT设备信息_添加两台设备, 关联_门店节点):
    with allure.step("前置条件: 添加两个抓拍节点"):
        info_1 = api_admin.scn_node_addLogic(parentAreaCode=关联_门店节点["areaCode"],
                                             logicTypeId=fixed_bnsData.LogicTypeId.intoshop.value)
        info_2 = api_admin.scn_node_addLogic(parentAreaCode=关联_门店节点["areaCode"],
                                             logicTypeId=fixed_bnsData.LogicTypeId.intoshop.value)
        areaCode_1 = info_1["areaCode"]
        areaCode_2 = info_2["areaCode"]
    with allure.step("前置条件: 设备绑定节点"):
        info_3 = api_admin.scn_device_add(mallAreaCode=关联_门店节点["areaCode"],
                                          deviceCodeOrBar=关联_IOT设备信息_添加两台设备[0]["deviceCode"],
                                          areaCodesList=[areaCode_1])
        info_4 = api_admin.scn_device_add(mallAreaCode=关联_门店节点["areaCode"],
                                          deviceCodeOrBar=关联_IOT设备信息_添加两台设备[1]["deviceCode"],
                                          areaCodesList=[areaCode_2])
        deviceCodeOrBar_1 = info_3["deviceCodeOrBar"]
        deviceCodeOrBar_2 = info_4["deviceCodeOrBar"]

    yield [areaCode_1, areaCode_2, deviceCodeOrBar_1, deviceCodeOrBar_2]
    # 设备解绑
    with allure.step("清理前置条件: 设备解绑"):
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar_1, areaCode=areaCode_1)
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar_2, areaCode=areaCode_2)
    # 删除品牌节点
    with allure.step("清理前置条件: 删除品牌节点"):
        api_admin.bns_node_delete(areaCode=areaCode_1[:9])


@pytest.fixture(scope="function", name="关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点")
def depend_collectnode_two(关联_IOT设备信息_添加两台设备, 关联_门店节点, request):
    with allure.step("前置条件: 门店下创建汇总节点"):
        info = api_admin.scn_node_addCollect(parentAreaCode=关联_门店节点["areaCode"], collectTypeId=request.param)
        areaCode = info["areaCode"]
    with allure.step("前置条件: 门店汇总节点下下创建另两个抓拍节点"):
        info = api_admin.scn_node_addLogic(parentAreaCode=areaCode,
                                           logicTypeId=fixed_bnsData.LogicTypeId.intoshop.value)
        areaCode_1 = info["areaCode"]
        info = api_admin.scn_node_addLogic(parentAreaCode=areaCode,
                                           logicTypeId=fixed_bnsData.LogicTypeId.intoshop.value)
        areaCode_2 = info["areaCode"]
    with allure.step("前置条件:绑定这两个抓拍节点"):
        # 设备绑定抓拍节点
        info_3 = api_admin.scn_device_add(mallAreaCode=areaCode, deviceCodeOrBar=关联_IOT设备信息_添加两台设备[0]["deviceCode"],
                                          areaCodesList=[areaCode_1])
        info_4 = api_admin.scn_device_add(mallAreaCode=areaCode, deviceCodeOrBar=关联_IOT设备信息_添加两台设备[1]["deviceCode"],
                                          areaCodesList=[areaCode_2])

        deviceCodeOrBar_1 = info_3["deviceCodeOrBar"]
        deviceCodeOrBar_2 = info_4["deviceCodeOrBar"]
    yield [areaCode_1, areaCode_2, deviceCodeOrBar_1, deviceCodeOrBar_2]
    # 设备解绑
    with allure.step("清理前置条件: 设备解绑"):
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar_1, areaCode=areaCode_1)
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar_2, areaCode=areaCode_2)
    # 删除品牌节点
    with allure.step("清理前置条件: 删除品牌节点"):
        api_admin.bns_node_delete(areaCode=areaCode_1[:9])


@pytest.fixture(scope="function", name="关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点_出店逻辑")
def depend_collectnode_out_two(关联_IOT设备信息_添加两台设备, 关联_门店节点, request):
    with allure.step("前置条件: 门店下创建汇总节点"):
        info = api_admin.scn_node_addCollect(parentAreaCode=关联_门店节点["areaCode"], collectTypeId=request.param)
        areaCode = info["areaCode"]
    with allure.step("前置条件: 门店汇总节点下下创建另两个抓拍节点"):
        info = api_admin.scn_node_addLogic(parentAreaCode=areaCode,
                                           logicTypeId=fixed_bnsData.LogicTypeId.outshop.value)
        areaCode_1 = info["areaCode"]
        info = api_admin.scn_node_addLogic(parentAreaCode=areaCode,
                                           logicTypeId=fixed_bnsData.LogicTypeId.outshop.value)
        areaCode_2 = info["areaCode"]
    with allure.step("前置条件:绑定这两个抓拍节点"):
        # 设备绑定抓拍节点
        info_3 = api_admin.scn_device_add(mallAreaCode=areaCode, deviceCodeOrBar=关联_IOT设备信息_添加两台设备[0]["deviceCode"],
                                          areaCodesList=[areaCode_1])
        info_4 = api_admin.scn_device_add(mallAreaCode=areaCode, deviceCodeOrBar=关联_IOT设备信息_添加两台设备[1]["deviceCode"],
                                          areaCodesList=[areaCode_2])

        deviceCodeOrBar_1 = info_3["deviceCodeOrBar"]
        deviceCodeOrBar_2 = info_4["deviceCodeOrBar"]
    yield [areaCode_1, areaCode_2, deviceCodeOrBar_1, deviceCodeOrBar_2]
    # 设备解绑
    with allure.step("清理前置条件: 设备解绑"):
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar_1, areaCode=areaCode_1)
        api_admin.bns_device_umount(deviceCode=deviceCodeOrBar_2, areaCode=areaCode_2)
    # 删除品牌节点
    with allure.step("清理前置条件: 删除品牌节点"):
        api_admin.bns_node_delete(areaCode=areaCode_1[:9])



@allure.feature("抓拍列表")
@allure.story("抓拍列表查询")
class TestSnapList(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询抓拍列表_节点查询_单节点查询_抓拍子节点(self, 关联_门店节点, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张人脸图片'):
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"])

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )

        with allure.step('校验:接口响应信息'):
            with allure.step('校验:查询数据为一条'):
                expect_value = 1
                actual_value = JsonHelper.parseJson_by_objectpath(res_info, "$..*[@.total]")[0]
                self.assert_actual_equal_expect("接口查询返回条数", actual_value, expect_value)

            with allure.step('校验:查询结果中为该设备上报的抓拍数据'):
                expected_value = 关联_设备绑定节点["deviceCodeOrBar"]
                actual_value = JsonHelper.parseJson_by_objectpath(res_info, "$..*[@.deviceCode]")
                self.assert_actual_contain_expect("校验返回数据中包含", actual_value, expected_value)


@allure.feature("抓拍列表")
@allure.story("抓拍逻辑-比对不上处理结果")
class TestSnapLogicnomatch(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_正脸图片像素小于65得分大于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素小于65
            img_path = gen_bnsData.get_face_picture_38pixel()
            # 得分大于1点1
            score = 1.4
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=6,
                                       expect_userType=0,
                                       expect_snapRecordStatus=-1,
                                       expect_collectRecordStatus=-1, expect_faceId=False
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_正脸图片像素小于65得分等于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素小于65
            img_path = gen_bnsData.get_face_picture_64pixel()
            # 得分等于1点1
            score = 1.1
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=6,
                                       expect_userType=0,
                                       expect_snapRecordStatus=0,
                                       expect_collectRecordStatus=-1, expect_faceId=False
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_侧脸图片像素小于65得分大于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张侧脸抓拍图'):
            # 正脸图片
            capAngle = 1
            # 像素小于65
            img_path = gen_bnsData.get_face_picture_38pixel()
            # 得分大于1点1
            score = 1.4
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=6,
                                       expect_userType=0,
                                       expect_snapRecordStatus=-1,
                                       expect_collectRecordStatus=-1, expect_faceId=False
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_侧脸图片像素小于65得分等于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张侧脸抓拍图'):
            # 正脸图片
            capAngle = 1
            # 像素小于65
            img_path = gen_bnsData.get_face_picture_64pixel()
            # 得分等于1点1
            score = 1.1
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=6,
                                       expect_userType=0,
                                       expect_snapRecordStatus=0,
                                       expect_collectRecordStatus=-1, expect_faceId=False
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_正脸图片像素大于65得分等于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于65
            img_path = gen_bnsData.get_face_picture_66pixel()
            # 得分等于1点1
            score = 1.1
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=0,
                                       expect_userType=0,
                                       expect_snapRecordStatus=0,
                                       expect_collectRecordStatus=-1, expect_faceId=True
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_正脸图片像素大于65得分大于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于65
            img_path = gen_bnsData.get_face_picture_68pixel()
            # 得分等于1点1
            score = 1.3
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=0,
                                       expect_userType=0,
                                       expect_snapRecordStatus=0,
                                       expect_collectRecordStatus=-1, expect_faceId=True
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_正脸且为出店图片像素大于65得分大于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于65
            img_path = gen_bnsData.get_face_picture_90pixel()
            # 得分等于1点1
            score = 1.2
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score, userStatus=4)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=0,
                                       expect_userType=0,
                                       expect_snapRecordStatus=-1,
                                       expect_collectRecordStatus=-1, expect_faceId=True
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_正脸且为无状态图片像素大于65得分大于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于65
            img_path = gen_bnsData.get_face_picture_102pixel()
            # 得分等于1点1
            score = 1.3
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score, userStatus=0)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=0,
                                       expect_userType=0,
                                       expect_snapRecordStatus=0,
                                       expect_collectRecordStatus=-1, expect_faceId=True
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_侧脸图片像素大于65得分等于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张侧脸抓拍图'):
            # 侧脸图片
            capAngle = 1
            # 像素大于65
            img_path = gen_bnsData.get_face_picture_88pixel()
            # 得分等于1点1
            score = 1.1
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=0,
                                       expect_userType=0,
                                       expect_snapRecordStatus=0,
                                       expect_collectRecordStatus=-1, expect_faceId=True
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_侧脸图片像素大于65得分大于1点1(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张侧脸抓拍图'):
            # 侧脸图片
            capAngle = 1
            # 像素大于65
            img_path = gen_bnsData.get_face_picture_92pixel()
            # 得分等于1点1
            score = 1.1
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=0,
                                       expect_userType=0,
                                       expect_snapRecordStatus=0,
                                       expect_collectRecordStatus=-1, expect_faceId=True
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_头肩类型_capAngle等于3(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 头肩图片
            capAngle = 3
            # 像素小于65
            img_path = gen_bnsData.get_face_picture_66pixel()
            # 得分大于1点1
            score = 1.4
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=3,
                                       expect_userType=0,
                                       expect_snapRecordStatus=-1,
                                       expect_collectRecordStatus=-1, expect_faceId=False
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_无特征类型_图片检测不到人脸(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张无特征抓拍图'):
            # 头肩图片
            capAngle = 0
            # 像素小于65
            img_path = gen_bnsData.get_face_picture_00pixel()
            # 得分大于1点1
            score = 1.3
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=5,
                                       expect_userType=0,
                                       expect_snapRecordStatus=-1,
                                       expect_collectRecordStatus=-1, expect_faceId=False
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_类型为不做人脸识别_图片为店外徘徊状态(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 1
            # 像素小于65
            img_path = gen_bnsData.get_face_picture_68pixel()
            # 得分大于1点1
            score = 1.3
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score, userStatus=1)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=7,
                                       expect_userType=0,
                                       expect_snapRecordStatus=-1,
                                       expect_collectRecordStatus=-1, expect_faceId=False
                                       )

    @allure.severity(allure.severity_level.NORMAL)
    def test_类型为不做人脸识别_图片为店内徘徊状态(self, 关联_设备绑定节点, 关联_抓拍子节点_进店):
        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素小于65
            img_path = gen_bnsData.get_face_picture_68pixel()
            # 得分大于1点1
            score = 1.4
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score, userStatus=3)

        utils.positive_check_snapLogic(api_admin,
                                       areaCode=[关联_抓拍子节点_进店["areaCode"]],
                                       expect_snapType=7,
                                       expect_userType=0,
                                       expect_snapRecordStatus=-1,
                                       expect_collectRecordStatus=-1, expect_faceId=False
                                       )


@allure.feature("抓拍列表")
@allure.story("抓拍逻辑-比对处理结果")
class TestSnapLogicmatch(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_正脸图片像素小于40得分小于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture1_90pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素小于40
            img_path = gen_bnsData.get_face_picture_38pixel()
            # 得分小于1点0
            score = 0.9
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=6, expect_userType=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_正脸图片像素小于40得分等于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture1_90pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素小于40
            img_path = gen_bnsData.get_face_picture_38pixel()
            # 得分等于1.0
            score = 1.0
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=6, expect_userType=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_正脸图片像素小于40得分大于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture1_90pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素小于40
            img_path = gen_bnsData.get_face_picture_38pixel()
            # 得分等于1.0
            score = 1.3
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=6, expect_userType=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_正脸图片像素等于40得分小于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture_70pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于
            img_path = gen_bnsData.get_face_picture_40_70pixel()
            # 得分小于1.0
            score = 0.9
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=6, expect_userType=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_正脸图片像素等于40得分等于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture_70pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于
            img_path = gen_bnsData.get_face_picture_40_70pixel()
            # 得分等于1.0
            score = 1.0
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=0, expect_userType=1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_正脸图片像素等于40得分大于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture_70pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于
            img_path = gen_bnsData.get_face_picture_40_70pixel()
            # 得分等于1.0
            score = 1.1
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=0, expect_userType=1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_低质量类型_正脸图片像素大于40得分小于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture_88pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于
            img_path = gen_bnsData.get_face_picture_44pixel()
            # 得分小于1.0
            score = 0.9
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=6, expect_userType=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_正脸图片像素大于40得分等于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture_88pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于40
            img_path = gen_bnsData.get_face_picture_44pixel()
            # 得分等于1.0
            score = 1.0
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=0, expect_userType=1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_人脸类型_正脸图片像素大于40得分大于1点0(self, 关联_设备绑定节点, 关联_抓拍子节点_进店, 关联_门店节点, 关联_新增会员级别):
        with allure.step('前置条件：模拟上报一条正脸抓拍图并注册成会员'):
            img_pathmember = gen_bnsData.get_face_picture_88pixel()
            # 上报注册会员图片
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_path=img_pathmember,
                                                   score=1.3)

            utils.register_member(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                  mallareaCode=关联_门店节点["areaCode"], memberlevelId=关联_新增会员级别)

        with allure.step('前置条件：模拟设备上报一张正脸抓拍图'):
            # 正脸图片
            capAngle = 0
            # 像素大于40
            img_path = gen_bnsData.get_face_picture_44pixel()
            # 得分大于1.0
            score = 1.3
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], capAngle=capAngle,
                                                   img_path=img_path, score=score)

        utils.positive_check_snapLogicmatch(api_admin, areaCode=关联_抓拍子节点_进店["areaCode"],
                                            expect_snapType=0, expect_userType=1)


@allure.feature("抓拍列表")
@allure.story("抓拍逻辑-年龄识别")
class TestSnapAgeIdentification(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_进店_小孩类型人脸(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备上报一张小孩人脸图片'):
            img_path = gen_bnsData.get_face_picture(index=3)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=img_path, score="1.2")

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )
        utils.snap_age_identification(response=res_info, expect_age_value=10,
                                      expect_deciceCode=关联_设备绑定节点["deviceCodeOrBar"])

    @allure.severity(allure.severity_level.NORMAL)
    def test_进店_成年类型人脸(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备上报一张小孩人脸图片'):
            img_path = gen_bnsData.get_face_picture(index=2)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=img_path, score="1.2")

        with allure.step('准备用例查询入参'):
            # mallAreaCode = 关联_门店节点["areaCode"]
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )
        utils.snap_age_identification(response=res_info, expect_age_value=40,
                                      expect_deciceCode=关联_设备绑定节点["deviceCodeOrBar"])

    @allure.severity(allure.severity_level.NORMAL)
    def test_无状态_小孩类型人脸(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备上报一张小孩人脸图片'):
            img_path = gen_bnsData.get_face_picture(index=3)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=img_path, userStatus=0,
                                                   score="1.2")

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )
        utils.snap_age_identification(response=res_info, expect_age_value=10,
                                      expect_deciceCode=关联_设备绑定节点["deviceCodeOrBar"])

    @allure.severity(allure.severity_level.NORMAL)
    def test_无状态_成年类型人脸(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备上报一张小孩人脸图片'):
            img_path = gen_bnsData.get_face_picture(index=2)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=img_path, userStatus=0,
                                                   score="1.2")

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )
        utils.snap_age_identification(response=res_info, expect_age_value=40,
                                      expect_deciceCode=关联_设备绑定节点["deviceCodeOrBar"])

    @allure.severity(allure.severity_level.NORMAL)
    def test_离店_小孩类型人脸(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备上报一张小孩人脸图片'):
            img_path = gen_bnsData.get_face_picture(index=3)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=img_path, userStatus=4,
                                                   score="1.2")

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )
        utils.snap_age_identification(response=res_info, expect_age_value=10,
                                      expect_deciceCode=关联_设备绑定节点["deviceCodeOrBar"])

    @allure.severity(allure.severity_level.NORMAL)
    def test_离店_成年类型人脸(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备上报一张小孩人脸图片'):
            img_path = gen_bnsData.get_face_picture(index=2)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=img_path, userStatus=4,
                                                   score="1.2")

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )
        utils.snap_age_identification(response=res_info, expect_age_value=40,
                                      expect_deciceCode=关联_设备绑定节点["deviceCodeOrBar"])

    @allure.severity(allure.severity_level.NORMAL)
    def test_店内徘徊不做性别年龄识别(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备上报一张小孩人脸图片'):
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], userStatus=3, score="1.2")

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )
        utils.snap_age_identification(response=res_info, expect_age_value=-1,
                                      expect_deciceCode=关联_设备绑定节点["deviceCodeOrBar"])

    @allure.severity(allure.severity_level.NORMAL)
    def test_店外徘徊不做性别年龄识别(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备上报一张小孩人脸图片'):
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], userStatus=1, score="1.2")

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
            )
        utils.snap_age_identification(response=res_info, expect_age_value=-1,
                                      expect_deciceCode=关联_设备绑定节点["deviceCodeOrBar"])


@allure.feature("抓拍列表")
@allure.story("抓拍逻辑-节点数据处理")
class TestSnapNodeIdentification(BaseCase):
    @allure.severity(allure.severity_level.NORMAL)
    def test_进店_抓拍节点_去重时间外_上传相同的人脸不被去重(self, 关联_抓拍子节点_进店_去重时间为0, 关联_设备绑定节点_去重时间为0):
        with allure.step('前置条件：模拟设备随机上报两张人脸图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点_去重时间为0["deviceCodeOrBar"], img_path=image_path,
                                                   score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点_去重时间为0["deviceCodeOrBar"], img_path=image_path,
                                                   score="1.2")
            time.sleep(3)

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店_去重时间为0["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                expected_value=2,
                res_accurate=False,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_进店_抓拍节点_去重时间内_上传相同的人脸被去重(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备随机上报两张人脸图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, score="1.2")
            time.sleep(3)
        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                expected_value=2,
                res_accurate=False,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_无状态_抓拍节点_去重时间外_上传相同的人脸不被去重(self, 关联_抓拍子节点_进店_去重时间为0, 关联_设备绑定节点_去重时间为0):
        with allure.step('前置条件：模拟设备随机上报两张人脸图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点_去重时间为0["deviceCodeOrBar"], img_path=image_path,
                                                   userStatus=0, score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点_去重时间为0["deviceCodeOrBar"], img_path=image_path,
                                                   userStatus=0, score="1.2")
            time.sleep(3)

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店_去重时间为0["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                expected_value=2,
                res_accurate=False,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_无状态_抓拍节点_去重时间内_上传相同的人脸被去重(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备随机上报两张人脸图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, userStatus=0,
                                                   score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, userStatus=0,
                                                   score="1.2")
            time.sleep(3)
        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]
        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                expected_value=2,
                res_accurate=False,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_离店_抓拍节点_去重时间内_上传相同的人脸不会去重(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备随机上报两张人脸图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, userStatus=4,
                                                   score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, userStatus=4,
                                                   score="1.2")
            time.sleep(3)
        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                expected_value=2,
                res_accurate=False,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=-1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_店内徘徊_抓拍节点_去重时间内_上传相同的人脸不会去重(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备随机上报两张人脸图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, userStatus=3,
                                                   score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, userStatus=3,
                                                   score="1.2")
            time.sleep(3)

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                expected_value=2,
                res_accurate=False,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=-1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_店外_抓拍节点_去重时间内_上传相同的人脸不会去重(self, 关联_抓拍子节点_进店, 关联_设备绑定节点):
        with allure.step('前置条件：模拟设备随机上报两张人脸图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, userStatus=1,
                                                   score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], img_path=image_path, userStatus=1,
                                                   score="1.2")
            time.sleep(3)

        with allure.step('准备用例查询入参'):
            areaCodesList = [关联_抓拍子节点_进店["areaCode"]]

        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=areaCodesList,
                res_accurate=False,
                expected_value=2,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=-1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_进店_门店下创建两个抓拍节点_选择门店节点查看抓拍列表_门店去重时间内不会去重(self, 关联_门店下创建两个抓拍节点_绑定节点):
        with allure.step('前置条件：两个节点上传相同的图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            device_1 = 关联_门店下创建两个抓拍节点_绑定节点[2]
            device_2 = 关联_门店下创建两个抓拍节点_绑定节点[3]
            gen_devData.simulate_device_upload_pic(device_1, img_path=image_path, score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(device_2, img_path=image_path, score="1.2")
            time.sleep(3)
        # 选择门店查看抓拍列表
        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=[关联_门店下创建两个抓拍节点_绑定节点[0][:14]],
                res_accurate=False,
                expected_value=2,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_无状态_门店下创建两个抓拍节点_选择门店节点查看抓拍列表_门店去重时间内不会去重(self, 关联_门店下创建两个抓拍节点_绑定节点):
        with allure.step('前置条件：两个节点上传相同的图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            device_1 = 关联_门店下创建两个抓拍节点_绑定节点[2]
            device_2 = 关联_门店下创建两个抓拍节点_绑定节点[3]
            gen_devData.simulate_device_upload_pic(device_1, img_path=image_path, score="1.2", userStatus=0)
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(device_2, img_path=image_path, score="1.2", userStatus=0)
            time.sleep(3)
        # 选择门店查看抓拍列表
        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=[关联_门店下创建两个抓拍节点_绑定节点[0][:14]],
                res_accurate=False,
                expected_value=2,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=0)

    @allure.severity(allure.severity_level.NORMAL)
    def test_离店_门店下创建两个抓拍节点_选择门店节点查看抓拍列表_门店去重时间内不会去重(self, 关联_门店下创建两个抓拍节点_绑定节点):
        with allure.step('前置条件：两个节点上传相同的图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            device_1 = 关联_门店下创建两个抓拍节点_绑定节点[2]
            device_2 = 关联_门店下创建两个抓拍节点_绑定节点[3]
            gen_devData.simulate_device_upload_pic(device_1, img_path=image_path, score="1.2", userStatus=4)
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(device_2, img_path=image_path, score="1.2", userStatus=4)
            time.sleep(3)
        # 选择门店查看抓拍列表
        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=[关联_门店下创建两个抓拍节点_绑定节点[0][:14]],
                res_accurate=False,
                expected_value=2,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=-1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_店内徘徊_门店下创建两个抓拍节点_选择门店节点查看抓拍列表_门店去重时间内不会去重(self, 关联_门店下创建两个抓拍节点_绑定节点):
        with allure.step('前置条件：两个节点上传相同的图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            device_1 = 关联_门店下创建两个抓拍节点_绑定节点[2]
            device_2 = 关联_门店下创建两个抓拍节点_绑定节点[3]
            gen_devData.simulate_device_upload_pic(device_1, img_path=image_path, score="1.2", userStatus=3)
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(device_2, img_path=image_path, score="1.2", userStatus=3)
            time.sleep(3)
        # 选择门店查看抓拍列表
        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=[关联_门店下创建两个抓拍节点_绑定节点[0][:14]],
                res_accurate=False,
                expected_value=2,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=-1)

    @allure.severity(allure.severity_level.NORMAL)
    def test_店外_门店下创建两个抓拍节点_选择门店节点查看抓拍列表_门店去重时间内不会去重(self, 关联_门店下创建两个抓拍节点_绑定节点):
        with allure.step('前置条件：两个节点上传相同的图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            device_1 = 关联_门店下创建两个抓拍节点_绑定节点[2]
            device_2 = 关联_门店下创建两个抓拍节点_绑定节点[3]
            gen_devData.simulate_device_upload_pic(device_1, img_path=image_path, score="1.2", userStatus=1)
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(device_2, img_path=image_path, score="1.2", userStatus=1)
            time.sleep(3)
        # 选择门店查看抓拍列表
        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=[关联_门店下创建两个抓拍节点_绑定节点[0][:14]],
                res_accurate=False,
                expected_value=2,
            )
        utils.snap_node_identification(response=res_info, expect_snapRecordStatus=-1)

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点", ["1", "2", "3"], indirect=True)  # 2 楼层汇总节点  3 其它汇总节点
    def test_汇总节点下_门店汇总_楼层汇总_其它汇总_创建两个抓拍节点_选择汇总节点查看抓拍列表_去重时间内相同的人脸会被去重(self, 关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点):
        with allure.step('前置条件：两个节点上传相同的图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点[2], img_path=image_path, score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点[3], img_path=image_path, score="1.2")
            time.sleep(3)
        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=[关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点[0][:19]],
                res_accurate=False,
                expected_value=2,
            )
            utils.snap_node_identification(response=res_info, expect_snapRecordStatus=0, expect_collectRecordStatus=1)

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点_出店逻辑", ["1", "2", "3"], indirect=True)  # 1 门店汇总节点  2 楼层汇总节点  3 其它汇总节点
    def test_汇总节点下_门店汇总_楼层汇总_其它汇总_创建出店逻辑两个抓拍节点_选择汇总节点查看抓拍列表_去重时间内相同的人脸不会被去重(self, 关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点_出店逻辑):
        with allure.step('前置条件：两个节点上传相同的图片'):
            image_path = gen_bnsData.get_face_picture(index=1)
            gen_devData.simulate_device_upload_pic(关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点_出店逻辑[2], img_path=image_path, score="1.2")
            time.sleep(1)
            gen_devData.simulate_device_upload_pic(关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点_出店逻辑[3], img_path=image_path, score="1.2")
            time.sleep(3)
        with allure.step('接口请求'):
            res_info = api_admin.scn_snap_list(
                areaCodesList=[关联_参数化门店汇总节点下创建两个抓拍节点_绑定节点_出店逻辑[0][:19]],
                res_accurate=False,
                expected_value=2,
            )
            utils.snap_node_identification(response=res_info, expect_snapRecordStatus=-1, expect_collectRecordStatus=-1)
