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

    @allure_attach("订单查询")
    def bns_queryData_three(self, data=None):
        # TODO: 请完成函数注释!!!

        if data is None: data = {"fdataRoleId": gen_id.get_fdataRoleId(),
                                 "fpermissionId": gen_id.get_real_id(first_name='BBC3.0自助查询服务',second_name='订单查询'),
                                 "fsortName": "",
                                 "fsortType": 1, "currentPage": 1, "pageSize": 10, "commonFieldDtoList": [
                {"ftableAlias": "tso", "ffieldName": "fchannel_type_var", "ftype": 2},
                {"ftableAlias": "tso", "ffieldName": "fmerchant_order_id", "ftype": 3, "fstringQuery": ""},
                {"ftableAlias": "tco", "ffieldName": "fcompany_abbreviation", "ftype": 3, "fstringQuery": ""},
                {"ftableAlias": "tco", "ffieldName": "fdeliver_time", "ftype": 1, "fstartValue": "", "fendValue": ""},
                {"ftableAlias": "tso", "ffieldName": "forder_time", "ftype": 1, "fstartValue": "", "fendValue": ""},
                {"ftableAlias": "tso", "ffieldName": "fpay_time", "ftype": 5, "fstartValue": "", "fendValue": ""},
                {"ftableAlias": "tco", "ffieldName": "forder_time", "ftype": 1, "fstartValue": "", "fendValue": ""},
                {"ftableAlias": "tso", "ffieldName": "funame", "ftype": 3, "fstringQuery": ""}],
                                 "ffieldNames": ["tso.fis_brand_var", "tso.fbd_head", "tso.fbrand_name", "tso.fbuy_num",
                                                 "tso.fcategory_name1", "tso.fchannel_type_var", "tso.fdelivery_name",
                                                 "tso.ffreight_amount", "tso.fgoods_amount", "tso.fgoods_price",
                                                 "undefined.2"]}

        # 请求入参

        self.headers['x-requested-with'] = 'true'
        # 请求地址
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/data/data/admin/order/read/queryData".format(get_data_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("BBC3.0接口返回数据:{}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    a = BnsApi()
    a.bns_queryData_three()
