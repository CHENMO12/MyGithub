# -*- coding: utf-8 -*-
# @Time : 2019-11-21 14:47:11
from base.decorators import api_retry, api_wait
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.dkyj.member.bns_api_member import BnsApi
from testdata import gen_bnsData
from base.helper import StringHelper


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_member_add(self, mallareaCode, faceId, imagePath, headers=None, membername=None, phoneNo=None, membercardNo=None, memberlevelId=None, sex=None, age=None, res_accurate=False, business_exception=False):
        '''
        功能：注册会员
        :param headers:
        :param mallareaCode: 门店编码
        :param membername: 会员姓名
        :param phoneNo: 手机号
        :param membercardNo: 会员卡号
        :param memberlevelId: 会员级别Id
        :param faceId: 人脸Id
        :param imagePath: 注册图片的地址
        :param sex: 性别
        :param age: 年龄
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        if membername is None: membername = gen_bnsData.random_member_membername()
        if phoneNo is None: phoneNo = StringHelper.get_random_phoneno()
        if membercardNo is None: membercardNo = gen_bnsData.get_member_membercardNo()

        # 发送业务请求
        res_json = self.bns_member_add(headers=headers,
										mallareaCode=mallareaCode,
										membername=membername,
										phoneNo=phoneNo,
										membercardNo=membercardNo,
										memberlevelId=memberlevelId,
										faceId=faceId,
										imagePath=imagePath,
										sex=sex,
										age=age,)

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
            if mallareaCode is not None: info_dict.setdefault('mallareaCode', mallareaCode)
            if membername is not None: info_dict.setdefault('membername', membername)
            if phoneNo is not None: info_dict.setdefault('phoneNo', phoneNo)
            if membercardNo is not None: info_dict.setdefault('membercardNo', membercardNo)
            if memberlevelId is not None: info_dict.setdefault('memberlevelId', memberlevelId)
            if faceId is not None: info_dict.setdefault('faceId', faceId)
            if imagePath is not None: info_dict.setdefault('imagePath', imagePath)
            if sex is not None: info_dict.setdefault('sex', sex)
            if age is not None: info_dict.setdefault('age', age)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:新增会员")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:新增会员")

    @api_wait()
    def scn_member_status(self, headers=None, shopAreaCode=None, faceId=None, userType=None, res_accurate=False,
                          business_exception=False, expected_value=None):
        '''
        功能：注册状态查询
        :param headers:
        :param shopAreaCode: 门店编码
        :param faceId: 人脸ID
        :param userType: 用户类型(1:会员;2:店员)
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        # if func_param is None: func_param = gen_bnsData.xxx()

        # 发送业务请求
        res_json = self.bns_member_status(headers=headers,
                                          shopAreaCode=shopAreaCode,
                                          faceId=faceId,
                                          userType=userType, )

        # 定义一个http状态码的白名单, 如果状态码不在白名单中,则直接返回
        white_list = [200, 201]
        # 获取当前请求的http状态码
        http_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_code")
        # 如果请求返回的状态码不是期望的http状态码, 则直接返回该状态码
        if http_code not in white_list:
            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data")

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
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:查询注册状态")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:查询注册状态")

if __name__ == '__main__':
    api=ScnApi()
    res = api.scn_member_status(shopAreaCode="0002-00L0-0000", faceId="252345069741281280", userType=1, expected_value=True)
    print(res)
