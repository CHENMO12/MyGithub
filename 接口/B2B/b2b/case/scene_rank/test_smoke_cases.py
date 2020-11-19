# # -*- coding: utf-8 -*-
# # @Time    : 2019/7/14 23:52
# # @Author  : chinablue
# # @Email   : dongjun@reconova.cn
# # @File    : test_smoke_cases.py
import pytest
import allure
import time
import json
import jsonpath
from case import BaseCase
from bns.b2b.api import Api  # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
from case.utils import positive_check_bb_response, positive_check_stock_response

api_admin = Api(username=None, password=None)


def json_path(res, pattern):
    if isinstance(res, dict):
        try:
            res = jsonpath.jsonpath(res, pattern)
        except:
            raise Exception("pattern({})不正确或res({})为空".format(res, pattern))
        return res
    else:
        raise Exception('不是json字符串')


def BusinessType(res_info):
    # 需要用jsonpath 提取字符串
    # fplanType = JsonHelper.parseJson_by_objectpath(res_info, "$..*[@.fplanType is 1")
    fplanType = json_path(res_info, '$..fplanType')
    num = 0
    for i in fplanType:
        num = num + 1
        if i == 1 or 2:
            return num - 1


@allure.feature("基本功能")
@allure.story("冒烟测试")
class Test(BaseCase):
    # 主菜单
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询到菜单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.scn_queryMenu_menu(id=None, res_accurate=False, business_exception=False)
        positive_check_bb_response(res_info)

    # 采购
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询到采购订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_po_list()
        positive_check_bb_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查看某个采购订单详情(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_po_list()
            num = BusinessType(res_info)
            self.fpurchaseOrderId = jsonpath.jsonpath(res_info, "$.retEntity..fpurchaseOrderId")[num]
            res_info = api_admin.bns_po_detail(order=self.fpurchaseOrderId)
        positive_check_bb_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询到采购入库通知列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_po_stock_list()
        positive_check_bb_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询到采购退货列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_po_reback_list()
        positive_check_bb_response(res_info)

    # 销售
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询到销售订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_so_list()
        positive_check_bb_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询某个销售订单列表详情(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_so_list()
            num = BusinessType(res_info)
            self.fpurchaseOrderId = jsonpath.jsonpath(res_info, "$.retEntity..fsaleOrderId")[num]
            res_info = api_admin.bns_so_detail(fsaleOrderId=self.fpurchaseOrderId)
        positive_check_bb_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询到销售出库列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_so_sale_saleDeliveryApplyList()
        positive_check_bb_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询到销售退货列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_so_sale_returnList()
        positive_check_bb_response(res_info)

    # 仓库
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_仓库采购入库订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouseOrderInStock_polist()
        positive_check_stock_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_仓库销售退货订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouseOrderInStock_soreback()
        positive_check_stock_response(res_info)
        pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_仓库调拨入库订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouseOrderInStock_in_list()
        positive_check_stock_response(res_info)
        pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_仓库其他入库订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouseOrderInStock_other_in_list()
        positive_check_stock_response(res_info)
        pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_仓库销售出库订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_so_sale_warehouse_solist()
        positive_check_stock_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_仓库采购退货订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouseOrderInStock_po_back_list()
        positive_check_stock_response(res_info)
        pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_仓库调拨出库订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouseOrderInStock_out_list()
        positive_check_stock_response(res_info)
        pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_仓库其他出库订单列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouseOrderInStock_other_out_list()
        positive_check_stock_response(res_info)
        pass

    # 库存中心
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心通知(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_noticelist()
        positive_check_stock_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心采购入库列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_polist()
        positive_check_stock_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心采购退货列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_poback()
        positive_check_stock_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心采购订单详情(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_polist()
            finStockId = jsonpath.jsonpath(res_info, "$.data..finStockId")[0]
            res_info = api_admin.bns_warehouse_center_podetail(finStockId=finStockId)
        positive_check_stock_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心销售出库列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_solist()
        positive_check_stock_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心销售退货列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_soback()
        positive_check_stock_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心调拨入库列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouseOrderInStock_in_list()
        positive_check_stock_response(res_info)
        pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心调拨出库列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_out_list()
        positive_check_stock_response(res_info)
        pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心其他入库列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_other_in_list()
        positive_check_stock_response(res_info)
        pass

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_库存中心其他出库列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_warehouse_center_other_out_list()
        positive_check_stock_response(res_info)
        pass


if __name__ == '__main__':
    pytest.main()
