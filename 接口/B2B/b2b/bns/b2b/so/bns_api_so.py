from base.decorators import allure_attach
from base.helper import JsonHelper
from testdata.gen_bnsData import *
from bns.b2b import BusinessApi
from config import *
import json


class BnsApi_So(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @allure_attach("新建销售订单")
    def bns_new_so_add(self, ):
        if str(get_b2b_host) == "http://192.168.0.53:3003":
            fcompanyId = "825"
        else:
            fcompanyId = "531"
        data = {
            "createSaleOrderQoBasicInfoComponent": {
                "fquotationMethod": "FCA",
                "fplanType": "1",
                "fsaleAid": "249",
                "fsaleContact": "17688546806",
                "fxycompanyId": "102",
                "fagreementId": "TXY-SL-HH/191226-09",
                "fcompanyId": fcompanyId,
                "ftradeType": "2",
                "faccountChargeName": "11",
                "saleMode": "2",
                "faccountChargeContact": "11",
                "foriginPlace": "11",
                "fqualityGuaranteePeriod": "11",
                "orderCategory": "1",
                "saleOrderTag": "0"
            },
            "saleOrderQoFinanceComponent": {
                "fpreGatherAmount": "0",
                "fpreGatherAmountRatio": "100",
                "fsaleTotalAmountIncludeTaxOriginalCurrency": 3916,
                "fsettlementFrequency": "1",
                "fitemReceivedInAdvance": "0",
                "fpreGatherConditionStr": "11",
                "fsettlementCurrencyType": "USD",
                "fpreGatherDate": "2020-05-14",
                "fpreGatherCondition": -1,
                "fmidtermGatherCondition": -1,
                "frestGatherCondition": -1
            },
            "saleOrderQoDeliveryTermComponent": {
                "ftransportType": "2",
                "fdeliveryAddress": "11",
                "fdeliveryDate": get_current_time(),
                "tallyReportReceivedDate": get_current_time()
            },
            "contract": {
                "finvoiceType": 1,
                "fmoneyWay": 0
            },
            "saleOrderSkuQoComponentList": [
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
                    "brandTagDesc": "非品牌",
                    "fsaleNum": 11,
                    "ftaxRateId": 40,
                    "fpriceIncludingTaxOriginalCurrency": 111,
                    "ftaxRate": 0.02,
                    "fpriceIncludingTaxFunctionalCurrency": 783.34,
                    "frealPriceOriginalCurrency": 108.823636,
                    "frealPriceFunctionalCurrency": 767.979282,
                    "fsaleTotalAmountWithoutTaxOriginalCurrency": 1197.06,
                    "fsaleTotalAmountWithoutTaxFunctionalCurrency": 8447.77,
                    "ftaxAmountOriginalCurrency": 23.94,
                    "ftaxAmountFunctionalCurrency": 168.95,
                    "fsaleTotalAmountIncludeTaxOriginalCurrency": 1221,
                    "fsaleTotalAmountIncludeTaxFunctionalCurrency": 8616.72
                },
                {
                    "fskuSpecification": "白色 135/64",
                    "fexpirationDate": 0,
                    "fskuId": "FBF02443-Y",
                    "fskuName": "Sergent Major 思佳美儿女童T恤17E2PF45TCT 白色 135/64",
                    "fskuInternationalNo": "6931947072338",
                    "fcategoryId": 1,
                    "fcategoryId2": None,
                    "fcategoryId3": None,
                    "fcategoryName": "母婴用品",
                    "fcategoryName2": None,
                    "fcategoryName3": None,
                    "unit": "Sergent Major 思佳美儿",
                    "fbrandId": 592,
                    "fbrandName": "sergentmajor思佳美儿",
                    "fbrandNameEng": "",
                    "fbrandLabelName": "非品牌",
                    "fbrandLabelCode": 1,
                    "foriginId": 45,
                    "brandTagDesc": "非品牌",
                    "fsaleNum": 22,
                    "ftaxRateId": 52,
                    "fpriceIncludingTaxOriginalCurrency": 121,
                    "ftaxRate": 0.5,
                    "fpriceIncludingTaxFunctionalCurrency": 853.91,
                    "frealPriceOriginalCurrency": 80.666818,
                    "frealPriceFunctionalCurrency": 569.273801,
                    "fsaleTotalAmountWithoutTaxOriginalCurrency": 1774.67,
                    "fsaleTotalAmountWithoutTaxFunctionalCurrency": 12524.02,
                    "ftaxAmountOriginalCurrency": 887.33,
                    "ftaxAmountFunctionalCurrency": 6261.98,
                    "fsaleTotalAmountIncludeTaxOriginalCurrency": 2662,
                    "fsaleTotalAmountIncludeTaxFunctionalCurrency": 18786
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
                    "brandTagDesc": "自有品牌",
                    "fsaleNum": 333,
                    "ftaxRateId": 38,
                    "fpriceIncludingTaxOriginalCurrency": 0.55,
                    "ftaxRate": 0.01,
                    "fpriceIncludingTaxFunctionalCurrency": 3.88,
                    "frealPriceOriginalCurrency": 0.544565,
                    "frealPriceFunctionalCurrency": 3.84305,
                    "fsaleTotalAmountWithoutTaxOriginalCurrency": 181.34,
                    "fsaleTotalAmountWithoutTaxFunctionalCurrency": 1279.73,
                    "ftaxAmountOriginalCurrency": 1.81,
                    "ftaxAmountFunctionalCurrency": 12.77,
                    "fsaleTotalAmountIncludeTaxOriginalCurrency": 183.15,
                    "fsaleTotalAmountIncludeTaxFunctionalCurrency": 1292.51
                }
            ],
            "saleOrderQoAttachmentComponentList": [
                {
                    "fattachmentName": "账号.txt",
                    "fattachmentUrl": "M00/00/9A/wKgA3l66ebGACKfpAAACyuMWYDo668.txt",
                    "fattachmentSize": 714,
                    "fattachmentType": 0,
                    "fdataType": 0,
                    "fpurchaseBillId": None
                }
            ],
            "check": False}

        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sale/createNewSaleOrderAction".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )

        # self.log.log_info("新建销售订单接口请求信息:{}".format(data))
        self.log.log_info("新建销售订单接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("销售订单列表")
    def bns_so_list(self, ):
        data = {
            "pageSize": 10,
            "pageIndex": 1
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sale/viewSaleOrderList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )

        # self.log.log_info("销售订单列表接口请求信息:{}".format(data))
        self.log.log_info("销售订单列表接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("销售订单详情")
    def bns_so_detail(self, fsaleOrderId=None):
        data = {
            "fsaleOrderId": fsaleOrderId
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sale/viewSaleOrder".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )

        # self.log.log_info("销售订单列表接口请求信息:{}".format(data))
        self.log.log_info("销售订单列详情接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("提交审批销售订单")
    def bns_so_submitSaleOrder(self, ):
        self.order = JsonHelper.parseJson_by_objectpath(self.bns_so_list(), "$.retEntity..fsaleOrderId")[0]

        data = {
            "fsaleOrderId": self.order
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sale/submitSaleOrder".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # self.log.log_info("提交审批销售订单接口请求信息:{}".format(data))
        self.log.log_info("提交审批销售订单接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("OA模拟审批通过")
    def bns_so_saleOrderApprove(self, ):
        data = {
            "fsaleOrderId": self.order,
            "status": 3
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sale/saleOrderApprove".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # self.log.log_info("OA模拟审批通过接口请求信息:{}".format(data))
        self.log.log_info("OA模拟审批通过接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("销售订单申请发货")
    def bns_so_sale_deliverSubmit(self, ):
        data = {
            "basic": {
                "fagreementId": "TXY-SL-HH/191226-09",
                "fbusinessType": 1,
                "fcompanyId": 531,
                "fcompanyName": "哈哈供应商2",
                "flogisticsType": 2,
                "freceiveAddress": "深圳",
                "freceiveContact": "jordan",
                "freceiveTelephone": "13714956215",
                "frelationOrderNum": self.order,
                "fremark": None,
                "ftargetDeliveryDate": get_current_time(),
                "fwarehouseId": 76
            },
            "skuList": [
                {
                    "fshouldNum": 10,
                    "fskuId": "118905006",
                    "fwarehouseId": 76
                }
            ],
            "attachmentList": [
                {
                    "ffileName": "账号.txt",
                    "ffileUrl": "M00/00/99/wKgA3l6yf5yAZLSiAAACf-Z7Kz4065.txt"
                }
            ]
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sale/deliverSubmit".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("申请发货接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("销售出库订单查询")
    def bns_so_sale_saleDeliveryApplyList(self, ):
        data = {
            "fcreateTimeEnd": "",
            "fcreateTimeStart": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sale/saleDeliveryApplyList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("销售出库订单查询接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("销售退货列表")
    def bns_so_sale_returnList(self, ):
        data = {
            "fcreateTimeEnd": "",
            "fcreateTimeStart": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sale/returnList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("销售出库订单查询接口返回信息:{}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    a = BnsApi_So()
    # a.bns_new_so_add()
    # a.bns_so_submitSaleOrder()
    # a.bns_so_saleOrderApprove()
    # a.bns_so_sale_deliverSubmit()
    # a.bns_so_sale_warehouseOrderOutStock()
    # a.bns_so_sale_confirmDelivery()
    a.bns_so_sale_returnList()
