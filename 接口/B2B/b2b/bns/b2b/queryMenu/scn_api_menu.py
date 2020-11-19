# -*- coding: utf-8 -*-
# @Time : 2020-04-26 14:53:49
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.b2b.queryMenu.bns_api_menu import BnsApi
import json


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    def scn_queryMenu_menu(self, id=None, res_accurate=False, business_exception=False):
        # TODO: 请确定参数并完成参数注释

        # 参数化
        # if func_param is None: func_param = gen_bnsData.xxx()
        if id is None: id = 1

        # 发送业务请求
        res_json = self.bns_queryMenu_menu(
                                           id=id, )

        # 定义一个http状态码的白名单, 如果状态码不在白名单中,则直接返回
        white_list = [200, 201]

        return res_json




if __name__ == '__main__':
    a=ScnApi()
    B=a.scn_queryMenu_menu()
    print(B)