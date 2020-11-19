# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 16:37
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : api.py

from bns.data.BBC3 import bbc3
from bns.data.BBC4 import bbc4 ,afterSale,supplierWorkOrder
from bns.data.Report import report_brand
from bns.data.Report import report_channel
from bns.data.Report import report_sale
from bns.data.Report import report_sku
from bns.data.opt_order import orderList ,overSale,supplieList


class Api(
    bbc3.BnsApi, bbc4.BnsApi, report_sale.BnsApi, report_sku.BnsApi, report_channel.BnsApi,report_brand.BnsApi,orderList.BnsApi,overSale.BnsApi,afterSale.BnsApi,supplieList.BnsApi,supplierWorkOrder.BnsApi

):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)


if __name__ == '__main__':
    a = Api()
