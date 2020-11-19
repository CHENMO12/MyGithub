# -*- coding: utf-8 -*-
# @Time : 2019-11-27 15:52:07
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.iot.iotUser.bns_api_iotUser import BnsApi
from testdata import gen_bnsData
from bns.dkyj.utils import *


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_iotUser_add_techSupoort(self, headers=None, userEmail=None, userName=None, userPhone=None, res_accurate=False, business_exception=False):
        '''
        功能：IOT添加一个技术支持人员
        :param headers:
        :param userEmail: 邮箱
        :param userName: 姓名
        :param userPhone: 手机号
        :return:
        '''

        # 参数化
        if userEmail is None: userEmail = gen_bnsData.random_iotUser_userEmail()
        if userName is None: userName = gen_bnsData.random_iotUser_userName()
        if userPhone is None: userPhone = gen_bnsData.random_iotUser_userPhone()
        roleIdsList = [3]

        # 发送业务请求
        res_json = self.bns_iotUser_add(headers=headers,
										userEmail=userEmail,
										userName=userName,
										userPhone=userPhone,
										roleIdsList=roleIdsList,)

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
            userId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.userId")
            # 获取密码
            password_by_md5 = get_md5Password_from_mysql_in_iot(userPhone)
            # 精确返回的内容
            if res_accurate:
                return userPhone

            # 全部信息返回
            info_dict = dict()
            info_dict.setdefault('userId', userId)
            info_dict.setdefault('userPassword', password_by_md5)
            if userEmail is not None: info_dict.setdefault('userEmail', userEmail)
            if userName is not None: info_dict.setdefault('userName', userName)
            if userPhone is not None: info_dict.setdefault('userPhone', userPhone)
            if roleIdsList is not None: info_dict.setdefault('roleIdsList', roleIdsList)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加员工")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加员工")


if __name__ == '__main__':
    api = ScnApi()
    res = api.scn_iotUser_add_techSupoort()
    print(res)