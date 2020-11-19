# -*- coding: utf-8 -*-
# @Time : 2020-04-26 14:53:49
from base.decorators import allure_attach
from bns.b2b import BusinessApi
from config import *
import json
import allure


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @allure_attach("菜单查询")
    def bns_queryMenu_menu(self, id=None):
        # TODO: 请完成函数注释!!!
        data = {"id": id}

        # 请求地址
        # allure.attach(body=data, name="接口请求参数")
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/admin/sso/queryMenu".format(get_b2b_host),
            data=json.dumps(data),
            headers=self.headers
        )

        return response.json()


if __name__ == '__main__':
    a = BnsApi()
    a = a.bns_queryMenu_menu(id=1)
    print(a)
