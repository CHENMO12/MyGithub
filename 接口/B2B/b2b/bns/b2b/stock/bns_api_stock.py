#!/usr/bin/python3.7
# @Time : 2020/6/15 0015 16:42 
from base.decorators import allure_attach
from base.helper import JsonHelper
from testdata.gen_bnsData import *
from bns.b2b import BusinessApi
from bns.b2b.po.bns_api_po import BnsApi_Po
from bns.b2b.so.bns_api_so import BnsApi_So
from config import *
import json
import time

po_admin = BnsApi_Po()
so_admin = BnsApi_So()


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    # 仓库管理po
    @allure_attach("入库通知")
    def bns_po_stock_add(self):
        self.order = JsonHelper.parseJson_by_objectpath(po_admin.bns_po_list(), "$.retEntity..fpurchaseOrderId")[0]
        data_test = {
            "basicDTO": {"fpurchaseOrderId": self.order, "finStockId": None, "fpurchaseOrderEnterStockId": None,
                         "fpurchaseOrderReturnId": None, "fplanType": 1, "fplanTypeName": "BB自营分销1",
                         "fplanTypeProcess": 1, "fcorporateSubjectId": 102, "fourCompanyName": "深圳市天行云供应链有限公司",
                         "fsupplierId": 531, "fsupplierName": "哈哈供应商2", "fourCompanyLeader": "蔡惠子", "fpurchaseAid": 249,
                         "fsupplierLeader": "图图", "fsupplierLeaderPhone": "13026161548", "ftradeType": 1,
                         "fquotationMethod": "CPT", "fwarehouseId": "76", "fwarehouseName": None,
                         "fwarehouseAdminId": None, "fwarehouseAdminName": "刘丽君", "fdismissTheReason": None,
                         "fenterStockStatus": None, "fwarehouseEntryTime": None},
            "deliveryDTO": {"flogisticsMode": 1, "fcommonCarrierName": "11", "ftransportType": 1,
                            "flogisticsNumber": "11", "fsendTime": "2020-06-30", "fexpectedArrivalDate": "2020-06-30"},
            "skuDetailDTOS": [
                {"fpurchaseOrderEnterStockSkuId": None, "fpurchaseOrderEnterStockId": None, "fskuId": "118905006",
                 "fsendNum": 1, "fsurplusSendNum": 1, "fpurchaseAmount": 110, "fboxSize": 1, "fpalletNum": None,
                 "fbrandLabelName": "自有品牌", "fisCompleteInspection": 0, "fvalidtyEnd": "2020-06-22",
                 "fexpirationDate": 1095, "fcategoryName": "母婴用品", "fbrandName": "虎牌", "fbrandNameEng": "TIGER",
                 "fskuName": "TIGER虎牌 儿童保温杯MBR-T06G 吸管杯国际版 老虎 600ml", "fskuSpecification": "600ml",
                 "fskuInternationalNo": "4904710424933", "unit": "个", "factualStorageCost": 11.881188,
                 "factualStorageCostCn": 84.73188, "fskuBatch": "11", "poEnterStockSkuInnerDTOS": None, "index": 1},
                {"fpurchaseOrderEnterStockSkuId": None, "fpurchaseOrderEnterStockId": None, "fskuId": "GMH00831-J",
                 "fsendNum": 1, "fsurplusSendNum": 1, "fpurchaseAmount": 110, "fboxSize": 1, "fpalletNum": None,
                 "fbrandLabelName": "非品牌", "fisCompleteInspection": 1, "fvalidtyEnd": "2020-06-29",
                 "fexpirationDate": 1093, "fcategoryName": "美妆个护", "fbrandName": "SNP", "fbrandNameEng": "",
                 "fskuName": "SNP 韩国 老虎动物面膜保湿抗皱 25ml*10片", "fskuSpecification": "老虎动物面膜 25ml*10片",
                 "fskuInternationalNo": "8809237828652", "unit": "SNP", "factualStorageCost": 1,
                 "factualStorageCostCn": 7.1316, "fskuBatch": "11", "poEnterStockSkuInnerDTOS": None, "index": 2},
                {"fpurchaseOrderEnterStockSkuId": None, "fpurchaseOrderEnterStockId": None, "fskuId": "HJH05363-J",
                 "fsendNum": 1, "fsurplusSendNum": 1, "fpurchaseAmount": 110, "fboxSize": 1, "fpalletNum": None,
                 "fbrandLabelName": "代理品牌", "fisCompleteInspection": 0, "fvalidtyEnd": "2020-06-30",
                 "fexpirationDate": 0, "fcategoryName": "家居生活", "fbrandName": "ecolifelatex",
                 "fbrandNameEng": "12122323", "fskuName": "ecolifelatex 泰国 老虎乳胶枕头-老虎", "fskuSpecification": "老虎乳胶枕头-老虎",
                 "fskuInternationalNo": "8858991833150", "unit": "ecolifelatex", "factualStorageCost": 0.333333,
                 "factualStorageCostCn": 2.377198, "fskuBatch": "11", "poEnterStockSkuInnerDTOS": None, "index": 3}],
            "restInfoDTO": {"attachmentDOS": [
                {"fattachmentName": "账号.txt", "fattachmentUrl": "M00/0A/06/wKgA3175lJGAAL8qAAACyuMWYDo190.txt"}]},
            "financeDTO": {}}
        data_dev = {"basicDTO": {"fpurchaseOrderId": self.order, "fpurchaseOrderEnterStockId": None,
                                 "fpurchaseOrderReturnId": None, "fplanType": 1, "fcorporateSubjectId": 102,
                                 "fourCompanyName": "深圳市天行云供应链有限公司", "fsupplierId": 531, "fsupplierName": "哈哈供应商2",
                                 "fourCompanyLeader": "刘丽君", "fpurchaseAid": 120, "fsupplierLeader": "ben",
                                 "fsupplierLeaderPhone": "13264645696", "ftradeType": 1, "fquotationMethod": "CPT",
                                 "fwarehouseId": "76", "fwarehouseName": None, "fwarehouseAdminId": None,
                                 "fwarehouseAdminName": "张宇、赵金灏", "fdismissTheReason": None, "fenterStockStatus": None,
                                 "fwarehouseEntryTime": None},
                    "deliveryDTO": {"flogisticsMode": 1, "fcommonCarrierName": "京东", "ftransportType": 1,
                                    "flogisticsNumber": "1213121232", "fsendTime": get_current_time(day=30),
                                    "fexpectedArrivalDate": get_current_time()}, "skuDetailDTOS": [
                {"fpurchaseOrderEnterStockSkuId": None, "fpurchaseOrderEnterStockId": None, "fskuId": "118905121",
                 "fsendNum": 100, "fboxSize": 1, "fpalletNum": 1, "fvalidtyEnd": get_current_time(day=30),
                 "fexpirationDate": 9999,
                 "fcategoryName": "母婴用品", "fbrandName": "火柴猴", "fbrandNameEng": "Matchstick Monkey",
                 "fskuName": "英国Matchstick Monkey火柴猴牙胶宝宝婴儿咬咬安抚磨牙棒软硅胶—红色 个", "fskuSpecification": "个",
                 "fskuInternationalNo": "0611901211053", "unit": "红色", "factualStorageCost": 0.9901,
                 "factualStorageCostCn": 0.9901, "fskuBatch": None, "poEnterStockSkuInnerDTOS": None},
                {"fpurchaseOrderEnterStockSkuId": None, "fpurchaseOrderEnterStockId": None,
                 "fskuId": "DL157941907294202", "fsendNum": 100, "fboxSize": 1, "fpalletNum": 1,
                 "fvalidtyEnd": "2020-05-30", "fexpirationDate": 500, "fcategoryName": "服饰鞋包",
                 "fbrandName": "SWAROVSKI 施华洛世奇", "fbrandNameEng": "", "fskuName": "潘多拉项链 彩金",
                 "fskuSpecification": "彩金", "fskuInternationalNo": "121221", "unit": "**", "factualStorageCost": 2,
                 "factualStorageCostCn": 2, "fskuBatch": None, "poEnterStockSkuInnerDTOS": None},
                {"fpurchaseOrderEnterStockSkuId": None, "fpurchaseOrderEnterStockId": None, "fskuId": "GMH02965-J",
                 "fsendNum": 100, "fboxSize": 1, "fpalletNum": 1, "fvalidtyEnd": get_current_time(day=30),
                 "fexpirationDate": 1095,
                 "fcategoryName": "美妆个护", "fbrandName": "悦木之源", "fbrandNameEng": "",
                 "fskuName": "悦木之源 蘑菇水200ml 菌菇水 200ml", "fskuSpecification": "菌菇水 200ml",
                 "fskuInternationalNo": "717334229594", "unit": "悦木之源", "factualStorageCost": 0.0971,
                 "factualStorageCostCn": 0.0971, "fskuBatch": None, "poEnterStockSkuInnerDTOS": None}], "restInfoDTO": {
                "attachmentDOS": [
                    {"fattachmentName": "账号.txt", "fattachmentUrl": "M00/00/BB/wKgA316zt_iAXpUGAAACf-Z7Kz4463.txt"}]},
                    "financeDTO": {}}
        self.headers["use-node-method"] = "jsonRequest"
        if str(get_b2b_host) == "http://192.168.1.227:3003":
            data = data_dev
        else:
            data = data_test
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/purchase-order/stock/add".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # Three(response, self.bns_po_stock_add)
        # self.log.log_info("入库通知接口请求信息:{}".format(data))
        self.log.log_info("入库通知接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库通知列表查询")
    def bns_warehouse_queryNoticeList(self):
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "time": [],
            "fnoticeOrderNum": "",
            "frelationOrderNum": "",
            "fcompanyName": "",
            "fwarehouseId": "76",
            "fbusinessType": "",
            "fnoticeType": "",
            "fnoticeTimeStart": "",
            "fnoticeTimeEnd": ""
        }
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouse/queryNoticeList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # self.log.log_info("仓库通知列表接口请求信息:{}".format(data))
        self.log.log_info("仓库通知列接口返回信息:{}".format(response.json()))

        return response.json()

    @allure_attach("仓库确认入库接受")
    def bns_warehouseOrderInStock_saveOrUpdatePONotice(self):
        response = self.bns_warehouse_queryNoticeList()
        self.fstockId = JsonHelper.parseJson_by_objectpath(response, "$.data..fstockId")[0]
        self.fnoticeOrderNum = JsonHelper.parseJson_by_objectpath(response, "$.data..fnoticeOrderNum")[0]
        data = {
            "finStockStatus": 4,
            "finStockId": self.fstockId
        }
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderInStock/saveOrUpdatePONotice".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # self.log.log_info("仓库确认入库接受接口请求信息:{}".format(data))
        self.log.log_info("仓库确认入库接受接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库确认入库详情")
    def bns_warehouseOrderInStock_detail(self, fstockId):
        self.headers["use-node-method"] = "jsonRequest"
        url = "{}/new/warehouse/warehouseOrderInStock/queryPONoticeDetail?finStockId={}".format(get_b2b_host, fstockId)
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url=url,
            headers=self.headers)
        self.log.log_info("仓库确认入库详情返回信息:{}".format(response.json()))
        return response.json()
        pass

    @allure_attach("仓库确认入库")
    def bns_warehouseOrderInStock_save(self):
        response = self.bns_warehouseOrderInStock_detail(fstockId=self.fstockId)
        finStockSkuId_1 = JsonHelper.parseJson_by_objectpath(response,"$.data..finStockSkuId")[0]
        finStockSkuId_2 = JsonHelper.parseJson_by_objectpath(response,"$.data..finStockSkuId")[1]
        finStockSkuId_3 = JsonHelper.parseJson_by_objectpath(response,"$.data..finStockSkuId")[2]
        data_test = {
            "finStockId": self.fstockId,
            "finStockOrderNum": self.fnoticeOrderNum,
            "finStockStatus": 5,
            "finStockNum": random_str(),
            "finStockRemark": "这是确认出库备注。。。",
            "frelationOrderNum": self.order,
            "fwarehouseId": "76",
            "warehouseOrderInStockSkuVoList": [
                {"fskuStatus": 0, "factualReceiveNum": 1, "fbatchCode": "11", "fremark": "1111",
                 "fskuId": "118905006", "gid": "id_816", "factualExpirattionDate": "2020-06-30", "showAdd": True,
                 "fboxesNum": "1", "fbrandName": "虎牌", "fbusinessType": 1, "fcategoryName": "母婴用品",
                 "fexpirationDate": 1095, "finStockSkuId": finStockSkuId_1, "fshouldReceiveNum": "110",
                 "fskuInternationalNo": "4904710424933", "fskuName": "TIGER虎牌 儿童保温杯MBR-T06G 吸管杯国际版 老虎 600ml",
                 "fskuSpecification": "600ml", "ftrayNum": 1, "fwarehouseId": "76"},
                {"fskuStatus": 0, "factualReceiveNum": 1, "fbatchCode": "11", "fremark": "2222",
                 "fskuId": "GMH00831-J", "gid": "id_8132", "factualExpirattionDate": "2020-06-30", "showAdd": True,
                 "fboxesNum": "1", "fbrandName": "SNP", "fbusinessType": 1, "fcategoryName": "美妆个护",
                 "fexpirationDate": 1093, "finStockSkuId": finStockSkuId_2, "fshouldReceiveNum": "110",
                 "fskuInternationalNo": "8809237828652", "fskuName": "SNP 韩国 老虎动物面膜保湿抗皱 25ml*10片",
                 "fskuSpecification": "老虎动物面膜 25ml*10片", "ftrayNum": 1, "fwarehouseId": "76"},
                {"fskuStatus": 0, "factualReceiveNum": 1, "fbatchCode": "11", "fremark": "3333", "fskuId": "HJH05363-J",
                 "gid": "id_9657", "factualExpirattionDate": "2020-06-30", "showAdd": True, "fboxesNum": "1",
                 "fbrandName": "ecolifelatex", "fbusinessType": 1, "fcategoryName": "家居生活", "fexpirationDate": 0,
                 "finStockSkuId": finStockSkuId_3, "fshouldReceiveNum": "1", "fskuInternationalNo": "8858991833150",
                 "fskuName": "ecolifelatex 泰国 老虎乳胶枕头-老虎", "fskuSpecification": "老虎乳胶枕头-老虎", "ftrayNum": 1,
                 "fwarehouseId": "76"}],
            "instockAttachmentVoList": [
                {
                    "fattachmentId": "",
                    "ffileName": "账号.txt",
                    "ffileUrl": "M00/00/99/wKgA3l6yMj2ASRy0AAACf-Z7Kz4513.txt"
                }
            ]
        }
        data_dev = {"finStockId": self.fstockId, "finStockOrderNum": self.fnoticeOrderNum, "finStockStatus": 5,
                    "finStockNum": random_str(), "finStockRemark": "", "frelationOrderNum": self.order,
                    "fwarehouseId": "76", "warehouseOrderInStockSkuVoList": [
                {"fskuStatus": 0, "factualReceiveNum": 100, "fbatchCode": "", "fskuId": "118905121", "gid": "id_2813",
                 "factualExpirattionDate": "2020-05-30", "showAdd": True, "fboxesNum": "1", "fbrandName": "火柴猴",
                 "fbusinessType": 1, "fcategoryName": "母婴用品", "fexpirationDate": 9999, "finStockSkuId": "405",
                 "fshouldReceiveNum": "100", "fskuInternationalNo": "0611901211053",
                 "fskuName": "英国Matchstick Monkey火柴猴牙胶宝宝婴儿咬咬安抚磨牙棒软硅胶—红色 个", "fskuSpecification": "个", "ftrayNum": "1",
                 "fwarehouseId": "76"},
                {"fskuStatus": 0, "factualReceiveNum": 100, "fbatchCode": "", "fskuId": "DL157941907294202",
                 "gid": "id_5872", "factualExpirattionDate": get_current_time(day=30), "showAdd": True,
                 "fboxesNum": "1",
                 "fbrandName": "SWAROVSKI 施华洛世奇", "fbusinessType": 1, "fcategoryName": "服饰鞋包", "fexpirationDate": 500,
                 "finStockSkuId": "406", "fshouldReceiveNum": "100", "fskuInternationalNo": "121221",
                 "fskuName": "潘多拉项链 彩金", "fskuSpecification": "彩金", "ftrayNum": "1", "fwarehouseId": "76"},
                {"fskuStatus": 0, "factualReceiveNum": 100, "fbatchCode": "", "fskuId": "GMH02965-J", "gid": "id_2250",
                 "factualExpirattionDate": get_current_time(day=30), "showAdd": True, "fboxesNum": "1",
                 "fbrandName": "悦木之源",
                 "fbusinessType": 1, "fcategoryName": "美妆个护", "fexpirationDate": 1095, "finStockSkuId": "407",
                 "fshouldReceiveNum": "100", "fskuInternationalNo": "717334229594",
                 "fskuName": "悦木之源 蘑菇水200ml 菌菇水 200ml", "fskuSpecification": "菌菇水 200ml", "ftrayNum": "1",
                 "fwarehouseId": "76"}], "instockAttachmentVoList": [{"fattachmentId": "", "ffileName": "账号.txt",
                                                                      "ffileUrl": "M00/00/9A/wKgA3l6zucqAHXHLAAACf-Z7Kz4084.txt"}]}
        if str(get_b2b_host) == "http://192.168.1.227:3003":
            data = data_dev
        else:
            data = data_test
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderInStock/saveOrUpdatePONotice".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库确认入库接口请求信息:{}".format(data))
        self.log.log_info("仓库确认入库接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库其他入库")
    def bns_warehouseOrderInStock_otherin(self):
        data = {
            "frejectReason": "",
            "finStockOrderNum": "",
            "finStockStatus": 3,
            "frelationOrderNum": "",
            "finStockNum": "",
            "fotherInStockType": 1,
            "fbusinessType": 2,
            "fbusinessName": "BB以销定采4",
            "fsubjectId": 102,
            "fremark": "",
            "fcompanyId": None,
            "fcompanyName": "",
            "otherWarehouseSkuList": [
                {
                    "fskuSpecification": "个",
                    "fexpirationDate": 9999,
                    "fskuId": "118905121",
                    "fskuName": "英国Matchstick Monkey火柴猴牙胶宝宝婴儿咬咬安抚磨牙棒软硅胶—红色 个",
                    "fskuInternationalNo": "0611901211053",
                    "fcategoryId": 1,
                    "fcategoryId2": None,
                    "fcategoryId3": None,
                    "fcategoryName": "母婴用品",
                    "fcategoryName2": None,
                    "fcategoryName3": None,
                    "unit": "红色",
                    "fbrandId": 1462,
                    "fbrandName": "火柴猴",
                    "fbrandNameEng": "Matchstick Monkey",
                    "fbrandLabelName": "非品牌",
                    "fbrandLabelCode": 1,
                    "foriginId": 8,
                    "value": "英国Matchstick Monkey火柴猴牙胶宝宝婴儿咬咬安抚磨牙棒软硅胶—红色 个",
                    "State3": 0,
                    "fboxesNum": 1,
                    "ftrayNum": 1,
                    "fskuStatus": 1,
                    "factualReceiveNum": 11,
                    "factualExpirattionDate": "2020-05-31",
                    "fbatchCode": "1111",
                    "fwarehouseId": 76
                },
                {
                    "fskuSpecification": "盒",
                    "fexpirationDate": 1,
                    "fskuId": "122305132",
                    "fskuName": "Technic特技赛车42095 盒",
                    "fskuInternationalNo": "585012286979",
                    "fcategoryId": 1,
                    "fcategoryId2": None,
                    "fcategoryId3": None,
                    "fcategoryName": "母婴用品",
                    "fcategoryName2": None,
                    "fcategoryName3": None,
                    "unit": "盒",
                    "fbrandId": 634,
                    "fbrandName": "LEGO乐高",
                    "fbrandNameEng": "",
                    "fbrandLabelName": "非品牌",
                    "fbrandLabelCode": 1,
                    "foriginId": 9,
                    "value": "Technic特技赛车42095 盒",
                    "State3": 0,
                    "fboxesNum": 11,
                    "ftrayNum": 1,
                    "fskuStatus": 0,
                    "factualReceiveNum": 11,
                    "factualExpirattionDate": "2020-05-27",
                    "fbatchCode": "1121",
                    "fwarehouseId": 76
                },
                {
                    "fskuSpecification": "600ml",
                    "fexpirationDate": 1095,
                    "fskuId": "118905006",
                    "fskuName": "TIGER虎牌 儿童保温杯MBR-T06G 吸管杯国际版 老虎 600ml",
                    "fskuInternationalNo": "4904710424933",
                    "fcategoryId": 1,
                    "fcategoryId2": None,
                    "fcategoryId3": None,
                    "fcategoryName": "母婴用品",
                    "fcategoryName2": None,
                    "fcategoryName3": None,
                    "unit": "个",
                    "fbrandId": 1450,
                    "fbrandName": "虎牌",
                    "fbrandNameEng": "TIGER",
                    "fbrandLabelName": "自有品牌",
                    "fbrandLabelCode": 2,
                    "foriginId": 14,
                    "value": "TIGER虎牌 儿童保温杯MBR-T06G 吸管杯国际版 老虎 600ml",
                    "State3": 0,
                    "fboxesNum": 111,
                    "ftrayNum": 1,
                    "fskuStatus": 2,
                    "factualReceiveNum": 11,
                    "factualExpirattionDate": "2020-05-24",
                    "fbatchCode": "1212",
                    "fwarehouseId": 76
                }
            ],
            "fwarehouseId": 76,
            "otherAttachmentList": [
                {
                    "fdataType": 0,
                    "fattachmentType": 0,
                    "fattachmentName": "账号.txt",
                    "fattachmentUrl": "M00/01/28/wKgA317N3eWAGk30AAACyuMWYDo163.txt",
                    "name": "账号.txt",
                    "url": "M00/01/28/wKgA317N3eWAGk30AAACyuMWYDo163.txt",
                    "fattachmentSize": "714KB",
                    "uid": 1590550033969,
                    "status": "success",
                    "ffileName": "账号.txt",
                    "ffileUrl": "M00/01/28/wKgA317N3eWAGk30AAACyuMWYDo163.txt"
                }
            ]
        }
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderInStock/saveOtherWarehouse".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库其他入库接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库其他出库")
    def bns_warehouseOrderInStock_otherout(self):
        data = {
            "Fdate": "",
            "freceiveAddress": "",
            "fvalidUntilDate": "",
            "freceiveTelephone": "11",
            "fstockState": "",
            "skuInfo": "",
            "finStockNum": "",
            "fremark": "",
            "frelationOrderNum": "",
            "frejectReason": "",
            "foutStockStatus": 3,
            "foutStockOrderNum": "",
            "fsubjectId": 102,
            "fbusinessType": 1,
            "fbusinessName": "BB自营分销1",
            "fotherOutStockType": 3,
            "fdestination": "11",
            "skuVoList": [
                {
                    "fbatchCode": "57996545",
                    "fbatchCost": "10000000",
                    "fbatchCostUnit": "1000000",
                    "fbatchNo": "05689、122305136、2020-04-21",
                    "fbatchStocckNum": "181",
                    "fbrand": "LEGO乐高",
                    "fcategory": "母婴用品",
                    "finStockNum": "05689",
                    "finternationalCode": "571435421357",
                    "fskuId": "122305136",
                    "fskuName": "Harry potter霍格沃茨城堡75954 盒",
                    "fskuSpecifications": "盒",
                    "fstockState": 0,
                    "fvalidUntilDate": "2020-04-21",
                    "fwarehouseId": 76,
                    "fskuStatus": 0,
                    "frealNum": "1",
                    "feffectiveTime": "2020-04-21"
                },
                {
                    "fbatchCode": "57996545",
                    "fbatchCost": "10000000",
                    "fbatchCostUnit": "1000000",
                    "fbatchNo": "05689、FSP05092-J、2021-04-23",
                    "fbatchStocckNum": "62",
                    "fbrand": "SWAROVSKI 施华洛世奇",
                    "fcategory": "服饰鞋包",
                    "finStockNum": "05689",
                    "finternationalCode": "9009654463903",
                    "fskuId": "FSP05092-J",
                    "fskuName": "Swarovski 奥地利施华洛世奇 迪士尼米奇可爱浪漫 耳饰 5446390",
                    "fskuSpecifications": " 迪士尼米奇可爱浪漫 耳饰 5446390",
                    "fstockState": 0,
                    "fvalidUntilDate": "2021-04-23",
                    "fwarehouseId": 76,
                    "fskuStatus": 0,
                    "frealNum": "1",
                    "feffectiveTime": "2021-04-23"
                }
            ],
            "fskuStatus": None,
            "addOrUpdate": True,
            "fwarehouseId": 76,
            "attachmentDtoList": [],
            "skuEditDtoList": [
                {
                    "fbatchCode": "57996545",
                    "fbatchCost": "10000000",
                    "fbatchCostUnit": "1000000",
                    "fbatchNo": "05689、122305136、2020-04-21",
                    "fbatchStocckNum": "181",
                    "fbrand": "LEGO乐高",
                    "fcategory": "母婴用品",
                    "finStockNum": "05689",
                    "finternationalCode": "571435421357",
                    "fskuId": "122305136",
                    "fskuName": "Harry potter霍格沃茨城堡75954 盒",
                    "fskuSpecifications": "盒",
                    "fstockState": 0,
                    "fvalidUntilDate": "2020-04-21",
                    "fwarehouseId": 76,
                    "fskuStatus": 0,
                    "frealNum": "1",
                    "feffectiveTime": "2020-04-21"
                },
                {
                    "fbatchCode": "57996545",
                    "fbatchCost": "10000000",
                    "fbatchCostUnit": "1000000",
                    "fbatchNo": "05689、FSP05092-J、2021-04-23",
                    "fbatchStocckNum": "62",
                    "fbrand": "SWAROVSKI 施华洛世奇",
                    "fcategory": "服饰鞋包",
                    "finStockNum": "05689",
                    "finternationalCode": "9009654463903",
                    "fskuId": "FSP05092-J",
                    "fskuName": "Swarovski 奥地利施华洛世奇 迪士尼米奇可爱浪漫 耳饰 5446390",
                    "fskuSpecifications": " 迪士尼米奇可爱浪漫 耳饰 5446390",
                    "fstockState": 0,
                    "fvalidUntilDate": "2021-04-23",
                    "fwarehouseId": 76,
                    "fskuStatus": 0,
                    "frealNum": "1",
                    "feffectiveTime": "2021-04-23"
                }
            ]
        }
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderOutStock/saveOrUpdateOtherOut".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库其他出库接口返回信息:{}".format(response.json()))
        return response.json()

    # 仓库so
    @allure_attach("仓库接受确认")
    def bns_so_sale_warehouseOrderOutStock(self, ):
        response = so_admin.bns_so_sale_saleDeliveryApplyList()
        self.foutStockId = JsonHelper.parseJson_by_objectpath(response, "$..foutStockId")[0]
        url = "/new/warehouse/warehouseOrderOutStock/modifyOutboundStatus?foutStockId={}&foutStockStatus=4&frejectReason=".format(
            self.foutStockId)
        self.headers["use-node-method"] = "commonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url=str(get_b2b_host) + url,
            headers=self.headers
        )
        self.log.log_info("仓库接受确认接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库采购入库单查询")
    def bns_warehouseOrderInStock_polist(self, warehouseId=None):
        if warehouseId is None: warehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            warehouseId = "137"
        data = \
            {"currentPage": 1, "pageSize": 10, "time": [], "fbusinessType": "", "finStockOrderNum": "",
             "fsubjectName": "", "fcompanyName": "", "fskuId": "", "fskuName": "", "queryType": 1,
             "finStockTimeStart": "", "finStockTimeEnd": "", "fwarehouseId": warehouseId}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderInStock/queryPOInStockList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库采购订单列表接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库确认出库")
    def bns_so_sale_confirmDelivery(self, ):
        data = {
            "foutStockStatus": 5,
            "foutStockId": self.foutStockId,
            "fwareHouseId": "76",
            "fsubjectId": 102,
            "outStockDtos": [
                {
                    "foutStockId": self.foutStockId,
                    "frealNum": 10,
                    "fskuId": "118905006",
                    "fshouldNum": "10",
                    "fstockState": 0,
                    "fstockId": "1076",
                    "fremark": ""
                }
            ]
        }
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderOutStock/confirmDelivery".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库确认出库接口返回信息:{}".format(response.json()))
        return response.json()

    # 仓库入库单据
    @allure_attach("仓库采购入库单查询")
    def bns_warehouseOrderInStock_polist(self, warehouseId=None):
        if warehouseId is None: warehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            warehouseId = "137"
        data = \
            {"currentPage": 1, "pageSize": 10, "time": [], "fbusinessType": "", "finStockOrderNum": "",
             "fsubjectName": "", "fcompanyName": "", "fskuId": "", "fskuName": "", "queryType": 1,
             "finStockTimeStart": "", "finStockTimeEnd": "", "fwarehouseId": warehouseId}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderInStock/queryPOInStockList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库采购订单列表接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库销售退货单查询")
    def bns_warehouseOrderInStock_soreback(self, warehouseId=None):
        if warehouseId is None: warehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            warehouseId = "137"
        data = \
            {"currentPage": 1, "pageSize": 10, "time": [], "fbusinessType": "", "finStockOrderNum": "",
             "fsubjectName": "", "fcompanyName": "", "fskuId": "", "fskuName": "", "queryType": 1,
             "finStockTimeStart": "", "finStockTimeEnd": "", "fwarehouseId": warehouseId}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderInStock/querySROInStockList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库采购订单列表接口返回信息:{}".format(response.json()))
        return response.json()

        pass

    @allure_attach("仓库调拨入库单查询")
    def bns_warehouseOrderInStock_in_list(self, warehouseId=None):
        if warehouseId is None: warehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            warehouseId = "137"
        data = \
            {"currentPage": 1, "pageSize": 10, "fwarehouseId": warehouseId}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/allotOrderInStock/queryInStockListByBills".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库调拨入库订单列表接口返回信息:{}".format(response.json()))
        return response.json()

        pass

    @allure_attach("仓库其他入库单查询")
    def bns_warehouseOrderInStock_other_in_list(self, warehouseId=None):
        if warehouseId is None: warehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            warehouseId = "137"
        data = \
            {"currentPage": 1, "pageSize": 10, "fwarehouseId": warehouseId, "creatTime": [],
             "queryType": 1}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderInStock/queryOtherWarehouseList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库其他入库订单列表接口返回信息:{}".format(response.json()))
        return response.json()
        pass

    # 仓库出库单据
    @allure_attach("仓库销售出库单")
    def bns_so_sale_warehouse_solist(self, fwarehouseId=None):
        if fwarehouseId is None: fwarehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            fwarehouseId = "137"
        data = {
            "currentPage": 1,
            "pageSize": 10,
            "time": [],
            "fbusinessType": "",
            "foutStockOrderNum": "",
            "fsaleOrderNum": "",
            "fcompanyName": "",
            "fskuId": "",
            "fskuName": "",
            "foutStockTimeBegin": "",
            "foutStockTimeEnd": "",
            "foutStockType": 1,
            "showType": "bill",
            "fwarehouseId": fwarehouseId
        }
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderOutStock/selectWarehouseOrderOutStcokList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库销售出库单接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库采购退货单查询")
    def bns_warehouseOrderInStock_po_back_list(self, warehouseId=None):
        if warehouseId is None: warehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            warehouseId = "137"
        data = \
            {"currentPage": 1, "pageSize": 10, "time": [], "fbusinessType": "", "foutStockOrderNum": "",
             "fpurchaseOrderCode": "", "fcompanyName": "", "freturnReason": "", "fskuName": "", "fskuId": "",
             "foutStockTimeBegin": "", "foutStockTimeEnd": "", "foutStockType": 2, "showType": "bill",
             "fwarehouseId": 76}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderOutStock/selectReturnPurchaseStockList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库采购退货订单列表接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库调拨出库单查询")
    def bns_warehouseOrderInStock_out_list(self, warehouseId=None):
        if warehouseId is None: warehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            warehouseId = "137"
        data = \
            {"currentPage": 1, "pageSize": 10, "fwarehouseId": warehouseId, "creatTime": [],
             "searchType": 1}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/allocate/outStock/bills/list".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库调拨出库订单列表接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("仓库其他出库单查询")
    def bns_warehouseOrderInStock_other_out_list(self, warehouseId=None):
        if warehouseId is None: warehouseId = "76"
        if get_b2b_host == "http://192.168.0.53:3003":
            warehouseId = "137"
        data = \
            {"queryType": 1, "foutStockOrderNum": "", "fotherOutStockType": None, "finventoryId": "", "createTime": "",
             "fskuId": "", "fskuName": "", "currentPage": 1, "pageSize": 10, "fwarehouseId": 76}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderOutStock/queryOtherOutList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("仓库其他出库订单列表接口返回信息:{}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    a = BnsApi()
    a.bns_po_stock_add()
    a.bns_warehouseOrderInStock_saveOrUpdatePONotice()
    a.bns_warehouseOrderInStock_save()
