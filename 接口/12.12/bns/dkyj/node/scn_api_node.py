# -*- coding: utf-8 -*-
# @Time : 2019-11-13 15:43:18
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.dkyj.node.bns_api_node import BnsApi
from testdata import gen_bnsData


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_node_addBrand(self, parentAreaCode=None,headers=None,  brandName=None, ageGroups=None, res_accurate=False, business_exception=False):
        """
        添加品牌节点
        :param parentAreaCode:上级区域编码
        :param headers:
        :param brandName:品牌名称
        :param ageGroups: 年龄分组，例：[(0,2),(3,5),(5,90)]
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        if brandName is None: brandName = gen_bnsData.random_node_brandName()
        if ageGroups is None: ageGroups = [(0,90)]

        # 发送业务请求
        res_json = self.bns_node_addBrand(headers=headers,
										parentAreaCode=parentAreaCode,
										brandName=brandName,
                                        ageGroups=ageGroups)

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
            # 收集响应信息：输入信息或返回信息中提取
            areaId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaId")
            areaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaCode")
            areaType = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaType")
            nodeLevel = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.nodeLevel")

            # 精确返回的内容
            if res_accurate:
                return areaCode

            # 全部信息返回
            info_dict = dict()
            if areaId is not None: info_dict.setdefault('areaId', areaId)
            if areaCode is not None: info_dict.setdefault('areaCode', areaCode)
            if areaType is not None: info_dict.setdefault('areaType', areaType)
            if nodeLevel is not None: info_dict.setdefault('nodeLevel', nodeLevel)
            if parentAreaCode is not None: info_dict.setdefault('parentAreaCode', parentAreaCode)
            if brandName is not None: info_dict.setdefault('brandName', brandName)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加品牌")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加品牌")

    @api_retry()
    def scn_node_addShop(self, headers=None, parentAreaCode=None, shopName=None, province=None, city=None,
                         district=None, clerkSim=None, clerkSimType=None, customerSim=None, customerSimType=None,
                         groupId=None, repeatDate=None, skipTime=None, trailSkipTime=None, res_accurate=False,
                         business_exception=False):
        '''

        :param headers:
        :param parentAreaCode: 添加门店的上级节点区域编码
        :param shopName: 添加门店的名称
        :param province: 省
        :param city: 市
        :param district: 县/区
        :param clerkSim: 店员相似度阈值
        :param clerkSimType: 店员相似度选择(-1表示自定义,0表示低,1表示中,2表示高)
        :param customerSim: 顾客相似度阈值
        :param customerSimType: 顾客相似度选择(-1表示自定义,0表示低,1表示中,2表示高)
        :param groupId: 门店分组编码
        :param repeatDate: 回头客范围(天)
        :param skipTime: 门店去重时间(秒)
        :param trailSkipTime: 门店轨迹去重时间(秒)
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        if shopName is None: shopName = gen_bnsData.random_node_shopName()
        if province is None or city is None or district is None:
            province, city, district = gen_bnsData.get_random_addNode_mallAddr()
        if clerkSimType is None: clerkSimType = 1
        if customerSimType is None: customerSimType = 1
        if repeatDate is None: repeatDate = 30
        if skipTime is None: skipTime = 3600
        if trailSkipTime is None: trailSkipTime = 3600
        if shopName is None: shopName = gen_bnsData.random_node_shopName()

        # 发送业务请求
        res_json = self.bns_node_addShop(headers=headers,
                                         parentAreaCode=parentAreaCode,
                                         shopName=shopName,
                                         province=province,
                                         city=city,
                                         district=district,
                                         clerkSim=clerkSim,
                                         clerkSimType=clerkSimType,
                                         customerSim=customerSim,
                                         customerSimType=customerSimType,
                                         groupId=groupId,
                                         repeatDate=repeatDate,
                                         skipTime=skipTime,
                                         trailSkipTime=trailSkipTime, )

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
            5013
        ]

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            areaId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaId")
            areaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaCode")
            areaType = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaType")
            nodeLevel = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.nodeLevel")
            if res_accurate:
                return areaCode

            # 全部信息返回
            info_dict = dict()
            if areaId is not None: info_dict.setdefault('areaId', areaId)
            if areaCode is not None: info_dict.setdefault('areaCode', areaCode)
            if areaType is not None: info_dict.setdefault('areaType', areaType)
            if nodeLevel is not None: info_dict.setdefault('nodeLevel', nodeLevel)
            if parentAreaCode is not None: info_dict.setdefault('parentAreaCode', parentAreaCode)
            if shopName is not None: info_dict.setdefault('shopName', shopName)
            if clerkSim is not None: info_dict.setdefault('clerkSim', clerkSim)
            if clerkSimType is not None: info_dict.setdefault('clerkSimType', clerkSimType)
            if customerSim is not None: info_dict.setdefault('customerSim', customerSim)
            if customerSimType is not None: info_dict.setdefault('customerSimType', customerSimType)
            if groupId is not None: info_dict.setdefault('groupId', groupId)
            if repeatDate is not None: info_dict.setdefault('repeatDate', repeatDate)
            if skipTime is not None: info_dict.setdefault('skipTime', skipTime)
            if trailSkipTime is not None: info_dict.setdefault('trailSkipTime', trailSkipTime)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加门店")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加门店")

    @api_retry()
    def scn_node_addLogic(self, headers=None, parentAreaCode=None, nodeName=None, logicTypeId=None,
                          skipTime=None, skipType=None, res_accurate=False, business_exception=False):
        '''

        :param headers:
        :param parentAreaCode: 添加节点的上级节点编码
        :param nodeName: 添加节点的名称
        :param logicTypeId: 数据处理逻辑类型id
        :param skipTime: 门店去重时间(秒)
        :param skipType: 去重时间类型(-1表示自定义,0表示门店去重时间)
        :param res_accurate:
        :param business_exception:
        :return:
        '''

        # 参数化
        if nodeName is None: nodeName = gen_bnsData.random_node_nodeName()
        #skipType为0时为取门店去重时间,即skipTime取门店去重时间
        if skipType is None: skipType = 0

        # 发送业务请求
        res_json = self.bns_node_addLogic(headers=headers,
                                          parentAreaCode=parentAreaCode,
                                          nodeName=nodeName,
                                          logicTypeId=logicTypeId,
                                          skipTime=skipTime,
                                          skipType=skipType, )

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
            areaId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaId")
            areaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaCode")
            areaType = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaType")
            nodeLevel = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.nodeLevel")
            # 精确返回的内容
            if res_accurate:
                pass
                # return deviceCode

            # 全部信息返回
            info_dict = dict()
            if areaId is not None: info_dict.setdefault('areaId', areaId)
            if areaCode is not None: info_dict.setdefault('areaCode', areaCode)
            if areaType is not None: info_dict.setdefault('areaType', areaType)
            if nodeLevel is not None: info_dict.setdefault('nodeLevel', nodeLevel)
            if parentAreaCode is not None: info_dict.setdefault('parentAreaCode', parentAreaCode)
            if nodeName is not None: info_dict.setdefault('nodeName', nodeName)
            if logicTypeId is not None: info_dict.setdefault('logicTypeId', logicTypeId)
            if skipTime is not None: info_dict.setdefault('skipTime', skipTime)
            if skipType is not None: info_dict.setdefault('skipType', skipType)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加抓拍子节点")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加抓拍子节点")

    @api_retry()
    def scn_node_addCollect(self, headers=None, parentAreaCode=None, nodeName=None, collectTypeId=None,
                            skipTime=None, skipType=None, res_accurate=False, business_exception=False):
        """
        添加汇总节点
        :param headers:
        :param parentAreaCode: 上级区域编码
        :param nodeName: 节点名称
        :param collectTypeId: 汇总节点类型
        :param skipTime: 门店去重时间
        :param skipType:去重时间类型(-1表示自定义,0表示门店去重时间)
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        if nodeName is None: nodeName = gen_bnsData.random_node_collectNodeName()
        if collectTypeId is None: collectTypeId = 1
        if skipType is None: skipType = 0

        # 发送业务请求
        res_json = self.bns_node_addCollect(headers=headers,
                                            parentAreaCode=parentAreaCode,
                                            nodeName=nodeName,
                                            collectTypeId=collectTypeId,
                                            skipTime=skipTime,
                                            skipType=skipType, )

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
        areaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaCode")
        areaId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaId")
        areaType = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaType")
        parentAreaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.parentAreaCode")
        nodeLevel = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.nodeLevel")
        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                return areaCode

            # 全部信息返回
            info_dict = dict()
            # TODO: 请确认,是否需要接收其他必要信息, 如添加后产生的唯一性标识信息
            if areaCode is not None: info_dict.setdefault('areaCode', areaCode)
            if areaId is not None: info_dict.setdefault('areaId', areaId)
            if areaType is not None: info_dict.setdefault('areaType', areaType)
            if nodeLevel is not None: info_dict.setdefault('nodeLevel', nodeLevel)
            if parentAreaCode is not None: info_dict.setdefault('parentAreaCode', parentAreaCode)
            if nodeName is not None: info_dict.setdefault('nodeName', nodeName)
            if collectTypeId is not None: info_dict.setdefault('collectTypeId', collectTypeId)
            if skipTime is not None: info_dict.setdefault('skipTime', skipTime)
            if skipType is not None: info_dict.setdefault('skipType', skipType)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加汇总子节点")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加汇总子节点")

    @api_retry()
    def scn_node_addFirstPartner(self, headers=None, partnerName=None, res_accurate=False,
                                 business_exception=False):
        """
        添加一级合作方
        :param headers:
        :param partnerName: 合作方名称
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        if partnerName is None: partnerName = gen_bnsData.random_node_firstPartnerName()

        # 发送业务请求
        res_json = self.bns_node_addFirstPartner(headers=headers,
                                                 partnerName=partnerName, )

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
            5013, #区域名称已被使用
        ]

        areaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaCode")
        areaId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaId")
        areaType = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaType")
        parentAreaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.parentAreaCode")
        nodeLevel = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.nodeLevel")

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                return areaCode

            # 全部信息返回
            info_dict = dict()
            if areaCode is not None: info_dict.setdefault('areaCode', areaCode)
            if areaId is not None: info_dict.setdefault('areaId', areaId)
            if areaType is not None: info_dict.setdefault('areaType', areaType)
            if partnerName is not None: info_dict.setdefault('name', partnerName)
            if parentAreaCode is not None: info_dict.setdefault('parentAreaCode', parentAreaCode)
            if nodeLevel is not None: info_dict.setdefault('nodeLevel', nodeLevel)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加一级合作方")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加一级合作方")

    @api_retry()
    def scn_node_addFloor(self, headers=None, parentAreaCode=None, floorName=None, res_accurate=False,
                          business_exception=False):
        """
        添加楼层节点
        :param headers:
        :param parentAreaCode:上级区域编码
        :param floorName: 楼层名称
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        if floorName is None: floorName = gen_bnsData.random_node_floorName()

        # 发送业务请求
        res_json = self.bns_node_addFloor(headers=headers,
                                          parentAreaCode=parentAreaCode,
                                          floorName=floorName, )

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
        areaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaCode")
        areaId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaId")
        areaType = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaType")
        nodeLevel = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.nodeLevel")
        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                return areaCode

            # 全部信息返回
            info_dict = dict()
            if parentAreaCode is not None: info_dict.setdefault('parentAreaCode', parentAreaCode)
            if floorName is not None: info_dict.setdefault('floorName', floorName)
            if areaCode is not None: info_dict.setdefault('areaCode', areaCode)
            if areaId is not None: info_dict.setdefault('areaId', areaId)
            if areaType is not None: info_dict.setdefault('areaType', areaType)
            if nodeLevel is not None: info_dict.setdefault('nodeLevel', nodeLevel)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加楼层")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加楼层")

    @api_retry()
    def scn_node_addSecondPartner(self, headers=None, parentAreaCode=None, partnerName=None, res_accurate=False,
                                  business_exception=False):
        """
        添加二级合作方
        :param headers:
        :param parentAreaCode:上级区域编码
        :param partnerName:合作方名称
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        if partnerName is None: partnerName = gen_bnsData.random_node_secondPartnerName()

        # 发送业务请求
        res_json = self.bns_node_addSecondPartner(headers=headers,
                                                  parentAreaCode=parentAreaCode,
                                                  partnerName=partnerName, )

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
        areaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaCode")
        areaId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaId")
        areaType = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaType")
        parentAreaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.parentAreaCode")
        nodeLevel = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.nodeLevel")

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                return areaCode

            # 全部信息返回
            info_dict = dict()
            if areaCode is not None: info_dict.setdefault('areaCode', areaCode)
            if areaId is not None: info_dict.setdefault('areaId', areaId)
            if areaType is not None: info_dict.setdefault('areaType', areaType)
            if partnerName is not None: info_dict.setdefault('name', partnerName)
            if parentAreaCode is not None: info_dict.setdefault('parentAreaCode', parentAreaCode)
            if nodeLevel is not None: info_dict.setdefault('nodeLevel', nodeLevel)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加二级合作方")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加二级合作方")

    @api_retry()
    def scn_node_addThirdPartner(self, headers=None, parentAreaCode=None, partnerName=None, res_accurate=False,
                                 business_exception=False):
        """
        添加三级合作方
        :param headers:
        :param parentAreaCode:上级区域编码
        :param partnerName: 合作方名称
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        if partnerName is None: partnerName = gen_bnsData.random_node_thirdPartnerName()

        # 发送业务请求
        res_json = self.bns_node_addThirdPartner(headers=headers,
                                                 parentAreaCode=parentAreaCode,
                                                 partnerName=partnerName, )

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

        areaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaCode")
        areaId = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaId")
        areaType = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.areaType")
        name = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.name")
        parentAreaCode = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.parentAreaCode")
        nodeLevel = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.data.nodeLevel")

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                return areaCode

            # 全部信息返回
            info_dict = dict()
            if areaCode is not None: info_dict.setdefault('areaCode', areaCode)
            if areaId is not None: info_dict.setdefault('areaId', areaId)
            if areaType is not None: info_dict.setdefault('areaType', areaType)
            if name is not None: info_dict.setdefault('name', name)
            if parentAreaCode is not None: info_dict.setdefault('parentAreaCode', parentAreaCode)
            if nodeLevel is not None: info_dict.setdefault('nodeLevel', nodeLevel)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:添加三级合作方")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:添加三级合作方")

    @api_retry()
    def scn_node_detail(self, headers=None, areaCode=None, res_accurate=False, business_exception=False):
        """
        区域详情
        :param headers:
        :param areaCode:区域编码
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        # if func_param is None: func_param = gen_bnsData.xxx()

        # 发送业务请求
        res_json = self.bns_node_detail(headers=headers,
                                        areaCode=areaCode, )

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
                raise DefinedBusinessException("接口已知业务异常:区域详情")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:区域详情")

    @api_retry()
    def scn_node_list(self, headers=None, parentAreaCode=None, name=None, nodeLevel=None, pageNo=None, pageSize=None,
                      res_accurate=False, business_exception=False):
        """
        获取抓拍列表
        :param headers:
        :param parentAreaCode: 上级节点编码
        :param name: 节点名称
        :param nodeLevel: 节点等级
        :param pageNo: 页码
        :param pageSize: 每页展示数量
        :param res_accurate:
        :param business_exception:
        :return:
        """
        # 参数化
        if pageNo is None: pageNo = 1
        if pageSize is None: pageSize = 10

        # 发送业务请求
        res_json = self.bns_node_list(headers=headers,
                                      parentAreaCode=parentAreaCode,
                                      name=name,
                                      nodeLevel=nodeLevel,
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
                pass
                # return deviceCode

            # 全部信息返回
            info_dict = dict()
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:区域列表")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:区域列表")

    @api_retry()
    def scn_node_tree(self, headers=None, parentAreaCode=None, areaType=None, expandAll=None, includeParentNode=None,
                      name=None, nodeLevel=None, provinceCity=None, res_accurate=False, business_exception=False):
        """
        获取节点树
        :param headers:
        :param parentAreaCode:上级区域编码
        :param areaType: 节点类型
        :param expandAll: 是否展开所有节点，可选
        :param includeParentNode: 是否包含父级节点，可选，默认不包含
        :param name: 节点名称
        :param nodeLevel: 区域级别
        :param provinceCity: 区域位置-省市
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        # if func_param is None: func_param = gen_bnsData.xxx()

        # 发送业务请求
        res_json = self.bns_node_tree(headers=headers,
                                      parentAreaCode=parentAreaCode,
                                      areaType=areaType,
                                      expandAll=expandAll,
                                      includeParentNode=includeParentNode,
                                      name=name,
                                      nodeLevel=nodeLevel,
                                      provinceCity=provinceCity, )

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
                raise DefinedBusinessException("接口已知业务异常:节点树")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:节点树")

    @api_retry()
    def scn_node_treeGroup(self, headers=None, parentAreaCode=None, areaType=None, expandAll=None,
                           includeParentNode=None, name=None, nodeLevel=None, provinceCity=None, res_accurate=False,
                           business_exception=False):
        """
        获取节点树(带节点分组)
        :param headers:
        :param parentAreaCode:上级区域编码
        :param areaType: 节点类型
        :param expandAll: 是否展开所有节点，可选
        :param includeParentNode: 是否包含父级节点，可选，默认不包含
        :param name: 节点名称
        :param nodeLevel: 区域级别
        :param provinceCity: 区域位置-省市
        :param res_accurate:
        :param business_exception:
        :return:
        """

        # 参数化
        # if func_param is None: func_param = gen_bnsData.xxx()

        # 发送业务请求
        res_json = self.bns_node_treeGroup(headers=headers,
                                           parentAreaCode=parentAreaCode,
                                           areaType=areaType,
                                           expandAll=expandAll,
                                           includeParentNode=includeParentNode,
                                           name=name,
                                           nodeLevel=nodeLevel,
                                           provinceCity=provinceCity, )

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
                raise DefinedBusinessException("接口已知业务异常:节点树")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:节点树")


if __name__ == '__main__':
    from bns.dkyj.api import Api

    api_admin = Api(username=None, password=None)

    res_json = api_admin.scn_node_addShop(parentAreaCode="0005-0001")
    print(res_json)
