# -*- coding: utf-8 -*-
# @Time : 2019-11-21 15:39:56
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.dkyj.employee.bns_api_employee import BnsApi
from testdata import gen_bnsData
from base.helper import StringHelper


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_employee_add(self, mallareaCode, faceId, imagePath, headers=None,  employeename=None, phoneNo=None, sex=None, age=None, remark=None, res_accurate=False, business_exception=False):
        '''

        :param headers:
        :param mallareaCode: 门店编码
        :param employeename: 店员姓名
        :param phoneNo: 手机号码
        :param faceId: 人脸faceId
        :param imagePath: 图片路径
        :param sex: 性别
        :param age: 年龄
        :param remark: 备注
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        if employeename is None: employeename = gen_bnsData.random_employee_employeename()
        if phoneNo is None: phoneNo = StringHelper.get_random_phoneno()
        if remark is None: remark = gen_bnsData.random_employee_remark()

        # 发送业务请求
        res_json = self.bns_employee_add(headers=headers,
										mallareaCode=mallareaCode,
										employeename=employeename,
										phoneNo=phoneNo,
										faceId=faceId,
										imagePath=imagePath,
										sex=sex,
										age=age,
										remark=remark,)

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
            if employeename is not None: info_dict.setdefault('employeename', employeename)
            if phoneNo is not None: info_dict.setdefault('phoneNo', phoneNo)
            if faceId is not None: info_dict.setdefault('faceId', faceId)
            if imagePath is not None: info_dict.setdefault('imagePath', imagePath)
            if sex is not None: info_dict.setdefault('sex', sex)
            if age is not None: info_dict.setdefault('age', age)
            if remark is not None: info_dict.setdefault('remark', remark)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:新增店员")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:新增店员")