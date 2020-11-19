# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 16:37
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : api.py

from bns.b2b.queryMenu.scn_api_menu import ScnApi
from bns.b2b.po.bns_api_po import BnsApi_Po
from bns.b2b.so import bns_api_so
from bns.b2b.stock import bns_api_stock
from bns.b2b.center import bns_api_center


class Api(
    ScnApi, BnsApi_Po, bns_api_so.BnsApi_So, bns_api_center.BnsApi, bns_api_stock.BnsApi

):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)


if __name__ == '__main__':
    a = Api()
