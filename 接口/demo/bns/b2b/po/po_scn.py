#!/usr/bin/python3.7
# @Time : 2020/5/27 0027 15:44 
# -*- coding: utf-8 -*-
# @Time : 2020-05-27 15:38:50
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.b2b.po.po_bns import BnsApi
from testdata import gen_bnsData


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_po_add(self, headers=None , res_accurate=False, business_exception=False):
        # TODO: 请确定参数并完成参数注释

        # 参数化

        # 发送业务请求
        res_json = self.bns_po_add(headers=headers,
                                   )

        # 定义一个http状态码的白名单, 如果状态码不在白名单中,则直接返回
        white_list = [200, 201]
        # 获取当前请求的http状态码
        http_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_code")
        # 如果请求返回的状态码不是期望的http状态码, 则直接返回该状态码
        if http_code not in white_list:
            return res_json

        # 提取业务码
        actually_business_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")
        # 异常码集合
        exception_list = [
            # 400004,   # 设备类型不合法
        ]

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                pass
                # return deviceCode

            # 全部信息返回
            info_dict = dict()
            # TODO: 请确认,是否需要接收其他必要信息, 如添加后产生的唯一性标识信息

            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:新建采购订单")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:新建采购订单")

