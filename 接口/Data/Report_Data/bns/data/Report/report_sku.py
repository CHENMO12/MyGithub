#!/usr/bin/python3.7
# @Time : 2020/11/09 14:28
# !/usr/bin/python3.7
# @Time : 2020/11/09 14:21
# !/usr/bin/python3.7
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

    @allure_attach("商品中心明细日报")
    def bns_queryData_report_sku(self, data=None):
        # TODO: 请完成函数注释!!!
        if data is None: data = {"detailDataTime": None, "startMonth": "", "endMonth": "", "fpermissionId": gen_id.get_real_id(first_name='业务日报指标',second_name='商品中心日报'),
                                 "fdataRoleId": gen_id.get_fdataRoleId(), "currentPage": 1, "pageSize": 10,
                                 "fsortName": "", "fsortType": ""}

        # 请求入参

        self.headers['x-requested-with'] = 'true'
        # 请求地址
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/data/data/admin/report/goodsCenter/reportDetail".format(get_data_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("商品中心明细查询接口返回:{}".format(response.json()))
        return response.json()





if __name__ == '__main__':
    a = BnsApi()
    a.bns_queryData_report_sku()
