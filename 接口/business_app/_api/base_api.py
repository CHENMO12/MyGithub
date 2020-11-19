# -*- coding: utf-8 -*-
# @Time    : 2019/7/5 11:23
# @Author  : Huizi Cai
import requests
import base64
import time
import json
import hashlib
from business_app.smartShop_util.myrequest import MyRequest
from business_app.smartShop_util.mycommon import parseJson_by_objectpath
from business_app.smartShop_util.mylog import MyLog
from business_app._config.config import Config
from business_app._api.config import *


class BaseApi:
    def __init__(self):
        self.config = Config()
        self.request = MyRequest()
        self.config = Config()
        self.log = MyLog()
        self.session = requests.session()
        response = self.login().json()
        print(response)
        text = parseJson_by_objectpath(response, "$.*.message")
        self.token = parseJson_by_objectpath(response, "$.*.data.token")
        self.areaCode = parseJson_by_objectpath(response, "$.*.data.areaCode")

        try:
            if text == "登录成功":
                self.log.log_info("登入成功...")
            else:
                self.log.log_error("登入失败...")
                exit("登入失败...")
        except:
            self.log.log_warning("登录时出现异常:请检查域名信息是否正确...")
            exit(1)

    def login(self):
        self.host = self.config.get_netty_host + "/businessApp/user/login"
        password = str_md5(self.config.get_password)
        self.headers = {"Content-Type": "application/json"}
        data = {"password": password, "phoneNo": self.config.get_username}
        return self.session.post(url=self.host, data=json.dumps(data), headers=self.headers)

    # 抓拍列表数据  /businessApp/snap/snapDataList
    # 参数说明：
    # token：用户token（必填）
    # startDate：开始日期(格式例如：2019 - 03 - 26)
    # endDate：结束日期(格式例如：2019 - 03 - 26)
    # areaCode: 区域编码(000 - 000 - 000)（必填）
    # dataType: 类型(0:总客流;1:未跟进;2:未成单;3:已成单) （选填）

    def base_datalist(self, required_token=None, required_areaCode=None, optional_startDate=None, optional_endDate=None,
                      optional_dataType=None):
        self.host = self.config.get_netty_host + "/businessApp/snap/snapDataList"
        data = {}
        if required_token: data["token"] = required_token
        if required_areaCode: data["areaCode"] = required_areaCode
        if optional_startDate: data["startDate"] = optional_startDate
        if optional_endDate: data["endDate"] = optional_endDate
        if optional_dataType: data["dataType"] = optional_dataType
        self.log.log_info("抓拍列表数据请求参数:%s" % data)
        return self.session.post(url=self.host, data=json.dumps(data), headers=self.headers)

    #  /businessApp/snap/savePersonTraceInfo  跟进信息
    # 参数说明：
    # areaCode: 区域编码(000 - 000 - 000) （必填）
    # phone: 客户手机号
    # personName：客户名称
    # image：图片转成base64数据格式（必填）
    # isTrade: 是否成单(0:否;
    # 1: 是)
    # tradeSum: 5000, // 成单金额
    # brands: 关注品类(多个用逗号隔开)
    # used: 用途(多个用逗号隔开)
    # intention: 意向(多个用逗号隔开)
    # remark: 记录备注
    def base_save_trace_info(self, required_token=None, required_snapId=None, required_areaCode=None,
                             required_phone=None, optional_personName=None,
                             required_image=None, required_isTrade=None, optionael_brands=None, optional_used=None,
                             optional_intention=None, optional_remark=None):
        self.host = self.config.get_netty_host + "/businessApp/snap/savePersonTraceInfo"
        data = {}
        if required_snapId: data["snapId"] = required_snapId
        if required_token: data["token"] = required_token
        if required_areaCode: data["areaCode"] = required_areaCode
        if required_phone: data["phone"] = required_phone
        if optional_personName: data["personName"] = optional_personName
        if required_image: data["imagePath"] = required_image
        if required_isTrade is not None: data["isTrade"] = required_isTrade
        if optionael_brands: data["brands"] = optionael_brands
        if optional_intention: data["intention"] = optional_intention
        if optional_remark: data["remark"] = optional_remark
        if optional_used: data["used"] = optional_used
        self.log.log_info("跟进信息请求参数:%s" % data)
        return self.session.post(url=self.host, data=json.dumps(data), headers=self.headers)

    # POST /businessApp/snap/addTraceInfo  添加跟进信息
    def base_add_trace_info(self, required_token=None, required_areaCode=None, required_isTrade=None,
                            required_snapId=None, required_personCode=None, required_personName=None,
                            required_phone=None, optional_remark=None, optionael_brands=None, optional_used=None,
                            optional_intention=None):
        self.host = self.config.get_netty_host + "/businessApp/snap/addTraceInfo"
        data = {}
        if required_snapId: data["snapId"] = required_snapId
        if required_token: data["token"] = required_token
        if required_areaCode: data["areaCode"] = required_areaCode
        if required_personName: data["personName"] = required_personName
        if required_isTrade: data["isTrade"] = required_isTrade
        if optionael_brands: data["brands"] = optionael_brands
        if optional_intention: data["intention"] = optional_intention
        if optional_remark: data["remark"] = optional_remark
        if optional_used: data["used"] = optional_used
        if required_personCode: data["personCode"] = required_personCode
        if required_phone: data["phone"] = required_phone
        self.log.log_info("添加跟进信息请求参数:%s" % data)
        return self.session.post(url=self.host, data=json.dumps(data), headers=self.headers)

    # /businessApp/snap/snapDataCount  抓拍列表统计
    # token：用户token（必填）
    # startDate：开始日期(格式例如：2019 - 03 - 26)
    # endDate：结束日期(格式例如：2019 - 03 - 26)
    # areaCode: 区域编码(000 - 000 - 000)（必填）
    # 抓拍列表统计
    def base_snap_data_count(self, required_token=None, required_areaCode=None, optional_startDate=None,
                             optional_endDate=None):
        self.host = self.config.get_netty_host + "/businessApp/snap/snapDataCount"
        data = {}
        if required_token: data['token'] = required_token
        if required_areaCode: data['areaCode'] = required_areaCode
        if optional_startDate: data['startDate'] = optional_startDate
        if optional_endDate: data['endDate'] = optional_endDate
        self.log.log_info("抓拍列表统计请求参数:%s" % data)
        return self.session.post(url=self.host, data=json.dumps(data), headers=self.headers)

    # 标记为非客户
    def base_mark_snap_type(self, required_token=None, required_snapId=None, required_vipType=None):
        self.host = self.config.get_netty_host + "/businessApp/snap/markSnapType"
        data = {}
        if required_token: data['token'] = required_token
        if required_snapId: data['snapId'] = required_snapId
        if required_vipType is not None: data['vipType'] = required_vipType
        print(data['vipType'])
        self.log.log_info("标记为非客户请求参数:%s" % data)
        return self.session.post(url=self.host, data=json.dumps(data), headers=self.headers)

    # 品牌列表
    def base_brand_list(self, requied_token=None):
        self.host = self.config.get_netty_host + "/businessApp/area/brandList"
        data = {}
        if requied_token: data["token"] = requied_token
        self.log.log_info("品牌列表请求参数:%s" % data)
        return self.session.post(url=self.host, data=json.dumps(data), headers=self.headers)

    # 切换品牌  /businessApp/user/changeArea
    def base_change_brand_area(self, required_areaCode=None, required_token=None):
        self.url = self.config.get_netty_host + "/businessApp/user/changeArea"
        data = {}
        if required_areaCode: data["areaCode"] = required_areaCode
        if required_token: data["token"] = required_token
        self.log.log_info("切换品牌 请求参数:%s" % data)
        return self.session.post(data=json.dumps(data), url=self.url, headers=self.headers)

    # 我的客户列表
    # POST /businessApp/snap/personInfoList
    # startDate：开始日期(格式例如：2019 - 03 - 26)
    # endDate：结束日期(格式例如：2019 - 03 - 26)
    # areaCode: 区域编码(000 - 000 - 000)
    # vipType: vip类型(0:非客户;
    # 1: 无效客户;
    # 2: 潜客;
    # 3: 成单)
    # name: 手机号或者名称搜索条件

    def base_my_customer(self, required_token=None, required_areaCode=None, optional_startDate=None,
                         optional_endDate=None,
                         optional_vipType=None, ):
        self.host = self.config.get_netty_host + "/businessApp/snap/personInfoList"
        data = {}
        if required_token: data["token"] = required_token
        if required_areaCode: data["areaCode"] = required_areaCode
        if optional_startDate: data["startDate"] = optional_startDate
        if optional_endDate: data['endDate'] = optional_endDate
        if optional_vipType is not None: data['vipType'] = optional_vipType
        self.log.log_info("我的客户列表请求参数:%s" % data)
        return self.session.post(data=json.dumps(data), url=self.host, headers=self.headers)

    # 修改客户信息
    # POST /businessApp/snap/modifyTraceInfo
    # token：用户token（必填）
    # personCode:客户id（必填）
    # phone:客户手机号
    # personName：客户名称
    def base_change_customer_info(self, required_token=None, required_personCode=None, optional_phone=None,
                                  optional_personName=None):
        self.url = self.config.get_netty_host + "/businessApp/snap/modifyPersonInfo"
        data = {}
        if required_token: data["token"] = required_token
        if required_personCode: data["personCode"] = required_personCode
        if optional_phone: data['phone'] = optional_phone
        if optional_personName: data['personName'] = optional_personName
        self.log.log_info("修改客户信息请求参数:%s" % data)
        return self.session.post(data=json.dumps(data), url=self.url, headers=self.headers)

    # 历史跟进记录
    # {
    #     "areaCode": "string",
    #     "personCode": 0,
    #     "token": "string"
    # }
    def base_trace_info_list(self, required_token=None, required_areaCode=None, required_personCode=None):
        self.url = self.config.get_netty_host + "/businessApp/snap/traceInfoList"
        data = {}
        if required_token: data["token"] = required_token
        if required_areaCode: data["areaCode"] = required_areaCode
        if required_personCode: data["personCode"] = required_personCode
        self.log.log_info("历史跟进记录请求参数:%s" % data)
        return self.session.post(data=json.dumps(data), url=self.url, headers=self.headers)

    # 关联
    def base_relate_customer(self, required_token=None, required_areaCode=None, required_imagePathList=None,
                             required_imageHeader=None, required_isTrade=None, required_snapId=None,
                             required_snapIdList=None, required_personCode=None, required_personName=None,
                             required_phone=None):
        self.url = self.config.get_netty_host + "/businessApp/snap/saveRelatePerson"
        data = {}
        if required_token: data['token'] = required_token
        if required_snapId: data["snapId"] = required_snapId
        if required_areaCode: data["areaCode"] = required_areaCode
        if required_personName: data["personName"] = required_personName
        if required_isTrade: data["isTrade"] = required_isTrade
        if required_personCode is not None: data["personCode"] = required_personCode
        if required_phone: data["phone"] = required_phone
        if required_imageHeader: data['imageHeader'] = required_imageHeader
        if required_imagePathList: data['imagePathList'] = required_imagePathList
        if required_snapIdList: data['snapIdList'] = required_snapIdList
        self.log.log_info("关联请求参数:%s" % data)
        return self.session.post(data=json.dumps(data), url=self.url, headers=self.headers)

    # 店员业绩
    def base_clerk_tradelist(self, required_areaCode=None, required_token=None, optional_startDate=None,
                             optional_endDate=None):
        self.url = self.config.get_netty_host + "/businessApp/report/clerkTradeList"
        data = {}
        if required_areaCode: data['areaCode'] = required_areaCode
        if required_token: data['token'] = required_token
        if optional_endDate: data['endDate'] = optional_endDate
        if optional_startDate: data['startDate'] = optional_startDate
        self.log.log_info("店员业绩请求参数:%s" % data)
        return self.session.post(data=json.dumps(data), url=self.url, headers=self.headers)

    # 恢复为初次到访客户
    def base_resume_first_customer(self, reqiured_snapId=None, required_token=None):
        self.url = self.config.get_netty_host + "/businessApp/snap/resumeSnapType"
        data = {}
        if reqiured_snapId: data['snapId'] = reqiured_snapId
        if required_token: data['token'] = required_token
        self.log.log_info("恢复为初次到访客户请求参数:%s" % data)
        return self.session.post(data=json.dumps(data), url=self.url, headers=self.headers)


if __name__ == '__main__':
    api = BaseApi()
    config = Config()
    # response = api.brand_list().json()
    # print(response)
    response2 = api.base_datalist().json()
    # print("*******")
    print(response2)
    # print("*******")
    # response3 = api.base_trace_info_list(required_token=api.token, required_areaCode=api.areaCode,
    #                                      required_personCode=252).json()
    # print("*******")
    # print(response3)
