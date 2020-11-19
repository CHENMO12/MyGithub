#!/usr/bin/python3.7
# @Time : 2020/11/13 17:15
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

    @allure_attach("BBC4.0售后工单查询")
    def bns_supplierWorkOrder_four(self, data=None, forder_id=None):
        # TODO: 请完成函数注释!!!
        if data is None: data = {"fdataRoleId": gen_id.get_fdataRoleId(),
                                 "fpermissionId": gen_id.get_real_id(first_name='BBC4.0自助查询服务', second_name='售后工单查询'),
                                 "fsortName": "", "fsortType": 1, "currentPage": 1, "pageSize": 10,
                                 "commonFieldDtoList": [
                                     {"ftableAlias": "faaw", "ffieldName": "fuser_supplier_work_order", "ftype": 3,
                                      "fstringQuery": forder_id},
                                     {"ftableAlias": "faaw", "ffieldName": "funame", "ftype": 3, "fstringQuery": ""},
                                     {"ftableAlias": "faaw", "ffieldName": "freview_time", "ftype": 1,
                                      "fstartValue": "", "fendValue": ""},
                                     {"ftableAlias": "faaw", "ffieldName": "fadjustment_status_var", "ftype": 2},
                                     {"ftableAlias": "faaw", "ffieldName": "forder_id", "ftype": 3, "fstringQuery": ""},
                                     {"ftableAlias": "faaw", "ffieldName": "forder_aftersale_id", "ftype": 3,
                                      "fstringQuery": ""},
                                     {"ftableAlias": "faaw", "ffieldName": "fis_brand_var", "ftype": 2},
                                     {"ftableAlias": "faaw", "ffieldName": "fchannel_type_var", "ftype": 2}],
                                 "ffieldNames": ["faaw.fuser_supplier_work_order", "faaw.funame", "faaw.freview_time",
                                                 "faaw.fdws_work_type_var", "faaw.fadjustment_status_var",
                                                 "faaw.forder_id", "faaw.fsku_name", "faaw.fsku_code",
                                                 "faaw.forder_aftersale_id", "faaw.fis_brand_var",
                                                 "faaw.finternational_code", "faaw.fchannel_type_var",
                                                 "faaw.fcategory_name1", "faaw.fbrand_name", "faaw.fapply_amount"]}
        # 请求入参

        self.headers['x-requested-with'] = 'true'
        # 请求地址
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/data/data/admin/order/read/queryData".format(get_data_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("BBC4.0售后工单接口返回数据:{}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    a = BnsApi()
    a.bns_supplierWorkOrder_four(forder_id='G016049936568191468')
