#!/usr/bin/python3.7
# @Time : 2020/5/27 0027 15:44 
# -*- coding: utf-8 -*-
# @Time : 2020-05-27 15:38:50
from base.decorators import allure_attach
from bns.b2b import BusinessApi
from testdata import get_current_time


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

        self._config_po = self.base_yaml_info(
            curr_file=__file__,
            module_key="po"
        )

    @allure_attach("新建采购订单")
    def bns_po_add(self, headers=None, ):
        # TODO: 请完成函数注释!!!

        api_info = self._config_po["add"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            "xyPurchaseOrderDO": {
                "fplanType": 1,
                "forderLabels": 1,
                "forderCategory": 1,
                "ftradeType": 1,
                "fquotationMethod": "CPT",
                "fsupplierId": 531,
                "fsupplierName": "哈哈供应商2",
                "fcorporateSubjectId": 102,
                "fourCompanyName": "深圳市天行云供应链有限公司",
                "fsupplierLeader": "图图",
                "fsupplierLeaderPhone": "13026161548",
                "fagreementId": 220,
                "fagreementNum": "TXY-PC-HHGYS/191224-001",
                "fagreementType": 1,
                "finvoiceType": 1,
                "fmoneyWay": 1,
                "fpaymentComment": "三个结算啊大大说",
                "fpurchaseInvoiceType": 1,
                "fsourceArea": "深圳",
                "fshelfLife": "30",
                "fpurchaseAid": 249,
                "fourCompanyLeader": "蔡惠子",
                "fpurchaseDeptName": "测试开发团队",
                "fourCompanyLeaderPhone": "17688546806",
                "fpurchaseOrderStatus": 1
            },
            "xyPurchaseOrderFinanceDO": {
                "advanceProportion": 100,
                "advancePayment": 1430,
                "advanceProportionPayment": "100.00% 1430.00",
                "metaphaseProportion": 0,
                "metaphasePayment": 0,
                "metaphaseProportionPayment": "",
                "finalProportion": 0,
                "finalPayment": 0,
                "finalProportionPayment": "",
                "totalAmountOfTaxOriginalCurrency": 1430.5,
                "notTotalAmountOfTaxOriginalCurrency": 1417.26,
                "amountOfTaxOriginalCurrency": 13.24,
                "totalAmountOfTaxBaseCurrency": 10095.18,
                "notTotalAmountOfTaxBaseCurrency": 10001.75,
                "amountOfTaxBaseCurrency": 93.44,
                "estimatePurchaseCost": 0,
                "estimatePurchaseCostOfBase": 0,
                "ffinanceId": None,
                "fcurrencyCode": "USD",
                "payMoneyPlanBoList": None,
                "fexchangeRate": None,
                "fexchangeRateView": 7.0571,
                "fpurchaseInvoiceType": 1,
                "fwhetherAdvancePayment": 1,
                "fnumberOfSettlement": 1,
                "fmoneyWay": 1,
                "fadvancePayment": 14305000,
                "fadvanceProportion": 10000,
                "fadvancePaymentClause": 0,
                "fadvancePaymentClauseStr": None,
                "ftheFirstPayment": 14305000,
                "ftheFirstProportion": 10000,
                "ftheFirstPaymentClause": 0,
                "ftheFirstPaymentClauseStr": "11",
                "fmetaphasePayment": None,
                "fmetaphaseProportion": None,
                "fmetaphasePaymentClause": 0,
                "fmetaphasePaymentClauseStr": None,
                "ffinalPayment": None,
                "ffinalProportion": None,
                "ffinalPaymentClause": 0,
                "ffinalPaymentClauseStr": None,
                "fadvanceEstimatedTimeOfPayment": get_current_time(),
                "ftheFirstEstimatedTimeOfPayment": get_current_time(),
                "fmetaphaseEstimatedTimeOfPayment": None,
                "ffinalEstimatedTimeOfPayment": None,
                "festimatePurchaseCost": 0,
                "fotherPayment": 0
            },
            "xyPurchaseOrderDeliveryDO": {
                "ftransportType": 2,
                "fdeliveryAddress": "湖北",
                "fdeliveryDate": get_current_time(day=1),
                "festimatedDeliveryDate": get_current_time(day=1)
            },
            "xyPurchaseOrderSkuVOList": [
                {
                    "fpurchaseOrderSkuId": None,
                    "fpurchaseOrderId": None,
                    "fskuId": "118905006",
                    "fbrandLabel": None,
                    "fpurchaseAmount": 110,
                    "ftaxRate": 10,
                    "ftaxIncluded": 12000000,
                    "ftaxIncludedUnit": None,
                    "fwarehousingCost": 11881182,
                    "fwarehousingCostUnit": 1000000,
                    "taxIncluded": 12,
                    "warehousingCost": 11.881182,
                    "shareCost": None,
                    "totalAmountOfTaxOriginalCurrency": 1320,
                    "notTotalAmountOfTaxOriginalCurrency": 1306.93,
                    "amountOfTaxOriginalCurrency": 13.07,
                    "taxIncludedBaseCurrency": 84.69,
                    "warehousingCostBaseCurrency": 83.85,
                    "totalAmountOfTaxBaseCurrency": 9315.37,
                    "notTotalAmountOfTaxBaseCurrency": 9223.13,
                    "amountOfTaxBaseCurrency": 92.24,
                    "fskuName": "TIGER虎牌 儿童保温杯MBR-T06G 吸管杯国际版 老虎 600ml",
                    "fcategoryName": "母婴用品",
                    "fbrandName": "虎牌",
                    "fbrandLabelName": "非品牌",
                    "fbrandNameEng": "TIGER",
                    "funit": None,
                    "fskuInternationalNo": "4904710424933",
                    "fpurchaseOrderSkuChangeId": None,
                    "fdataType": None,
                    "foriginId": 14,
                    "ftaxRateString": "1%",
                    "edit": False
                },
                {
                    "fpurchaseOrderSkuId": None,
                    "fpurchaseOrderId": None,
                    "fskuId": "GMH00831-J",
                    "fbrandLabel": None,
                    "fpurchaseAmount": 110,
                    "ftaxRate": 0,
                    "ftaxIncluded": 1000000,
                    "ftaxIncludedUnit": None,
                    "fwarehousingCost": 1000000,
                    "fwarehousingCostUnit": 1000000,
                    "taxIncluded": 1,
                    "warehousingCost": 1,
                    "shareCost": None,
                    "totalAmountOfTaxOriginalCurrency": 110,
                    "notTotalAmountOfTaxOriginalCurrency": 110,
                    "amountOfTaxOriginalCurrency": 0,
                    "taxIncludedBaseCurrency": 7.06,
                    "warehousingCostBaseCurrency": 7.06,
                    "totalAmountOfTaxBaseCurrency": 776.28,
                    "notTotalAmountOfTaxBaseCurrency": 776.28,
                    "amountOfTaxBaseCurrency": 0,
                    "fskuName": "SNP 韩国 老虎动物面膜保湿抗皱 25ml*10片",
                    "fcategoryName": "美妆个护",
                    "fbrandName": "SNP",
                    "fbrandLabelName": "非品牌",
                    "fbrandNameEng": "",
                    "funit": None,
                    "fskuInternationalNo": "8809237828652",
                    "fpurchaseOrderSkuChangeId": None,
                    "fdataType": None,
                    "foriginId": 21,
                    "ftaxRateString": "0%",
                    "edit": False
                },
                {
                    "fpurchaseOrderSkuId": None,
                    "fpurchaseOrderId": None,
                    "fskuId": "HJH05363-J",
                    "fbrandLabel": None,
                    "fpurchaseAmount": 1,
                    "ftaxRate": 500,
                    "ftaxIncluded": 500000,
                    "ftaxIncludedUnit": None,
                    "fwarehousingCost": 330000,
                    "fwarehousingCostUnit": 1000000,
                    "taxIncluded": 0.5,
                    "warehousingCost": 0.33,
                    "shareCost": None,
                    "totalAmountOfTaxOriginalCurrency": 0.5,
                    "notTotalAmountOfTaxOriginalCurrency": 0.33,
                    "amountOfTaxOriginalCurrency": 0.17,
                    "taxIncludedBaseCurrency": 3.53,
                    "warehousingCostBaseCurrency": 2.33,
                    "totalAmountOfTaxBaseCurrency": 3.53,
                    "notTotalAmountOfTaxBaseCurrency": 2.33,
                    "amountOfTaxBaseCurrency": 1.2,
                    "fskuName": "ecolifelatex 泰国 老虎乳胶枕头-老虎",
                    "fcategoryName": "家居生活",
                    "fbrandName": "ecolifelatex",
                    "fbrandLabelName": "非品牌",
                    "fbrandNameEng": "",
                    "funit": None,
                    "fskuInternationalNo": "8858991833150",
                    "fpurchaseOrderSkuChangeId": None,
                    "fdataType": None,
                    "foriginId": 12,
                    "ftaxRateString": "50%"
                }
            ],
            "xyPurchaseOrderContractDO": {
                "fagreementId": 220,
                "fagreementNum": "TXY-PC-HHGYS/191224-001",
                "fagreementType": 1,
                "finvoiceType": 1,
                "fmoneyWay": 1,
                "fpaymentComment": "三个结算啊大大说"
            },
            "restsPurchaseOrderAttachmentDOList": [
                {
                    "fattachmentName": "账号.txt",
                    "fattachmentUrl": "M00/00/9A/wKgA3l66ebGACKfpAAACyuMWYDo668.txt",
                    "fattachmentSize": 714,
                    "fattachmentType": 0,
                    "fdataType": 0,
                    "fpurchaseBillId": None
                }
            ],
            "supplierFileDelete": False
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            # TODO: 请确认url是否需要变化！！！
            request_url="{}{}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response


if __name__ == '__main__':
    a = BnsApi()
    a.bns_po_add()
