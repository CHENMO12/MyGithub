#!/usr/bin/python3.7
# @Time : 2020/11/13 16:01
# !/usr/bin/python3.7

import json
from testdata.gen_bnsData import get_now_time
from base.decorators import allure_attach
from bns.data import BusinessApi
from config import get_data_host


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

        # self._config_queryData = self.base_yaml_info(
        #     curr_file=__file__,
        #     module_key=__name__.split(".")[-2]
        # )

    @allure_attach("数据中台售后订单查询")
    def bns_overSale_opt(self, data=None):
        # TODO: 请完成函数注释!!!
        # 已完成的售后订单
        if data is None: data = {"currentPage": 1, "pageSize": 20, "faftersaleStatus": "8"}

        # 请求入参
        self.headers['x-requested-with'] = 'true'
        # 请求地址
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/operate/opt/order/afterSaleOrder/list".format(get_data_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("数据中台售后订单接口返回数据:{}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    a = BnsApi()
    a.bns_overSale_opt()
