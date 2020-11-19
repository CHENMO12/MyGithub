#!/usr/bin/python3.7
# @Time : 2020/11/09 14:10
# -*- coding: utf-8 -*-
# @Time : 2020-11-09 11:37:29
import json

from base.decorators import allure_attach
from bns.data import BusinessApi
from config import get_data_host
from testdata.gen_id import GenId
gen_id = GenId()

class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

        # self._config_queryData = self.base_yaml_info(
        #     curr_file=__file__,
        #     module_key=__name__.split(".")[-2]
        # )

    @allure_attach("BBC4.0订单查询")
    def bns_queryData_four(self, data=None,forder_id =None):
        # TODO: 请完成函数注释!!!
        if data is None: data = {"fdataRoleId": gen_id.get_fdataRoleId(), "fpermissionId": gen_id.get_real_id(first_name='BBC4.0自助查询服务',second_name='订单查询'), "fsortName": "",
                                 "fsortType": 1, "currentPage": 1, "pageSize": 10, "commonFieldDtoList": [
                {"ftableAlias": "so", "ffieldName": "fchannel_type_var", "ftype": 2},
                {"ftableAlias": "so", "ffieldName": "forder_status_var", "ftype": 3, "fstringQuery": ""},
                {"ftableAlias": "so", "ffieldName": "forder_time", "ftype": 1, "fstartValue": "", "fendValue": ""},
                {"ftableAlias": "so", "ffieldName": "funame", "ftype": 3, "fstringQuery": ""},
                {"ftableAlias": "so", "ffieldName": "fpay_time", "ftype": 1, "fstartValue": "", "fendValue": ""},
                {"ftableAlias": "so", "ffieldName": "fplatform_order_no", "ftype": 3, "fstringQuery": ""},
                {"ftableAlias": "so", "ffieldName": "forder_id", "ftype": 7, "fstringQuery": forder_id}],
                                 "ffieldNames": ["co.fsupplier_warehouse_name", "so.fchannel_name",
                                                 "so.fchannel_type_var", "so.forder_pay_type_var",
                                                 "so.forder_status_var", "so.forder_time", "so.fown_brand_var",
                                                 "so.fsku_name", "so.fsku_num", "so.funame", "so.fbatch_id",
                                                 "so.fdeduction_value", "so.fdiscount_amount", "so.finternational_code",
                                                 "so.forder_sku_amount", "so.forder_source_var", "so.fpay_time",
                                                 "so.fplatform_order_no", "so.fsales_tax_amount",
                                                 "co.fpurchase_tax_amount", "so.forder_total_amount",
                                                 "co.fpurchase_total_amount", "co.fsupplier_order_id",
                                                 "so.fsales_freight_amount", "co.fpurchase_freight_amount",
                                                 "so.fsales_all_amount", "co.fpurchase_all_amount",
                                                 "co.fmerchants_head", "co.fpurchase_head", "co.fsaler_head",
                                                 "so.forder_id"]}

        # 请求入参

        self.headers['x-requested-with'] = 'true'
        # 请求地址
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/data/data/admin/order/read/queryData".format(get_data_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("BBC4.0接口返回数据:{}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    a = BnsApi()
    a.bns_queryData_four()
