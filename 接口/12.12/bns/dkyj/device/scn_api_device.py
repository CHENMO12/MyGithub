# -*- coding: utf-8 -*-
# @Time : 2019-11-13 14:27:22
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper,TimeHelper,StringHelper
from bns.dkyj.device.bns_api_device import BnsApi
from testdata import gen_bnsData
from bns.dkyj import utils
import json


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_device_add(self, mallAreaCode,deviceCodeOrBar, areaCodesList,headers=None, deviceName=None, res_accurate=False, business_exception=False):
        '''
        :param headers:
        :param deviceCodeOrBar: 设备编码/条码
        :param deviceName: 设备名称
        :param areaCodesList: 挂载节点(区域编码为列表形式)
        :return:
        '''

        self.set_headers("areaCode", "mallAreaCode")
        # 参数化
        if deviceName is None: deviceName = gen_bnsData.random_device_deviceName()

        # 发送业务请求
        res_json = self.bns_device_add( mallAreaCode=mallAreaCode,
                                        headers=headers,
										deviceCodeOrBar=deviceCodeOrBar,
										deviceName=deviceName,
										areaCodesList=areaCodesList,)

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
            if deviceCodeOrBar is not None: info_dict.setdefault('deviceCodeOrBar', deviceCodeOrBar)
            if deviceName is not None: info_dict.setdefault('deviceName', deviceName)
            if areaCodesList is not None: info_dict.setdefault('areaCodesList', areaCodesList)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:绑定设备")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:绑定设备")

    def scn_device_auth(self, deviceCode,data=None,headers=None,res_accurate=False,
                        business_exception=False):
        '''

        :param headers:
        :param deviceCode: 设备编码
        :param data: 数据加密
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        deviceCode = deviceCode

        json_dict = {
            "equno": deviceCode,
            "time": TimeHelper.get_time_from_timestamp(),
            "randCode": StringHelper.random_string(16)
        }

        publicKey = utils.get_publicKey_from_mysql(deviceCode)
        # RSA加密方法
        rsa = utils.RSA()

        data = rsa.rsa_pubkey_encrypt(publicKey, json.dumps(json_dict))

        # 发送业务请求
        res_json = self.bns_device_auth(headers=headers,
                                        deviceCode=deviceCode,
                                        data=data, )

        # 定义一个http状态码的白名单, 如果状态码不在白名单中,则直接返回
        white_list = [200, 201]
        # 获取当前请求的http状态码
        http_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_code")
        # 如果请求返回的状态码不是期望的http状态码, 则直接返回该状态码
        if http_code not in white_list:
            return res_json

        # 提取业务码
        actually_business_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.resultCode")
        # 异常码集合
        exception_list = [
            # 400004,   # 设备类型不合法
        ]

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数
            data = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data")
            res = rsa.rsa_pubkey_decrypt(publicKey, data)  # 解密接口返回的信息

            # 精确返回的内容
            if res_accurate:
                pass
                # return deviceCode

            # 全部信息返回
            info_dict = json.loads(res)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:设备鉴权")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:设备鉴权")

if __name__ == '__main__':
    import config
    api = ScnApi(config.get_dkyj_super_username, config.get_dkyj_super_password)
    # api.scn_device_auth("DJaa556481ee66")
    api.scn_device_add(mallAreaCode="0001-0000-0000",deviceCodeOrBar="DJaa556481ee66",areaCodesList=["0001-0000-0000-0001"])


