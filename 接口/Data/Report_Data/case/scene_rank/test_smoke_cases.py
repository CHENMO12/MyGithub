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
from bns.data.api import Api  # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
from case.utils import positive_check_data_response, positive_check_order_response,positive_check_afterOrder_response
from base.helper import JsonPath

api_admin = Api(username=None, password=None)


@allure.feature("基本功能")
@allure.story("冒烟测试")
class Test(BaseCase):
    # BBC3.0订单查询
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询BBC3列表(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_queryData_three()
        positive_check_data_response(res_info)

    # BBC4.0订单查询
    @allure.severity(allure.severity_level.BLOCKER)
    def test_正测_数据中台已推送订单_查询BBC4列表(self):
        with allure.step('接口请求'):
            # 数据中台获取订单id
            res = api_admin.bns_queryOeder_opt()
            forder_id = JsonPath.json_path(res, "$..forderId")[0]
            # 数仓
            res_info = api_admin.bns_queryData_four(forder_id=forder_id)
        positive_check_order_response(res_info, order_id=forder_id)

    @allure.severity(allure.severity_level.BLOCKER)
    def test_正测_数据中台售后订单_查询BBC4售后列表(self):
        with allure.step('接口请求'):
            res = api_admin.bns_overSale_opt()
            forder_id = JsonPath.json_path(res, "$..forderId")[0]
            res_info = api_admin.bns_afterSale_four(forder_id=forder_id)
        positive_check_order_response(res_info,order_id=forder_id)

    @allure.severity(allure.severity_level.BLOCKER)
    def test_正测_数据中台售后工单_查询BBC4售工单列表(self):
        with allure.step('接口请求'):
            res = api_admin.bns_supplieList_opt()
            forder_id = JsonPath.json_path(res, "$..fsupplierWorkOrder")[0]
            res_info = api_admin.bns_supplierWorkOrder_four(forder_id=forder_id)
        positive_check_afterOrder_response(res_info, order_id=forder_id)
    # 业务日报
    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查看品牌中心日报(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_queryData_report_brand()

        positive_check_data_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询渠道中心日报(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_queryData_report_channel()
        positive_check_data_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询商品中心日报(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_queryData_report_sku()
        positive_check_data_response(res_info)

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_查询品牌销售日报(self):
        with allure.step('接口请求'):
            res_info = api_admin.bns_queryData_report_sale()
        positive_check_data_response(res_info)


if __name__ == '__main__':
    pytest.main()
