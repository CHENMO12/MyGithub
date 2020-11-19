# -*- coding: utf-8 -*-
# @Time    : 2019/7/14 23:52
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : test_smoke_cases.py

import pytest
import allure
import time

from bns.dkyj.utils import get_md5Password_from_mysql_in_mall
from bns import dkyj
from bns.dkyj.api import Api    # 业务api的调用入口
from bns.iot.iotapi import IotApi   # 业务api的调用入口
from base.helper import JsonHelper, AllureHelper  # json信息提取
import testdata                     # 可随机化的简单参数
from case import utils              # 可复用的用例步骤
from testdata import fixed_bnsData
from testdata import  gen_bnsData
from testdata import  gen_devData

api_admin = Api(username=None,password=None)
iot_api_admin = IotApi(username=None,password=None)

@allure.feature('冒烟用例')
@allure.story('主功能')
class TestSmoke():

    def test_基本的数据处理流程_普客及去重(self, api_technicalSupport, 关联_抓拍子节点_进店, 关联_设备绑定节点):

        with allure.step('前置条件：模拟设备上报一张人脸图片'):
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], score=1.2)

        with allure.step('店客云及技术支持：查看抓拍列表'):
            actual_count = api_technicalSupport.scn_snap_list(areaCodesList=[关联_抓拍子节点_进店["areaCode"]], expected_value=1, res_accurate=True)
            AllureHelper.assert_equal("抓拍列表人数统计",1, actual_count)

        with allure.step('店客云及技术支持：查看访客列表'):
            actual_count = api_technicalSupport.scn_snap_visit_list(areaCode=关联_抓拍子节点_进店["areaCode"], expected_value=1, res_accurate=True)
            AllureHelper.assert_equal("访客列表人数统计",1, actual_count)

        with allure.step('前置条件：去重时间内模拟设备上报同一张人脸图片'):
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], score=1.2)

        with allure.step('店客云及技术支持：查看抓拍列表'):
            actual_count = api_technicalSupport.scn_snap_list(areaCodesList=[关联_抓拍子节点_进店["areaCode"]], expected_value=2, res_accurate=True)
            AllureHelper.assert_equal("抓拍列表人数统计",2, actual_count)

        with allure.step('店客云及技术支持：查看访客列表'):
            actual_count = api_technicalSupport.scn_snap_visit_list(areaCode=关联_抓拍子节点_进店["areaCode"], expected_value=1, res_accurate=True)
            AllureHelper.assert_equal("访客列表人数统计",1, actual_count)

    def test_基本的数据处理流程_会员注册及识别(self, api_technicalSupport, 关联_抓拍子节点_进店, 关联_设备绑定节点):

        with allure.step('前置条件：模拟设备上报一张人脸图片'):
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], score=1.2)

        with allure.step('店客云及技术支持：查看访客列表'):
            res = api_technicalSupport.scn_snap_visit_list(areaCode=关联_抓拍子节点_进店["areaCode"], expected_value=1)
            visitor_count = JsonHelper.parseJson_by_objectpath(res, "count($..*[@.userType is 0])")
            AllureHelper.assert_equal("访客列表普客人数", 1, visitor_count)

        with allure.step('店客云及技术支持：注册人脸为会员'):
            faceId = JsonHelper.parseJson_by_objectpath(res, "$..*['faceId']", res_firstOne=True)
            imagePath = JsonHelper.parseJson_by_objectpath(res, "$..*['featureImageUrl']", res_firstOne=True)
            shopAreaCode = JsonHelper.parseJson_by_objectpath(res, "$..*['mallCode']", res_firstOne=True)
            api_technicalSupport.scn_member_add(mallareaCode=shopAreaCode, imagePath=imagePath, faceId=faceId)

        with allure.step('店客云及技术支持：查看访客列表'):
            userType = 0
            i = 0
            while userType == 0 and i < 20:
                res = api_technicalSupport.scn_snap_visit_list(areaCode=关联_抓拍子节点_进店["areaCode"], expected_value=1)
                userType = JsonHelper.parseJson_by_objectpath(res, "$..*['userType']", res_firstOne=True)
                i += 1
                time.sleep(1)
            member_count = JsonHelper.parseJson_by_objectpath(res, "count($..*[@.userType is 1])",res_allowNone=True)
            AllureHelper.assert_equal("访客列表会员人数", 1, member_count)

        with allure.step('前置条件：去重时间内模拟设备上报同一张人脸图片'):
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], score=1.2)

        with allure.step('店客云及技术支持：查看抓拍列表'):
            i = 0
            while member_count < 2 and i < 20:
                res = api_technicalSupport.scn_snap_list(areaCodesList=[关联_抓拍子节点_进店["areaCode"]], expected_value=1)
                member_count = JsonHelper.parseJson_by_objectpath(res, "count($..*[@.userType is 1])",res_allowNone=True)
                i += 1
                time.sleep(1)
            AllureHelper.assert_equal("抓拍列表会员人数", 2, member_count)

        with allure.step('店客云及技术支持：查看访客列表'):
            res = api_technicalSupport.scn_snap_visit_list(areaCode=关联_抓拍子节点_进店["areaCode"], expected_value=1)
            member_count = JsonHelper.parseJson_by_objectpath(res, "count($..*[@.userType is 1])", res_allowNone=True)
            AllureHelper.assert_equal("访客列表会员人数", 1, member_count)

    def test_基本的数据处理流程_去重时间外普客多次到访(self, api_technicalSupport, 关联_抓拍子节点_进店, 关联_设备绑定节点):

        with allure.step('前置条件：模拟设备上报一张人脸图片'):
            gen_devData.simulate_device_upload_pic(关联_设备绑定节点["deviceCodeOrBar"], score=1.2)

        with allure.step('店客云及技术支持：查看抓拍列表'):
            actual_count = api_technicalSupport.scn_snap_list(areaCodesList=[关联_抓拍子节点_进店["areaCode"]], expected_value=1, res_accurate=True)
            AllureHelper.assert_equal("抓拍列表人数统计",1, actual_count)

        with allure.step('店客云及技术支持：查看访客列表'):
            actual_count = api_technicalSupport.scn_snap_visit_list(areaCode=关联_抓拍子节点_进店["areaCode"], expected_value=1, res_accurate=True)
            AllureHelper.assert_equal("访客列表人数统计",1, actual_count)

        with allure.step('前置条件：去重时间外模拟设备上报同一张人脸图片'):
            gen_devData.simulate_device_upload_pic(deviceCode=关联_设备绑定节点["deviceCodeOrBar"], img_time=gen_bnsData.TimeHelper.get_custom_time(timestamp_offset=4000), score=1.2)

        with allure.step('店客云及技术支持：查看抓拍列表'):
            actual_count = api_technicalSupport.scn_snap_list(areaCodesList=[关联_抓拍子节点_进店["areaCode"]], expected_value=2, res_accurate=True)
            AllureHelper.assert_equal("抓拍列表人数统计",2, actual_count)
            # TODO：验证回头客属性

        with allure.step('店客云及技术支持：查看访客列表'):
            actual_count = api_technicalSupport.scn_snap_visit_list(areaCode=关联_抓拍子节点_进店["areaCode"], expected_value=2, res_accurate=True)
            AllureHelper.assert_equal("访客列表人数统计",2, actual_count)
            # TODO：验证回头客属性

    def test_基本权限操作流程_运营用户多权限(self, 关联_门店节点, 关联_门店节点2):

        with allure.step('超级管理员：创建账号A，关联所有角色权限(技术支持，数据修正，安装人员)'):
            api_admin = Api()
            userName = gen_bnsData.random_operateUser_userName()
            userPhone = gen_bnsData.random_operateUser_userPhone()
            roleId = fixed_bnsData.operateUserId.techSupport.value
            areaCodesList = ["0000"]
            roleId2 = fixed_bnsData.operateUserId.data_correct.value
            areaCodesList2 = [关联_门店节点["areaCode"]]
            roleId3 = fixed_bnsData.operateUserId.installation_person.value
            areaCodesList3 = [关联_门店节点2["areaCode"]]

            res_json = api_admin.bns_operateUser_add(userName=userName, userPhone=userPhone,
                                                     roleId=roleId, areaCodesList=areaCodesList,
                                                     roleId2=roleId2, areaCodesList2=areaCodesList2,
                                                     roleId3=roleId3, areaCodesList3=areaCodesList3)

            with allure.step("校验: 业务状态码是否正确"):
                actual_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")
                AllureHelper.assert_equal("业务状态码", actual_code, 0)

            with allure.step('超级管理员：获取创建账号A对应UserID及账号密码'):
                userInfo = api_admin.bns_operateUser_list(userInfo=userPhone)
                userId_A = JsonHelper.parseJson_by_objectpath(userInfo, "$..*[@.id]", res_firstOne=True)
                password_by_md5 = get_md5Password_from_mysql_in_mall(userPhone)

        with allure.step('登录账号A校验：包含安装人员角色的账号不可登录'):
            res = dkyj.BusinessApi.bns_user_login(userName=userPhone, userPasswd=password_by_md5)
            with allure.step("校验: 业务状态码是否正确"):
                actual_code = JsonHelper.parseJson_by_objectpath(res, "$.response_data.code")
                expect_code = 2037
                AllureHelper.assert_equal("业务状态码", actual_code, expect_code)
            with allure.step("校验: 提示信息是否正确"):
                actual_msg = JsonHelper.parseJson_by_objectpath(res, "$.response_data.message")
                expect_msg = "安装人员仅允许在APP登录"
                AllureHelper.assert_equal("提示信息", actual_msg, expect_msg)
                
        with allure.step('超级管理员：创建账号B，关联所有角色权限(技术支持，数据修正)'):
            userName = gen_bnsData.random_operateUser_userName()
            userPhone = gen_bnsData.random_operateUser_userPhone()
            roleId = fixed_bnsData.operateUserId.techSupport.value
            areaCodesList = ["0000"]
            roleId2 = fixed_bnsData.operateUserId.data_correct.value
            areaCodesList2 = [关联_门店节点["areaCode"]]
    
            res_json = api_admin.bns_operateUser_add(userName=userName, userPhone=userPhone, roleId=roleId, areaCodesList=areaCodesList, roleId2=roleId2, areaCodesList2=areaCodesList2)
    
            with allure.step("校验: 业务状态码是否正确"):
                actual_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")
                AllureHelper.assert_equal("业务状态码", actual_code, 0)
    
            with allure.step('超级管理员：获取创建账号B对应UserID及账号密码'):
                userInfo = api_admin.bns_operateUser_list(userInfo=userPhone)
                userId_B = JsonHelper.parseJson_by_objectpath(userInfo, "$..*[@.id]", res_firstOne=True)
                password_by_md5 = get_md5Password_from_mysql_in_mall(userPhone)

        with allure.step('步骤: 登录账号B及修改密码为Dj123456'):
            api_operateUser = Api(username=userPhone, password=password_by_md5)
            api_operateUser.bns_operateUser_modifyPassword(oldPasswordMd5=password_by_md5,newPassword="Dj123456")
            api_operateUser = Api(username=userPhone, password="Dj123456")
            res = api_operateUser.bns_operateUser_getUserRoleList()

            with allure.step('校验: 账号B关联的角色权限ID列表'):
                userRoleId_list = JsonHelper.parseJson_by_objectpath(res, "$..*['roleId']")
                expect_userRoleId_list = [2,3]
                AllureHelper.assert_equal("角色权限ID列表", sorted(userRoleId_list), expect_userRoleId_list)

                userId_techSupport = JsonHelper.parseJson_by_objectpath(res, "$..*[@.'roleId' is 2].id",res_firstOne=True)
                userId_data_correct = JsonHelper.parseJson_by_objectpath(res, "$..*[@.'roleId' is 3].id",res_firstOne=True)

        with allure.step('步骤: 选择账号B，切换技术支持角色'):
            res = api_operateUser.bns_operateUser_changeUserRole(userId=userId_techSupport)
            with allure.step("校验: 业务状态码是否正确"):
                actual_code = JsonHelper.parseJson_by_objectpath(res, "$.response_data.code")
                AllureHelper.assert_equal("业务状态码", actual_code, 0)
            with allure.step('校验: 技术支持角色权限'):
                # TODO:待完成技术支持权限功能校验
                pass

        with allure.step('步骤: 选择账号B，切换数据修正角色'):
            res = api_operateUser.bns_operateUser_changeUserRole(userId=userId_data_correct)
            with allure.step("校验: 业务状态码是否正确"):
                actual_code = JsonHelper.parseJson_by_objectpath(res, "$.response_data.code")
                AllureHelper.assert_equal("业务状态码", actual_code, 0)
            with allure.step('校验: 数据修正角色权限'):
                # TODO:待完成数据修正权限功能校验
                pass

        with allure.step('数据清理: 删除账号A'):
            api_admin_new = Api()
            res = api_admin_new.bns_operateUser_delete(userId=userId_A)
            actual_code = JsonHelper.parseJson_by_objectpath(res, "$.response_data.code")
            AllureHelper.assert_equal("业务状态码", actual_code, 0)

        with allure.step('数据清理: 删除账号B'):
            res = api_admin_new.bns_operateUser_delete(userId=userId_B)
            actual_code = JsonHelper.parseJson_by_objectpath(res, "$.response_data.code")
            AllureHelper.assert_equal("业务状态码", actual_code, 0)






