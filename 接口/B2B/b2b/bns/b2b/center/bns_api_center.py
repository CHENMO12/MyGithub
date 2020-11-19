#!/usr/bin/python3.7
# @Time : 2020/6/15 0015 16:43 
from base.decorators import allure_attach
from base.helper import JsonHelper
from testdata.gen_bnsData import *
from bns.b2b import BusinessApi
from config import *
import json
import time


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    # 库存中心
    @allure_attach("库存中心通知查询")
    def bns_warehouse_center_noticelist(self, ):
        data = {"currentPage": 1, "pageSize": 10, "labelWidth": "120px", "time": "", "fnoticeOrderNum": "",
                "frelationOrderNum": "", "fcompanyName": "", "fwarehouseId": "", "fbusinessType": "", "fnoticeType": ""}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouse/queryNoticeList".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心通知接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("库存中心采购入库单列表查询")
    def bns_warehouse_center_polist(self, ):
        data = {"queryType": 1, "currentPage": 1, "pageSize": 10}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/stockCenterInStockController/queryPOInStockListByBill".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心采购订单列表接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("库存中心采购入库单详情")
    def bns_warehouse_center_podetail(self, finStockId=None):
        self.headers["use-node-method"] = "commonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/warehouseOrderInStock/queryPONoticeDetail?finStockId={}".format(get_b2b_host,
                                                                                                  finStockId),
            headers=self.headers
        )
        self.log.log_info("库存中心采购订单详情接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("库存中心采购退货单列表查询")
    def bns_warehouse_center_poback(self, ):
        data = {"currentPage": 1, "pageSize": 10, "showType": "bill", "foutStockType": 2, "labelWidth": "120px",
                "fbusinessType": "", "foutStockOrderNum": "", "fpurchaseOrderCode": "", "fsubjectName": "",
                "fwarehouseId": "", "fwarehouseName": "", "fcompanyName": "", "freturnReason": ""}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/stockCenterOutStockController/selectReturnPurchaseStockListForBill".format(
                get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心采购退货单接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("库存中心销售出库单列表查询")
    def bns_warehouse_center_solist(self, ):
        data = {"currentPage": 1, "pageSize": 10, "showType": "bill", "foutStockType": 1, "labelWidth": "120px",
                "fbusinessType": "", "foutStockOrderNum": "", "fsaleOrderNum": "", "fsubjectName": "", "fskuName": "",
                "fwarehouseId": "", "fcompanyName": ""}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/stockCenterOutStockController/selectWarehouseOrderOutStcokListForBill".format(
                get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心销售出库订单列表接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("库存中心销售退货单列表查询")
    def bns_warehouse_center_soback(self, ):
        data = {"currentPage": 1, "pageSize": 10, "queryType": 1, "time": [], "fbusinessType": "",
                "finStockOrderNum": "", "frelationOrderNum": "", "fxyCompanyName": "", "fwarehouseId": "",
                "fcompanyName": "", "freturnReason": "", "fskuId": "", "fskuName": "", "finStockTimeStart": "",
                "finStockTimeEnd": ""}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/stockCenterInStockController/querySROInStockListByBill".format(
                get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心销售退货单列表接口返回信息:{}".format(response.json()))
        return response.json()

    @allure_attach("库存中心调拨入库单列表查询")
    def bns_warehouse_center_in_list(self, ):
        data = {"currentPage": 1, "pageSize": 10, "queryType": 1}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/stockCenterInStockController/queryAllotListByBills".format(
                get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心调拨入库单列表接口返回信息:{}".format(response.json()))
        return response.json()
        pass

    @allure_attach("库存中心调拨出库单列表查询")
    def bns_warehouse_center_out_list(self, ):
        data = {"currentPage": 1, "pageSize": 10, "searchType": -1}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/allocate/outStock/bills/list".format(
                get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心调拨出库单列表接口返回信息:{}".format(response.json()))
        return response.json()

        pass

    @allure_attach("库存中心其他入库单列表查询")
    def bns_warehouse_center_other_in_list(self, ):
        data = {"currentPage": 1, "pageSize": 10, "queryType": 1}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/stockCenterInStockController/queryOtherInStockListByBill".format(
                get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心调拨入库单列表接口返回信息:{}".format(response.json()))
        return response.json()
        pass

    @allure_attach("库存中心其他出库单列表查询")
    def bns_warehouse_center_other_out_list(self, ):
        data = {"currentPage": 1, "pageSize": 10, "queryType": 1}
        self.headers["use-node-method"] = "jsonRequest"
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/new/warehouse/stockCenterOutStockController/selectOtherOutStockListForBill".format(
                get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("库存中心其他出库单列表接口返回信息:{}".format(response.json()))
        return response.json()

        pass


if __name__ == '__main__':
    a = BnsApi()
    a.bns_warehouse_center_other_in_list()
