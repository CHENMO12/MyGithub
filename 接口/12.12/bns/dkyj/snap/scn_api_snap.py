# -*- coding: utf-8 -*-
# @Time : 2019-11-19 18:11:30
from base.decorators import api_retry, api_wait
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.dkyj.snap.bns_api_snap import BnsApi
from testdata import gen_bnsData


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_wait()
    def scn_snap_list(self, headers=None, areaCodesList=None, deviceCode=None, deviceType=None, startAgeInit=None, endAgeInit=None, startDateTime=None, endDateTime=None, faceId=None, memberFaceId=None, sexInit=None, snapType=None, userStatus=None, userType=None, pageNo=None, pageSize=None, res_accurate=False, business_exception=False,expected_value=None):
        '''
        功能：抓拍列表查询
        :param headers:
        :param areaCodesList: 节点编码
        :param deviceCode: 设备编码
        :param deviceType: 设备类型
        :param startAgeInit: 开始年龄
        :param endAgeInit: 结束年龄
        :param startDateTime: 开始时间
        :param endDateTime: 结束时间
        :param faceId: 人脸ID
        :param sexInit: 性别,男:0,女:1
        :param snapType: 抓拍类型,0:人脸;3:头肩;5:无特征人脸;6:低质量
        :param userStatus: 客流方向,0:无状态;1:店外徘徊;2:进店;3:店内徘徊;4:出店
        :param userType: 客户类型, 0:普通客户;1:会员,2:店员
        :param pageNo: 页码
        :param pageSize:每页条数
        :param res_accurate:
        :param business_exception:
        :return:
        '''
        
        # 参数化
        if startDateTime is None: startDateTime = gen_bnsData.random_snap_startDateTime()
        if endDateTime is None: endDateTime = gen_bnsData.random_snap_endDateTime()
        if pageNo is None: pageNo = 1
        if pageSize is None: pageSize = 20

        # 发送业务请求
        res_json = self.bns_snap_list(headers=headers,
										areaCodesList=areaCodesList,
										deviceCode=deviceCode,
										deviceType=deviceType,
										startAgeInit=startAgeInit,
										endAgeInit=endAgeInit,
										startDateTime=startDateTime,
										endDateTime=endDateTime,
										faceId=faceId,
										sexInit=sexInit,
										snapType=snapType,
										userStatus=userStatus,
										userType=userType,
										pageNo=pageNo,
										pageSize=pageSize,)
        
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
                return JsonHelper.parseJson_by_objectpath(res_json, "count($.response_data.data.list)")

            # 全部信息返回
            info_dict = dict()
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")
        
        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:抓拍列表查询")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:抓拍列表查询")

    @api_wait(timeout=30,frequency=1)
    def scn_snap_visit_list(self, headers=None, areaCode=None, deviceCodeMix=None, deviceType=None, startAge=None,
                            endAge=None, startDateTime=None, endDateTime=None, memberFaceId=None, faceId=None, sex=None,
                            snapType=None, userStatus=None, userType=None, pageNo=None, pageSize=None,
                            res_accurate=False, business_exception=False, expected_value=None):
        '''
        功能：访客列表查询
        :param headers:
        :param areaCode: 节点编码（仅支持子节点）
        :param deviceCodeMix: 设备编码
        :param deviceType: 设备类型
        :param startAge: 开始年龄
        :param endAge: 结束年龄
        :param startDateTime: 查询开始日期，eg:2019-03-19 12:00:00
        :param endDateTime: 查询结束日期，eg:2019-03-19 12:00:00
        :param memberFaceId: 会员对应人脸ID
        :param faceId: 人脸ID
        :param sex: 性别
        :param snapType: 抓拍类型，0:人脸;3:头肩;5:无特征人脸;6:低质量
        :param userStatus: 客流方向，0:无状态;1:店外徘徊;2:进店;3:店内徘徊;4:出店
        :param userType: 客户类型: 0:普通客户:1:会员;2:店员
        :param pageNo: 当前页，默认是1，eg:1
        :param pageSize: 每页大小，默认每页20条
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        if startDateTime is None: startDateTime = gen_bnsData.random_snap_startDateTime()
        if endDateTime is None: endDateTime = gen_bnsData.random_snap_endDateTime()
        if pageNo is None: pageNo = 1
        if pageSize is None: pageSize = 20

        # 发送业务请求
        res_json = self.bns_snap_visit_list(headers=headers,
                                            areaCode=areaCode,
                                            deviceCodeMix=deviceCodeMix,
                                            deviceType=deviceType,
                                            startAge=startAge,
                                            endAge=endAge,
                                            startDateTime=startDateTime,
                                            endDateTime=endDateTime,
                                            memberFaceId=memberFaceId,
                                            faceId=faceId,
                                            sex=sex,
                                            snapType=snapType,
                                            userStatus=userStatus,
                                            userType=userType,
                                            pageNo=pageNo,
                                            pageSize=pageSize, )

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
                return JsonHelper.parseJson_by_objectpath(res_json, "count($.response_data.data.list)")

            # 全部信息返回
            info_dict = dict()
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:访客列表查询")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:访客列表查询")

if __name__ == '__main__':
    api = ScnApi()
    res = api.scn_snap_visit_list(areaCode="0002-00JY-0000-0001")
    print(res)

