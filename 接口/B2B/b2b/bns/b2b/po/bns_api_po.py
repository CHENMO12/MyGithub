from base.decorators import allure_attach
from base.helper import JsonHelper
from testdata.gen_bnsData import *
from bns.b2b import BusinessApi
from config import *
import json
import time


# def Three(response, fun):
#     res_msg = JsonHelper.parseJson_by_objectpath(response.json(), "$.msg")
#     for i in range(0, 3):
#         if res_msg == "处理成功":
#             break
#         else:
#             fun()
#             time.sleep(0.2)

class BnsApi_Po(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @allure_attach("新建采购订单")
    def bns_new_po_add(self, ):
        data_test = {
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
        data_dev = {"xyPurchaseOrderDO":
                        {"fplanType": 8, "forderLabels": 1, "ftradeType": 1, "fquotationMethod": "CPT",
                         "fsupplierId": 531, "fsupplierName": "哈哈供应商2", "fcorporateSubjectId": 102,
                         "fourCompanyName": "深圳市天行云供应链有限公司", "fsupplierLeader": "ben",
                         "fsupplierLeaderPhone": "13264645696", "fagreementId": 239,
                         "fagreementNum": "TXY-PC-HHGYS/200311-02", "fagreementType": 0,
                         "finvoiceType": 0, "fmoneyWay": 0, "fpaymentComment": "sfdsdfsddsfdsfdsfdsf",
                         "fpurchaseInvoiceType": 0, "fpurchaseAid": 120, "fourCompanyLeader": "刘丽君",
                         "fpurchaseDeptName": "测试开发团队", "fourCompanyLeaderPhone": "17688546806",
                         "fsourceArea": "湖北", "fshelfLife": "30", "ferpOrderId": "123321456",
                         "fpurchaseOrderStatus": 1},
                    "xyPurchaseOrderFinanceDO": {"advanceProportion": 100, "advancePayment": 300,
                                                 "advanceProportionPayment": "100.00% 300.00", "metaphaseProportion": 0,
                                                 "metaphasePayment": 0, "metaphaseProportionPayment": "",
                                                 "finalProportion": 0, "finalPayment": 0, "finalProportionPayment": "",
                                                 "totalAmountOfTaxOriginalCurrency": 310,
                                                 "notTotalAmountOfTaxOriginalCurrency": 308.72,
                                                 "amountOfTaxOriginalCurrency": 1.28,
                                                 "totalAmountOfTaxBaseCurrency": 310,
                                                 "notTotalAmountOfTaxBaseCurrency": 308.72,
                                                 "amountOfTaxBaseCurrency": 1.28, "estimatePurchaseCost": 0,
                                                 "estimatePurchaseCostOfBase": 0, "ffinanceId": None,
                                                 "fcurrencyCode": "CNY", "payMoneyPlanBoList": None,
                                                 "fexchangeRate": None, "fexchangeRateView": 1,
                                                 "fpurchaseInvoiceType": 0, "fwhetherAdvancePayment": 1,
                                                 "fnumberOfSettlement": 1, "fmoneyWay": 0, "fadvancePayment": 3100000,
                                                 "fadvanceProportion": 10000, "fadvancePaymentClause": 0,
                                                 "fadvancePaymentClauseStr": None, "ftheFirstPayment": 3100000,
                                                 "ftheFirstProportion": 10000, "ftheFirstPaymentClause": 0,
                                                 "ftheFirstPaymentClauseStr": "微信", "fmetaphasePayment": None,
                                                 "fmetaphaseProportion": None, "fmetaphasePaymentClause": 0,
                                                 "fmetaphasePaymentClauseStr": None, "ffinalPayment": None,
                                                 "ffinalProportion": None, "ffinalPaymentClause": 0,
                                                 "ffinalPaymentClauseStr": None,
                                                 "fadvanceEstimatedTimeOfPayment": get_current_time(),
                                                 "ftheFirstEstimatedTimeOfPayment": get_current_time(),
                                                 "fmetaphaseEstimatedTimeOfPayment": None,
                                                 "ffinalEstimatedTimeOfPayment": None, "festimatePurchaseCost": 0,
                                                 "fotherPayment": 0},
                    "xyPurchaseOrderDeliveryDO": {"ftransportType": 1, "fdeliveryAddress": "广东",
                                                  "fdeliveryDate": get_current_time()},
                    "xyPurchaseOrderSkuVOList": [
                        {"fpurchaseOrderSkuId": None, "fpurchaseOrderId": None, "fskuId": "118905121", "fbrandLabel": 0,
                         "fpurchaseAmount": 100, "ftaxRate": 10, "ftaxIncluded": 1000000, "ftaxIncludedUnit": None,
                         "fwarehousingCost": 990100, "fwarehousingCostUnit": 1000000, "taxIncluded": 1,
                         "warehousingCost": 0.9901, "shareCost": None, "totalAmountOfTaxOriginalCurrency": 100,
                         "notTotalAmountOfTaxOriginalCurrency": 99.01, "amountOfTaxOriginalCurrency": 0.99,
                         "taxIncludedBaseCurrency": 1, "warehousingCostBaseCurrency": 0.99,
                         "totalAmountOfTaxBaseCurrency": 100,
                         "notTotalAmountOfTaxBaseCurrency": 99.01, "amountOfTaxBaseCurrency": 0.99,
                         "fskuName": "英国Matchstick Monkey火柴猴牙胶宝宝婴儿咬咬安抚磨牙棒软硅胶—红色 个", "fcategoryName": "母婴用品",
                         "fbrandName": "火柴猴", "fbrandNameEng": "Matchstick Monkey", "skuBidNumAndPriceDTO": None,
                         "funit": None,
                         "fskuInternationalNo": "0611901211053", "fpurchaseOrderSkuChangeId": None, "fdataType": None,
                         "foriginId": 8, "ftaxRateString": "1%", "edit": False},
                        {"fpurchaseOrderSkuId": None, "fpurchaseOrderId": None, "fskuId": "DL157941907294202",
                         "fbrandLabel": 1,
                         "fpurchaseAmount": 100, "ftaxRate": 0, "ftaxIncluded": 2000000, "ftaxIncludedUnit": None,
                         "fwarehousingCost": 2000000, "fwarehousingCostUnit": 1000000, "taxIncluded": 2,
                         "warehousingCost": 2,
                         "shareCost": None, "totalAmountOfTaxOriginalCurrency": 200,
                         "notTotalAmountOfTaxOriginalCurrency": 200,
                         "amountOfTaxOriginalCurrency": 0, "taxIncludedBaseCurrency": 2,
                         "warehousingCostBaseCurrency": 2,
                         "totalAmountOfTaxBaseCurrency": 200, "notTotalAmountOfTaxBaseCurrency": 200,
                         "amountOfTaxBaseCurrency": 0, "fskuName": "潘多拉项链 彩金", "fcategoryName": "服饰鞋包",
                         "fbrandName": "SWAROVSKI 施华洛世奇", "fbrandNameEng": "", "skuBidNumAndPriceDTO": None,
                         "funit": None,
                         "fskuInternationalNo": "121221", "fpurchaseOrderSkuChangeId": None, "fdataType": None,
                         "foriginId": 2,
                         "ftaxRateString": "0%", "edit": False},
                        {"fpurchaseOrderSkuId": None, "fpurchaseOrderId": None, "fskuId": "GMH02965-J",
                         "fbrandLabel": 2,
                         "fpurchaseAmount": 100, "ftaxRate": 30, "ftaxIncluded": 100000, "ftaxIncludedUnit": None,
                         "fwarehousingCost": 97100, "fwarehousingCostUnit": 1000000, "taxIncluded": 0.1,
                         "warehousingCost": 0.0971, "shareCost": None, "totalAmountOfTaxOriginalCurrency": 10,
                         "notTotalAmountOfTaxOriginalCurrency": 9.71, "amountOfTaxOriginalCurrency": 0.29,
                         "taxIncludedBaseCurrency": 0.1, "warehousingCostBaseCurrency": 0.1,
                         "totalAmountOfTaxBaseCurrency": 10,
                         "notTotalAmountOfTaxBaseCurrency": 9.71, "amountOfTaxBaseCurrency": 0.29,
                         "fskuName": "悦木之源 蘑菇水200ml 菌菇水 200ml", "fcategoryName": "美妆个护", "fbrandName": "悦木之源",
                         "fbrandNameEng": "", "skuBidNumAndPriceDTO": None, "funit": None,
                         "fskuInternationalNo": "717334229594", "fpurchaseOrderSkuChangeId": None, "fdataType": None,
                         "foriginId": 30, "ftaxRateString": "3%", "edit": False}],
                    "xyPurchaseOrderContractDO": {"fagreementId": 239, "fagreementNum": "TXY-PC-HHGYS/200311-02",
                                                  "fagreementType": 0, "finvoiceType": 0, "fmoneyWay": 0,
                                                  "fpaymentComment": "sfdsdfsddsfdsfdsfdsf"},
                    "restsPurchaseOrderAttachmentDOList": [
                        {"fattachmentName": "账号.txt", "fattachmentUrl": "M00/00/9A/wKgA3l6zsfCAWgohAAACf-Z7Kz4885.txt",
                         "fattachmentSize": 639, "fattachmentType": 0, "fdataType": 0, "fpurchaseBillId": None}],
                    "supplierFileDelete": False}
        if str(get_b2b_host) == "http://192.168.1.227:3003":
            data = data_dev
        else:
            data = data_test

        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/po/add".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )

        # self.log.log_info("新建采购订单接口请求信息:{}".format(data))
        self.log.log_info("新建采购订单接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("查询采购订单")
    def bns_po_list(self, ):
        data = {
            "pageIndex": 1
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/po/list".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )

        # self.log.log_info("采购列表接口请求信息:{}".format(data))
        self.log.log_info("采购列表接口返回信息:{}".format(response.json()))

        return response.json()

    @allure_attach("查看订单详情")
    def bns_po_detail(self, order):
        data = {
            "purchaseOrderId": order
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/po/details".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )

        # self.log.log_info("采购列表接口请求信息:{}".format(data))
        self.log.log_info("采购订单详情返回信息:{}".format(response.json()))

        return response.json()

    @allure_attach("提交审批采购订单")
    def bns_po_oa_submit(self):
        self.order = JsonHelper.parseJson_by_objectpath(self.bns_po_list(), "$.retEntity..fpurchaseOrderId")[0]
        data_test = {
            "xyPurchaseOrderSkuVOList": [
                {"fpurchaseOrderSkuId": 15763, "fpurchaseOrderId": self.order, "fskuId": "118905004",
                 "fbrandLabel": 1, "fpurchaseAmount": 20, "ftaxRate": 0, "ftaxIncluded": 1000000,
                 "ftaxIncludedUnit": 1000000, "fwarehousingCost": 1000000, "fwarehousingCostUnit": 1000000,
                 "taxIncluded": 1, "warehousingCost": 1, "shareCost": None, "totalAmountOfTaxOriginalCurrency": 20,
                 "notTotalAmountOfTaxOriginalCurrency": 20, "amountOfTaxOriginalCurrency": 0,
                 "taxIncludedBaseCurrency": 1, "warehousingCostBaseCurrency": 1, "totalAmountOfTaxBaseCurrency": 20,
                 "notTotalAmountOfTaxBaseCurrency": 20, "amountOfTaxBaseCurrency": 0,
                 "fskuName": "Comotomo可么多么奶瓶婴儿防胀气进口全硅胶奶瓶2*250ml/盒 2*250ml/盒", "fcategoryName": "母婴用品",
                 "fbrandName": "Como tomo", "fbrandNameEng": "", "skuBidNumAndPriceDTO": None, "funit": "瓶盒",
                 "fskuInternationalNo": "886074000043", "fpurchaseOrderSkuChangeId": None, "fdataType": None,
                 "foriginId": 21, "ftaxRateString": "0%"},
                {"fpurchaseOrderSkuId": 15762, "fpurchaseOrderId": self.order, "fskuId": "118905006",
                 "fbrandLabel": 0, "fpurchaseAmount": 10, "ftaxRate": 10, "ftaxIncluded": 10000,
                 "ftaxIncludedUnit": 1000000, "fwarehousingCost": 10000, "fwarehousingCostUnit": 1000000,
                 "taxIncluded": 0.01, "warehousingCost": 0.01, "shareCost": None,
                 "totalAmountOfTaxOriginalCurrency": 0.1, "notTotalAmountOfTaxOriginalCurrency": 0.1,
                 "amountOfTaxOriginalCurrency": 0, "taxIncludedBaseCurrency": 0.01, "warehousingCostBaseCurrency": 0.01,
                 "totalAmountOfTaxBaseCurrency": 0.1, "notTotalAmountOfTaxBaseCurrency": 0.1,
                 "amountOfTaxBaseCurrency": 0, "fskuName": "TIGER虎牌 儿童保温杯MBR-T06G 吸管杯国际版 老虎 600ml",
                 "fcategoryName": "母婴用品", "fbrandName": "虎牌", "fbrandNameEng": "TIGER", "skuBidNumAndPriceDTO": None,
                 "funit": "个", "fskuInternationalNo": "4904710424933", "fpurchaseOrderSkuChangeId": None,
                 "fdataType": None, "foriginId": 14, "ftaxRateString": "1%"},
                {"fpurchaseOrderSkuId": 15764, "fpurchaseOrderId": self.order, "fskuId": "122305131",
                 "fbrandLabel": 2, "fpurchaseAmount": 30, "ftaxRate": 20, "ftaxIncluded": 2000000,
                 "ftaxIncludedUnit": 1000000, "fwarehousingCost": 1960667, "fwarehousingCostUnit": 1000000,
                 "taxIncluded": 2, "warehousingCost": 1.960667, "shareCost": None,
                 "totalAmountOfTaxOriginalCurrency": 60, "notTotalAmountOfTaxOriginalCurrency": 58.82,
                 "amountOfTaxOriginalCurrency": 1.18, "taxIncludedBaseCurrency": 2,
                 "warehousingCostBaseCurrency": 1.960667, "totalAmountOfTaxBaseCurrency": 60,
                 "notTotalAmountOfTaxBaseCurrency": 58.82, "amountOfTaxBaseCurrency": 1.18,
                 "fskuName": "Technic雪佛兰 ZR1 跑车42093 盒", "fcategoryName": "母婴用品", "fbrandName": "LEGO乐高",
                 "fbrandNameEng": "", "skuBidNumAndPriceDTO": None, "funit": "盒", "fskuInternationalNo": "585015266999",
                 "fpurchaseOrderSkuChangeId": None, "fdataType": None, "foriginId": 9, "ftaxRateString": "2%"}],
            "xyPurchaseOrderFinanceDO": {
                "advanceProportion": 100,
                "advancePayment": 0,
                "advanceProportionPayment": "100.00% 0.00",
                "metaphaseProportion": 0,
                "metaphasePayment": 0,
                "metaphaseProportionPayment": "",
                "finalProportion": 0,
                "finalPayment": 0,
                "finalProportionPayment": "",
                "totalAmountOfTaxOriginalCurrency": 100,
                "notTotalAmountOfTaxOriginalCurrency": 98.04,
                "amountOfTaxOriginalCurrency": 1.96,
                "totalAmountOfTaxBaseCurrency": 100,
                "notTotalAmountOfTaxBaseCurrency": 98.04,
                "amountOfTaxBaseCurrency": 1.96,
                "estimatePurchaseCost": 0,
                "estimatePurchaseCostOfBase": 0,
                "ffinanceId": 1206,
                "fcurrencyCode": "CNY",
                "payMoneyPlanBoList": None,
                "fexchangeRate": 1000000,
                "fexchangeRateView": 1,
                "fpurchaseInvoiceType": 1,
                "fwhetherAdvancePayment": 1,
                "fnumberOfSettlement": 1,
                "fmoneyWay": 1,
                "fadvancePayment": 1000000,
                "fadvanceProportion": 10000,
                "fadvancePaymentClause": 0,
                "fadvancePaymentClauseStr": "微信",
                "ftheFirstPayment": 1000000,
                "ftheFirstProportion": 10000,
                "ftheFirstPaymentClause": 0,
                "ftheFirstPaymentClauseStr": "微信",
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
                "fdeliveryId": 1208,
                "ftransportType": 1,
                "fdeliveryAddress": "深圳",
                "fdeliveryDate": get_current_time(day=1)
            },
            "xyPurchaseOrderDO": {
                "fpurchaseOrderId": self.order,
                "fbidId": None,
                "ferpOrderId": "121111",
                "fsaleOrderId": None,
                "fsupplierBidTradeId": None,
                "fcorporateSubjectId": 102,
                "fsupplierId": 531,
                "fpurchaseAid": 120,
                "ffinanceId": 1206,
                "fdeliveryId": 1208,
                "fpurchaseDeptName": "测试开发团队",
                "fsupplierName": "哈哈供应商2",
                "fsupplierLeader": "图图",
                "fsupplierLeaderPhone": "13026161548",
                "fourCompanyName": "深圳市天行云供应链有限公司",
                "fourCompanyLeader": "刘丽君",
                "fourCompanyLeaderPhone": "17688546806",
                "fagreementId": "TXY-PC-HHGYS/191224-001",
                "fplanType": 1,
                "ftradeType": 1,
                "fquotationMethod": "CPT",
                "fsourceArea": "湖北",
                "fshelfLife": "36",
                "fpurchaseOrderStatus": 1,
                "fclosingReasons": None,
                "fpurchaseOrderNotes": None,
                "fsourceAreaName": "湖北",
                "fautoCreate": 0,
                "finspection": 0,
                "forderLabels": 1,
                "fcreateTime": get_current_time(),
                "fsupplierBidTradeIdTradeId": None
            },
            "purchasPurchaseOrderAttachmentDOList": [],
            "restsPurchaseOrderAttachmentDOList": [
                {
                    "fattachmentName": "账号.txt",
                    "fattachmentUrl": "M00/00/BB/wKgA316paICALoAbAAACf-Z7Kz4219.txt",
                    "fattachmentSize": 639,
                    "fattachmentType": 0,
                    "fdataType": 0,
                    "fpurchaseBillId": self.order
                }
            ],
            "oaComments": None,
            "fpurchaseOrderChangeId": None,
            "supplierFileDelete": False,
            "xyPurchaseOrderContractDO": {
                "fpurchaseContractId": 1958,
                "fpurchaseOrderId": self.order,
                "fagreementId": 220,
                "fagreementNum": "TXY-PC-HHGYS/191224-001",
                "fagreementType": 1,
                "finvoiceType": 1,
                "fmoneyWay": 1,
                "fpaymentComment": "三个结算啊大大说",
                "fcreateTime": None,
                "fmodifyTime": None
            },
            "poRelationWarehouseInfoBBVoList": None,
            "paymentRequisitionList": None
        }
        data_dev = {"xyPurchaseOrderSkuVOList": [
            {"fpurchaseOrderSkuId": 4305, "fpurchaseOrderId": self.order, "fskuId": "118905121", "fbrandLabel": 0,
             "fpurchaseAmount": 100, "ftaxRate": 10, "ftaxIncluded": 1000000, "ftaxIncludedUnit": 1000000,
             "fwarehousingCost": 990100, "fwarehousingCostUnit": 1000000, "taxIncluded": 1, "warehousingCost": 0.9901,
             "shareCost": None, "totalAmountOfTaxOriginalCurrency": 100, "notTotalAmountOfTaxOriginalCurrency": 99.01,
             "amountOfTaxOriginalCurrency": 0.99, "taxIncludedBaseCurrency": 1, "warehousingCostBaseCurrency": 0.9901,
             "totalAmountOfTaxBaseCurrency": 100, "notTotalAmountOfTaxBaseCurrency": 99.01,
             "amountOfTaxBaseCurrency": 0.99, "fskuName": "英国Matchstick Monkey火柴猴牙胶宝宝婴儿咬咬安抚磨牙棒软硅胶—红色 个",
             "fcategoryName": "母婴用品", "fbrandName": "火柴猴", "fbrandNameEng": "Matchstick Monkey",
             "skuBidNumAndPriceDTO": None, "funit": "红色", "fskuInternationalNo": "0611901211053",
             "fpurchaseOrderSkuChangeId": None, "fdataType": None, "foriginId": 8, "ftaxRateString": "1%",
             "edit": False},
            {"fpurchaseOrderSkuId": 4306, "fpurchaseOrderId": self.order, "fskuId": "DL157941907294202",
             "fbrandLabel": 1, "fpurchaseAmount": 100, "ftaxRate": 0, "ftaxIncluded": 2000000,
             "ftaxIncludedUnit": 1000000, "fwarehousingCost": 2000000, "fwarehousingCostUnit": 1000000,
             "taxIncluded": 2, "warehousingCost": 2, "shareCost": None, "totalAmountOfTaxOriginalCurrency": 200,
             "notTotalAmountOfTaxOriginalCurrency": 200, "amountOfTaxOriginalCurrency": 0, "taxIncludedBaseCurrency": 2,
             "warehousingCostBaseCurrency": 2, "totalAmountOfTaxBaseCurrency": 200,
             "notTotalAmountOfTaxBaseCurrency": 200, "amountOfTaxBaseCurrency": 0, "fskuName": "潘多拉项链 彩金",
             "fcategoryName": "服饰鞋包", "fbrandName": "SWAROVSKI 施华洛世奇", "fbrandNameEng": "",
             "skuBidNumAndPriceDTO": None, "funit": "**", "fskuInternationalNo": "121221",
             "fpurchaseOrderSkuChangeId": None, "fdataType": None, "foriginId": 2, "ftaxRateString": "0%",
             "edit": False},
            {"fpurchaseOrderSkuId": 4307, "fpurchaseOrderId": self.order, "fskuId": "GMH02965-J", "fbrandLabel": 2,
             "fpurchaseAmount": 100, "ftaxRate": 30, "ftaxIncluded": 100000, "ftaxIncludedUnit": 1000000,
             "fwarehousingCost": 97100, "fwarehousingCostUnit": 1000000, "taxIncluded": 0.1, "warehousingCost": 0.0971,
             "shareCost": None, "totalAmountOfTaxOriginalCurrency": 10, "notTotalAmountOfTaxOriginalCurrency": 9.71,
             "amountOfTaxOriginalCurrency": 0.29, "taxIncludedBaseCurrency": 0.1, "warehousingCostBaseCurrency": 0.0971,
             "totalAmountOfTaxBaseCurrency": 10, "notTotalAmountOfTaxBaseCurrency": 9.71,
             "amountOfTaxBaseCurrency": 0.29, "fskuName": "悦木之源 蘑菇水200ml 菌菇水 200ml", "fcategoryName": "美妆个护",
             "fbrandName": "悦木之源", "fbrandNameEng": "", "skuBidNumAndPriceDTO": None, "funit": "悦木之源",
             "fskuInternationalNo": "717334229594", "fpurchaseOrderSkuChangeId": None, "fdataType": None,
             "foriginId": 30, "ftaxRateString": "3%", "edit": False}],
            "xyPurchaseOrderFinanceDO": {"advanceProportion": 100, "advancePayment": 310,
                                         "advanceProportionPayment": "100.00% 310.00", "metaphaseProportion": 0,
                                         "metaphasePayment": 0, "metaphaseProportionPayment": "",
                                         "finalProportion": 0, "finalPayment": 0, "finalProportionPayment": "",
                                         "totalAmountOfTaxOriginalCurrency": 310,
                                         "notTotalAmountOfTaxOriginalCurrency": 308.72,
                                         "amountOfTaxOriginalCurrency": 1.28,
                                         "totalAmountOfTaxBaseCurrency": 310,
                                         "notTotalAmountOfTaxBaseCurrency": 308.72,
                                         "amountOfTaxBaseCurrency": 1.28, "estimatePurchaseCost": 0,
                                         "estimatePurchaseCostOfBase": 0, "ffinanceId": 743,
                                         "fcurrencyCode": "CNY", "payMoneyPlanBoList": None,
                                         "fexchangeRate": 1000000, "fexchangeRateView": 1,
                                         "fpurchaseInvoiceType": 0, "fwhetherAdvancePayment": 1,
                                         "fnumberOfSettlement": 1, "fmoneyWay": 0, "fadvancePayment": 3100000,
                                         "fadvanceProportion": 10000, "fadvancePaymentClause": 0,
                                         "fadvancePaymentClauseStr": "微信", "ftheFirstPayment": 3100000,
                                         "ftheFirstProportion": 10000, "ftheFirstPaymentClause": 0,
                                         "ftheFirstPaymentClauseStr": "微信", "fmetaphasePayment": None,
                                         "fmetaphaseProportion": None, "fmetaphasePaymentClause": 0,
                                         "fmetaphasePaymentClauseStr": None, "ffinalPayment": None,
                                         "ffinalProportion": None, "ffinalPaymentClause": 0,
                                         "ffinalPaymentClauseStr": None,
                                         "fadvanceEstimatedTimeOfPayment": get_current_time(),
                                         "ftheFirstEstimatedTimeOfPayment": get_current_time(),
                                         "fmetaphaseEstimatedTimeOfPayment": None,
                                         "ffinalEstimatedTimeOfPayment": None, "festimatePurchaseCost": 0,
                                         "fotherPayment": 0},
            "xyPurchaseOrderDeliveryDO": {"fdeliveryId": 744, "ftransportType": 1, "fdeliveryAddress": "广东",
                                          "fdeliveryDate": get_current_time()},
            "xyPurchaseOrderDO": {"fpurchaseOrderId": self.order, "fbidId": None, "fstockUpPlanId": None,
                                  "ferpOrderId": "123321456", "fsaleOrderId": None, "fsupplierBidTradeId": None,
                                  "fcorporateSubjectId": 102, "fsupplierId": 531, "fpurchaseAid": 120,
                                  "ffinanceId": 743, "fdeliveryId": 744, "fpurchaseDeptName": "测试开发团队",
                                  "fsupplierName": "哈哈供应商2", "fsupplierLeader": "ben",
                                  "fsupplierLeaderPhone": "13264645696", "fourCompanyName": "深圳市天行云供应链有限公司",
                                  "fourCompanyLeader": "刘丽君", "fourCompanyLeaderPhone": "17688546806",
                                  "fagreementId": "TXY-PC-HHGYS/200311-02", "fplanType": 1, "ftradeType": 1,
                                  "fquotationMethod": "CPT", "fsourceArea": "湖北", "fshelfLife": "30",
                                  "fpurchaseOrderStatus": 1, "fclosingReasons": None,
                                  "fpurchaseOrderNotes": None, "fsourceAreaName": "湖北", "fautoCreate": 0,
                                  "finspection": 0, "forderLabels": 1, "fcreateTime": get_current_time(),
                                  "fsupplierBidTradeIdTradeId": None},
            "purchasPurchaseOrderAttachmentDOList": [], "restsPurchaseOrderAttachmentDOList": [
                {"fattachmentName": "账号.txt", "fattachmentUrl": "M00/00/9A/wKgA3l6zsfCAWgohAAACf-Z7Kz4885.txt",
                 "fattachmentSize": "639", "fattachmentType": 0, "fdataType": 0, "fpurchaseBillId": self.order}],
            "oaComments": None, "fpurchaseOrderChangeId": None, "supplierFileDelete": False,
            "xyPurchaseOrderContractDO": {"fpurchaseContractId": 336, "fpurchaseOrderId": self.order,
                                          "fagreementId": 239, "fagreementNum": "TXY-PC-HHGYS/200311-02",
                                          "fagreementType": 0, "finvoiceType": 0, "fmoneyWay": 0,
                                          "fpaymentComment": "sfdsdfsddsfdsfdsfdsf", "fcreateTime": None,
                                          "fmodifyTime": None}, "poRelationWarehouseInfoBBVoList": None,
            "paymentRequisitionList": None}
        if str(get_b2b_host) == "http://192.168.1.227:3003":
            data = data_dev
        else:
            data = data_test
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/po/oa/submit".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # self.log.log_info("提交审批采购订单接口请求信息:{}".format(data))
        self.log.log_info("提交审批采购订单接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("待审批的订单撤回")
    def bns_po_oa_recall(self):
        data = {"purchaseOrderId": self.order}
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/po/oa/recall".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("待审批的订单撤回接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("OA模拟审批通过")
    def bns_po_pass(self):
        self.order = JsonHelper.parseJson_by_objectpath(self.bns_po_list(), "$.retEntity..fpurchaseOrderId")[0]
        data = {
            "purchaseOrderId": self.order
        }
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/po/pass".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # self.log.log_info("OA模拟审批接口请求信息:{}".format(data))
        self.log.log_info("OA模拟审批接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("采购入库通知列表")
    def bns_po_stock_list(self):
        data = {"pageIndex": 1, "pageSize": 10, "fpurchaseOrderEnterStockId": None, "fpurchaseOrderId": None,
                "fwarehouseName": None, "fsupplierName": None, "fenterStockStatus": None}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/purchase-order/stock/list".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # self.log.log_info("采购列表接口请求信息:{}".format(data))
        self.log.log_info("采购入库通知列表接口返回信息:{}".format(response.json()))

        return response.json()

    @allure_attach("采购退货通知列表")
    def bns_po_reback_list(self):
        data = {"pageIndex": 1, "pageSize": 10, "fpurchaseOrderEnterStockId": None, "fpurchaseOrderId": None,
                "fwarehouseName": None, "fsupplierName": None, "fenterStockStatus": None}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderOutStock/remote/selectPurchaseReturnNoticeList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        # self.log.log_info("采购列表接口请求信息:{}".format(data))
        self.log.log_info("采购退货通知列表接口返回信息:{}".format(response.json()))

        return response.json()


if __name__ == '__main__':
    a = BnsApi_Po()
    # a.bns_new_po_add()
    # a.bns_po_pass()
    # a.bns_po_stock_add()
    # a.bns_warehouseOrderInStock_saveOrUpdatePONotice()
    # a.bns_warehouseOrderInStock_save()
    # a.bns_warehouse_center_polist()
    a.bns_po_stock_list()
