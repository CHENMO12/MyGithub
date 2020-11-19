# -*- coding: utf-8 -*-
# @Time : 2019-11-27 18:32:31
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.dkyj.operateUser.bns_api_operateUser import BnsApi
from testdata import gen_bnsData
from bns.dkyj.utils import *


class ScnApi(BnsApi):
    SET_DEFAULT_PASSWORD = "Dj123456"

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_operateUser_add_techSupport(self, headers=None, userName=None, userPhone=None, res_accurate=False, business_exception=False):
        '''
        功能：运营用户里添加一个技术支持
        :param headers:
        :param userName: 用户姓名
        :param userPhone: 手机号
        :param areaCodesList: 权限对应作用节点
        :return:
        '''

        # 参数化
        if userName is None: userName = gen_bnsData.random_operateUser_userName()
        if userPhone is None: userPhone = gen_bnsData.random_operateUser_userPhone()
        roleId = 2
        areaCodesList = ["0000"]

        # 发送业务请求
        res_json = self.bns_operateUser_add(headers=headers,
										userName=userName,
										userPhone=userPhone,
										roleId=roleId,
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
            userInfo = self.bns_operateUser_list(userInfo=userPhone)
            userId = JsonHelper.parseJson_by_objectpath(userInfo, "$..*[@.id]", res_firstOne=True)
            # 获取密码并修改为默认密码Dj123456
            password_by_md5 = get_md5Password_from_mysql_in_mall(userPhone)
            ScnApi(username=userPhone, password=password_by_md5).scn_operateUser_modifyPassword()
            # 精确返回的内容
            if res_accurate:
                pass
                # return deviceCode

            # 全部信息返回
            info_dict = dict()
            info_dict.setdefault('userId', userId)
            if userName is not None: info_dict.setdefault('userName', userName)
            if userPhone is not None: info_dict.setdefault('userPhone', userPhone)
            if roleId is not None: info_dict.setdefault('roleId', roleId)
            if areaCodesList is not None: info_dict.setdefault('areaCodesList', areaCodesList)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加运营用户")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加运营用户")

    def scn_operateUser_modifyPassword(self, headers=None, oldPasswordMd5=None, newPassword=None, res_accurate=False,
                                       business_exception=False):
        '''
        功能：修改密码
        :param headers:
        :param oldPasswordMd5: 旧密码，MD5值
        :param newPassword: 新密码
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        if oldPasswordMd5 is None:
            oldPasswordMd5 = self.password

        if newPassword is None:
            newPassword = self.SET_DEFAULT_PASSWORD


        # 发送业务请求
        res_json = self.bns_operateUser_modifyPassword(headers=headers,
                                                       oldPasswordMd5=oldPasswordMd5,
                                                       newPassword=newPassword, )

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
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:修改密码")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:修改密码")

    def scn_operateUser_changeUserRole(self, headers=None, userId=None, res_accurate=False, business_exception=False):
        '''

        :param headers:
        :param userId: 账户权限对应的用户ID
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        res = self.bns_operateUser_getUserRoleList()
        userId_list = JsonHelper.parseJson_by_objectpath(res, "$..*['id']")
        if userId is None: userId = userId_list[0]

        # 发送业务请求
        res_json = self.bns_operateUser_changeUserRole(headers=headers,
                                                       userId=userId, )

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
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:切换账户权限角色")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:切换账户权限角色")


if __name__ == '__main__':
    api1 = ScnApi()
    # userPhone = gen_bnsData.random_operateUser_userPhone()
    # api1.scn_operateUser_add_techSupport(userPhone = userPhone)
    # password_by_md5 = get_md5Password_from_mysql_in_mall(userPhone)
    # print("password_by_md5:{}".format(password_by_md5))
    #
    # api=ScnApi(username=userPhone,password=password_by_md5)
    # api.bns_operateUser_modifyPassword(oldPasswordMd5=password_by_md5,newPassword="Dj123456")
    api1.scn_operateUser_add_techSupport()

