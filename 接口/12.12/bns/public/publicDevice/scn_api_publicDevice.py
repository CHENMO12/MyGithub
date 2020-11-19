# -*-coding: utf-8 -*-
#@Time     : 2019/12/12 10:38
#@Author   : zhongqingqing
#@FileName : scn_api_publicDevice.py

from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.public.publicDevice.bns_api_publicDevice import BnsApi
from testdata import gen_bnsData


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_publicDevice_add(self, headers=None, deviceType=None, manufacturerType=None, deviceCode=None,
                          deviceBarCode=None, hardwareVersion=None, lensType=None, res_accurate=False,
                          business_exception=False):

        # 参数化: 默认是店计瑞为,编码长度14,条码长度10
        if deviceType is None: deviceType = 0
        if manufacturerType is None: manufacturerType = 0
        if deviceCode is None: deviceCode = gen_bnsData.random_publicDevice_deviceCode(14)
        if deviceBarCode is None: deviceBarCode = gen_bnsData.random_publicDevice_deviceBarCode(10)
        if hardwareVersion is None: hardwareVersion = gen_bnsData.random_publicDevice_hardwareVersion()
        if lensType is None: lensType = gen_bnsData.random_publicDevice_lensType()

        # 发送业务请求
        res_json = self.bns_publicDevice_add(headers=headers,
                                          deviceType=deviceType,
                                          manufacturerType=manufacturerType,
                                          deviceCode=deviceCode,
                                          deviceBarCode=deviceBarCode,
                                          hardwareVersion=hardwareVersion,
                                          lensType=lensType, )

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
            list_info = self.bns_publicDevice_list(pageNo=1, pageSize=20, deviceCode=deviceCode)
            enale = JsonHelper.parseJson_by_objectpath(list_info, "$..*[@.enable]", res_firstOne=True)
            deviceRegDatetime = JsonHelper.parseJson_by_objectpath(list_info, "$..*[@.createTime]", res_firstOne=True)

            # 精确返回的内容
            if res_accurate:
                pass

            # 全部信息返回
            info_dict = dict()
            if enale is not None: info_dict.setdefault('enale', enale)
            if deviceRegDatetime is not None: info_dict.setdefault('deviceRegDatetime', deviceRegDatetime)
            if deviceType is not None: info_dict.setdefault('deviceType', deviceType)
            if manufacturerType is not None: info_dict.setdefault('manufacturerType', manufacturerType)
            if deviceCode is not None: info_dict.setdefault('deviceCode', deviceCode)
            if deviceBarCode is not None: info_dict.setdefault('deviceBarCode', deviceBarCode)
            if hardwareVersion is not None: info_dict.setdefault('hardwareVersion', hardwareVersion)
            if lensType is not None: info_dict.setdefault('lensType', lensType)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:公共服务注册设备")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:公共服务注册设备")

