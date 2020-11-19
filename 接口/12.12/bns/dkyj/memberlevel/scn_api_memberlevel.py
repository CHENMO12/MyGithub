# -*- coding: utf-8 -*-
# @Time : 2019-11-21 14:24:12
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.dkyj.memberlevel.bns_api_memberlevel import BnsApi
from testdata import gen_bnsData


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_memberlevel_add(self, brandCode, brandId, headers=None, levelName=None, res_accurate=False, business_exception=False):
        '''

        :param headers:
        :param brandCode: 品牌编码
        :param brandId: 品牌id
        :param levelName: 会员级别名称
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        if levelName is None: levelName = gen_bnsData.random_memberlevel_levelName()

        # 发送业务请求
        res_json = self.bns_memberlevel_add(headers=headers,
										brandCode=brandCode,
										brandId=brandId,
										levelName=levelName,)

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
            if brandCode is not None: info_dict.setdefault('brandCode', brandCode)
            if brandId is not None: info_dict.setdefault('brandId', brandId)
            if levelName is not None: info_dict.setdefault('levelName', levelName)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:新增会员级别")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:新增会员级别")