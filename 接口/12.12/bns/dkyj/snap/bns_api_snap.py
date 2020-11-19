# -*- coding: utf-8 -*-
# @Time : 2019-11-18 17:04:04
from base.decorators import allure_attach
from bns.dkyj import BusinessApi


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_snap = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("抓拍列表查询")
    def bns_snap_list(self, headers=None, areaCodesList=None, deviceCode=None, deviceType=None, startAgeInit=None, endAgeInit=None, startDateTime=None, endDateTime=None, faceId=None, memberFaceId=None, sexInit=None, snapType=None, userStatus=None, userType=None, pageNo=None, pageSize=None):
        '''

        :param headers:
        :param areaCodesList: 商场编码[页面点击选择节点]
        :param deviceCode: 设备编码
        :param deviceType: 设备类型
        :param startAgeInit: 开始年龄
        :param endAgeInit: 结束年龄
        :param startDateTime: 查询开始日期，eg:2019-03-19 12:00:00
        :param endDateTime: 查询结束日期，eg:2019-03-19 12:00:00
        :param faceId: 人脸ID
        :param sexInit: 性别；男：0，女：1
        :param snapType: 抓拍类型，0:人脸;3:头肩;5:无特征人脸;6:低质量
        :param userStatus: 客流方向，0:无状态;1:店外徘徊;2:进店;3:店内徘徊;4:出店
        :param userType: 客户类型: 0:普通客户:1:会员;2:店员
        :param pageNo: 当前页，默认是1，eg:1
        :param pageSize: 每页大小，默认每页20条
        :return:
        '''

        api_info = self._config_snap["list"]
        
        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            "condition": {
            http_data["areaCodesList"]: areaCodesList,
			http_data["deviceCode"]: deviceCode,
			http_data["deviceType"]: deviceType,
			http_data["startAgeInit"]: startAgeInit,
			http_data["endAgeInit"]: endAgeInit,
			http_data["startDateTime"]: startDateTime,
			http_data["endDateTime"]: endDateTime,
			http_data["faceId"]: faceId,
			http_data["sexInit"]: sexInit,
			http_data["snapType"]: snapType,
			http_data["userStatus"]: userStatus,
			http_data["userType"]: userType,
            },
			http_data["pageNo"]: pageNo,
			http_data["pageSize"]: pageSize,
        }
        data = self.base_filter_data(data)
        
        # 请求地址
        response = self.business_request(

            request_url="{}{}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

    @allure_attach("访客列表查询")
    def bns_snap_visit_list(self, headers=None, areaCode=None, deviceCodeMix=None, deviceType=None, startAge=None,
                            endAge=None, startDateTime=None, endDateTime=None, memberFaceId=None, faceId=None, sex=None,
                            snapType=None, userStatus=None, userType=None, pageNo=None, pageSize=None):
        '''

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
        :return:
        '''

        api_info = self._config_snap["visit_list"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            "condition": {
            http_data["areaCode"]: areaCode,
            http_data["deviceCodeMix"]: deviceCodeMix,
            http_data["deviceType"]: deviceType,
            http_data["startAge"]: startAge,
            http_data["endAge"]: endAge,
            http_data["startDateTime"]: startDateTime,
            http_data["endDateTime"]: endDateTime,
            http_data["memberFaceId"]: memberFaceId,
            http_data["faceId"]: faceId,
            http_data["sex"]: sex,
            http_data["snapType"]: snapType,
            http_data["userStatus"]: userStatus,
            http_data["userType"]: userType,
            },
            http_data["pageNo"]: pageNo,
            http_data["pageSize"]: pageSize,
        }
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            request_url="{}{}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

