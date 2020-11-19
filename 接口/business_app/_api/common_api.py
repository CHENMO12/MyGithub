# -*- coding: utf-8 -*-
# @Time    : 2019/7/5 11:23
# @Author  : Huizi Cai
import requests
import time
import json
import hashlib
from business_app.smartShop_util.myrequest import MyRequest
from business_app.smartShop_util.mycommon import parseJson_by_objectpath
from business_app.smartShop_util.mylog import MyLog
from business_app._config.config import Config
from business_app._api.config import get_current_time, random_num, random_str, get_num, get_num02
from business_app._api.config import *
from business_app._api.base_api import BaseApi
from business_app._testcase.data_upload import UploadByNetty

config = Config()
upload = UploadByNetty(config.get_device, config.get_web_domain)


class CommonApi(BaseApi):
    def __init__(self):
        super().__init__()
        self.config = Config()

    # 抓拍列表
    def common_datalist(self, required_token=None, required_areaCode=None, optional_startDate=None,
                        optional_endDate=None,
                        optional_dataType=None):
        # for _ in range(0,1):
        #     upload.run()
        # time.sleep(5)
        # response_areaCode = parseJson_by_objectpath(self.common_brand_list().json(), "$.*.data.areaCode")[1]
        # # print(response_areaCode)
        # self.common_change_brand_area(required_areaCode=response_areaCode)
        if required_token is None: required_token = self.token
        if required_areaCode is None: required_areaCode = self.areaCode
        if optional_startDate is None: optional_startDate = get_current_time()
        if optional_endDate is None: optional_endDate = get_current_time()
        if optional_dataType is None: optional_dataType = 0
        return self.base_datalist(required_token=required_token, required_areaCode=required_areaCode,
                                  optional_startDate=optional_startDate, optional_dataType=optional_dataType,
                                  optional_endDate=optional_endDate)

    # 抓拍统计
    def common_snap_data_count(self, required_token=None, required_areaCode=None, optional_startDate=None,
                               optional_endDate=None):
        if required_token is None: required_token = self.token
        if required_areaCode is None: required_areaCode = self.areaCode
        if optional_startDate is None: optional_startDate = get_current_time()
        if optional_endDate is None: optional_endDate = get_current_time()
        return self.base_snap_data_count(required_token=required_token, required_areaCode=required_areaCode,
                                         optional_startDate=optional_startDate, optional_endDate=optional_endDate)

    # 去跟进
    def common_save_trace_info(self, required_token=None, required_snapId=None, required_areaCode=None,
                               optional_phone=None, optional_personName=None,
                               required_image=None, required_isTrade=None, optionael_brands=None, optional_used=None,
                               optional_intention=None, optional_remark=None):
        self.response = self.common_datalist().json()
        self.snapId = \
            parseJson_by_objectpath(self.response, "$.*.data.snapId")[0]
        self.imagePath = parseJson_by_objectpath(self.response,
                                                 "$.*.data.imagePath")[0]
        if required_token is None: required_token = self.token
        if required_snapId is None: required_snapId = self.snapId
        if required_areaCode is None: required_areaCode = self.areaCode
        if optional_phone is None: optional_phone = random_num()
        if optional_personName is None: optional_personName = random_str()
        if required_image is None: required_image = self.imagePath
        if required_isTrade is None: required_isTrade = 0
        if optionael_brands is None: optionael_brands = ["黄金"]
        if optional_used is None: optional_used = ["自己用"]
        if optional_intention is None: optional_intention = "中"
        if optional_remark is None: optional_remark = "测试..."
        return self.base_save_trace_info(required_token=required_token, required_snapId=required_snapId,
                                         required_areaCode=required_areaCode, required_phone=optional_phone,
                                         optional_personName=optional_personName, required_image=required_image,
                                         required_isTrade=required_isTrade, optionael_brands=optionael_brands,
                                         optional_used=optional_used, optional_intention=optional_intention,
                                         optional_remark=optional_remark
                                         )

    # 标记为非客户
    def common_mark_snap_type(self, required_token=None, required_snapId=None, required_vipType=None):
        self.response = self.common_datalist().json()
        self.snapId = \
            parseJson_by_objectpath(self.response, "$.*.data.snapId")[0]
        if required_token is None: required_token = self.token
        if required_snapId is None: required_snapId = self.snapId
        if required_vipType is None: required_vipType = 0
        return self.base_mark_snap_type(required_token=required_token, required_snapId=required_snapId,
                                        required_vipType=required_vipType)

    # 追加跟进信息
    def common_add_trace_info(self, required_token=None, required_areaCode=None, required_isTrade=None,
                              required_phone=None, required_snapId=None, required_personCode=None,
                              required_personName=None,
                              optional_remark=None, optionael_brands=None, optional_used=None,
                              optional_intention=None):
        # for _ in range(0,1):
        #     upload.run()
        # time.sleep(5)
        self.common_save_trace_info()
        self.response = self.common_datalist().json()
        num = get_num(parseJson_by_objectpath(self.response,
                                              "$.*.data.personName"))
        self.personName = parseJson_by_objectpath(self.response,
                                                  "$.*.data.personName")[num]

        self.personCode = parseJson_by_objectpath(self.response,
                                                  "$.*.data.personCode")[num]

        self.phone = parseJson_by_objectpath(self.response,
                                             "$.*.data.phone")[num]
        self.snapId = \
            parseJson_by_objectpath(self.response, "$.*.data.snapId")[num]
        if required_token is None: required_token = self.token
        if required_areaCode is None: required_areaCode = self.areaCode
        if required_isTrade is None: required_isTrade = 1
        if required_snapId is None: required_snapId = self.snapId
        if required_personCode is None: required_personCode = self.personCode
        if required_personName is None: required_personName = self.personName
        if optional_remark is None: optional_remark = "追加记录..."
        if optionael_brands is None: optionael_brands = ["黄金", "白金", "钻石"]
        if optional_used is None: optional_used = ["送礼", "收藏", "自用"]
        if optional_intention is None: optional_intention = "高"
        if required_phone is None: required_phone = self.phone
        return self.base_add_trace_info(required_token=required_token, required_areaCode=required_areaCode,
                                        required_isTrade=required_isTrade, required_snapId=required_snapId,
                                        required_personCode=required_personCode,
                                        required_personName=required_personName, optional_remark=optional_remark,
                                        optionael_brands=optionael_brands, optional_used=optional_used,
                                        optional_intention=optional_intention, required_phone=required_phone)

    # 品牌列表
    def common_brand_list(self, requied_token=None):
        if requied_token is None: requied_token = self.token
        return self.base_brand_list(requied_token=requied_token)

    # 切换品牌
    def common_change_brand_area(self, required_areaCode=None, required_token=None):
        if required_token is None: required_token = self.token
        if required_areaCode is None: required_areaCode = self.areaCode
        return self.base_change_brand_area(required_token=required_token, required_areaCode=required_areaCode)

    # 我的客户列表
    # POST /businessApp/snap/personInfoList
    def common_my_customer(self, required_token=None, required_areaCode=None, optional_startDate=None,
                           optional_endDate=None,
                           optional_vipType=None):
        if required_token is None: required_token = self.token
        if required_areaCode is None: required_areaCode = self.areaCode
        if optional_startDate is None: optional_startDate = get_current_time()
        if optional_endDate is None: optional_endDate = get_current_time()
        if optional_vipType is None: optional_vipType = 3
        return self.base_my_customer(required_token=required_token, required_areaCode=required_areaCode,
                                     optional_startDate=optional_startDate, optional_endDate=optional_endDate,
                                     optional_vipType=optional_vipType)

    # 修改客户信息
    # POST /businessApp/snap/modifyTraceInfo
    def common_change_customer_info(self, required_token=None, required_personCode=None, optional_phone=None,
                                    optional_personName=None):
        self.response = self.common_datalist().json()
        self.phone02 = random_num()
        self.personName02 = random_str()
        num = get_num(parseJson_by_objectpath(self.response,
                                              "$.*.data.personName"))
        self.personCode02 = parseJson_by_objectpath(self.response,
                                                    "$.*.data.personCode")[num]

        if required_token is None: required_token = self.token
        if required_personCode is None: required_personCode = self.personCode02
        if optional_phone is None: optional_phone = self.phone02
        if optional_personName is None: optional_personName = self.personName02

        return self.base_change_customer_info(required_token=required_token, required_personCode=required_personCode,
                                              optional_personName=optional_personName, optional_phone=optional_phone,
                                              )

    # 关联
    def common_relate_customer(self, required_token=None, required_areaCode=None, required_imagePathList=None,
                               required_imageHeader=None, required_isTrade=None, required_snapId=None,
                               required_snapIdList=None, required_personCode=None, required_personName=None,
                               required_phone=None):
        self.response = self.common_datalist(optional_dataType=1).json()
        self.phone02 = random_num()
        self.personName02 = random_str()
        self.snapId = \
            parseJson_by_objectpath(self.response, "$.*.data.snapId")[0]
        self.imagePath = parseJson_by_objectpath(self.response,
                                                 "$.*.data.imagePath")[1]
        self.imageHeader = parseJson_by_objectpath(self.response,
                                                   "$.*.data.imagePath")[0]
        if required_token is None: required_token = self.token
        if required_areaCode is None: required_areaCode = self.areaCode
        if required_personCode is None: required_personCode = 0
        if required_snapId is None: required_snapId = self.snapId
        if required_imagePathList is None: required_imagePathList = [self.imagePath]
        if required_imageHeader is None: required_imageHeader = self.imageHeader
        if required_isTrade is None: required_isTrade = 1
        if required_personName is None: required_personName = self.personName02
        if required_phone is None: required_phone = self.phone02
        if required_snapIdList is None: required_snapIdList = [self.snapId - 1]

        return self.base_relate_customer(required_token=required_token, required_personCode=required_personCode,
                                         required_personName=required_personName, required_phone=required_phone,
                                         required_snapIdList=required_snapIdList,
                                         required_imageHeader=required_imageHeader,
                                         required_imagePathList=required_imagePathList,
                                         required_isTrade=required_isTrade, required_areaCode=required_areaCode,
                                         required_snapId=required_snapId)

    # 店员业绩
    def common_clerk_tradelist(self, required_areaCode=None, required_token=None, optional_startDate=None,
                               optional_endDate=None):
        if required_areaCode is None: required_areaCode = self.areaCode
        if required_token is None: required_token = self.token
        if optional_startDate is None: optional_startDate = get_current_time()
        if optional_endDate is None: optional_endDate = get_current_time()
        return self.base_clerk_tradelist(required_token=required_token, required_areaCode=required_areaCode
                                         , optional_startDate=optional_startDate, optional_endDate=optional_endDate)

    # 恢复为初次到访客户
    def common_resume_first_customer(self, reqiured_snapId=None, required_token=None):
        if required_token is None: required_token = self.token
        self.response = self.common_datalist().json()
        snapId = parseJson_by_objectpath(self.response, "$.*.data.snapId")[0]
        if reqiured_snapId is None: reqiured_snapId = snapId
        return self.base_resume_first_customer(required_token=required_token, reqiured_snapId=reqiured_snapId)


if __name__ == '__main__':
    # for _ in range(0, 2):
    #     upload.run()
    # time.sleep(5)
    api = CommonApi()
    response = api.common_datalist().json()
    print(response)
