# -*- coding: utf-8 -*-
# @Time : 2019-11-13 15:43:18
from base.decorators import allure_attach
from bns.dkyj import BusinessApi


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_node = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("添加品牌")
    def bns_node_addBrand(self,headers=None,parentAreaCode=None, brandName=None, ageGroups=None):
        '''
        添加品牌
        :param headers:
        :param parentAreaCode: 添加品牌的上级节点
        :param brandName:添加品牌的名称
        :param ageGroups: 年龄分组，例：[(0,2),(3,5),(5,90)]
        :return:
        '''

        api_info = self._config_node["addBrand"]
        
        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]
        ageGroupsList = []
        if ageGroups is not None:
            for group in ageGroups:
                ageGroup = {}
                if group[0] is not None:
                    ageGroup["ageMin"] = group[0]
                if group[1] is not None:
                    ageGroup["ageMax"] = group[1]
                ageGroupsList.append(ageGroup)
        
        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
			http_data["brandName"]: brandName,
			http_data["ageGroups"]: ageGroupsList,
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

    @allure_attach("添加门店")
    def bns_node_addShop(self, headers=None, parentAreaCode=None, shopName=None, province=None, city=None,
                         district=None, clerkSim=None, clerkSimType=None, customerSim=None, customerSimType=None,
                         groupId=None, repeatDate=None, skipTime=None, trailSkipTime=None):
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
           :return:
           '''

        api_info = self._config_node["addShop"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
            http_data["shopName"]: shopName,
            http_data["province"]: province,
            http_data["city"]: city,
            http_data["district"]: district,
            http_data["clerkSim"]: clerkSim,
            http_data["clerkSimType"]: clerkSimType,
            http_data["customerSim"]: customerSim,
            http_data["customerSimType"]: customerSimType,
            http_data["groupId"]: groupId,
            http_data["repeatDate"]: repeatDate,
            http_data["skipTime"]: skipTime,
            http_data["trailSkipTime"]: trailSkipTime,
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

    @allure_attach("添加抓拍子节点")
    def bns_node_addLogic(self, headers=None, parentAreaCode=None, nodeName=None, logicTypeId=None, skipTime=None,
                          skipType=None):
        '''

        :param headers:
        :param parentAreaCode: 添加节点的上级节点编码
        :param nodeName: 添加节点的名称
        :param logicTypeId: 数据处理逻辑类型id
        :param skipTime: 门店去重时间(秒)
        :param skipType: 去重时间类型(-1表示自定义,0表示门店去重时间)

        :return:
        '''

        api_info = self._config_node["addLogic"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
            http_data["nodeName"]: nodeName,
            http_data["logicTypeId"]: logicTypeId,
            http_data["skipTime"]: skipTime,
            http_data["skipType"]: skipType,
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

    @allure_attach("删除节点")
    def bns_node_delete(self, headers=None, areaCode=None):
        '''

        :param headers:
        :param areaCode: 节点编码
        :return:
        '''

        api_info = self._config_node["delete"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["areaCode"]: areaCode,
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


    @allure_attach("添加汇总子节点")
    def bns_node_addCollect(self, headers=None, parentAreaCode=None, nodeName=None, collectTypeId=None, skipTime=None,
                            skipType=None):
        """
        添加汇总子节点
        :param headers:
        :param parentAreaCode:上级区域编码
        :param nodeName:节点名称
        :param collectTypeId:汇总类型
        :param skipTime:门店去重时间
        :param skipType:去重时间类型（-1表示自定义，0表示门店去重时间）
        :return:
        """

        api_info = self._config_node["addCollect"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
            http_data["nodeName"]: nodeName,
            http_data["collectTypeId"]: collectTypeId,
            http_data["skipTime"]: skipTime,
            http_data["skipType"]: skipType,
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

    @allure_attach("添加一级合作方")
    def bns_node_addFirstPartner(self, headers=None, partnerName=None):
        """
        添加一级合作方
        :param headers:
        :param parentAreaCode:上级区域编码
        :param partnerName: 合作方名称
        :return:
        """

        api_info = self._config_node["addFirstPartner"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["partnerName"]: partnerName,
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

    @allure_attach("添加楼层")
    def bns_node_addFloor(self, headers=None, parentAreaCode=None, floorName=None):
        """
        添加楼层
        :param headers:
        :param parentAreaCode:上级区域编码
        :param floorName:楼层名称
        :return:
        """

        api_info = self._config_node["addFloor"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
            http_data["floorName"]: floorName,
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

    @allure_attach("添加二级合作方")
    def bns_node_addSecondPartner(self, headers=None, parentAreaCode=None, partnerName=None):
        """
        添加二级合作方
        :param headers:
        :param parentAreaCode:上级区域编码
        :param partnerName: 合作方名称
        :return:
        """

        api_info = self._config_node["addSecondPartner"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
            http_data["partnerName"]: partnerName,
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


    @allure_attach("添加三级合作方")
    def bns_node_addThirdPartner(self, headers=None, parentAreaCode=None, partnerName=None):
        """
        添加三级合作方
        :param headers:
        :param parentAreaCode:上级区域编码
        :param partnerName: 合作方名称
        :return:
        """

        api_info = self._config_node["addThirdPartner"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
            http_data["partnerName"]: partnerName,
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

    @allure_attach("编辑汇总子节点")
    def bns_node_editCollect(self, headers=None, areaCode=None, nodeName=None, collectTypeId=None, skipTime=None,
                             skipType=None):
        """
        编辑汇总节点
        :param headers:
        :param areaCode:汇总节点编码
        :param nodeName: 节点名称
        :param collectTypeId:汇总节点类型id
        :param skipTime: 门店去重时间
        :param skipType: 去重时间类型(-1表示自定义,0表示门店去重时间)
        :return:
        """

        api_info = self._config_node["editCollect"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["areaCode"]: areaCode,
            http_data["nodeName"]: nodeName,
            http_data["collectTypeId"]: collectTypeId,
            http_data["skipTime"]: skipTime,
            http_data["skipType"]: skipType,
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

    @allure_attach("编辑抓拍子节点")
    def bns_node_editLogic(self, headers=None, areaCode=None, nodeName=None, logicTypeId=None, skipTime=None,
                           skipType=None):
        """
        编辑抓拍子节点
        :param headers:
        :param areaCode: 节点区域编码
        :param nodeName: 节点名称
        :param logicTypeId: 节点类型id
        :param skipTime: 门店去重时间
        :param skipType: 去重时间类型(-1表示自定义,0表示门店去重时间)
        :return:
        """
        api_info = self._config_node["editLogic"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["areaCode"]: areaCode,
            http_data["nodeName"]: nodeName,
            http_data["logicTypeId"]: logicTypeId,
            http_data["skipTime"]: skipTime,
            http_data["skipType"]: skipType,
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

    @allure_attach("编辑无配置节点")
    def bns_node_editPartnerBrandFloor(self, headers=None, areaCode=None, nodeName=None):
        """
        编辑无配置节点
        :param headers:
        :param areaCode: 节点区域编码
        :param nodeName: 节点名称
        :return:
        """

        api_info = self._config_node["editPartnerBrandFloor"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["areaCode"]: areaCode,
            http_data["nodeName"]: nodeName,
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

    @allure_attach("编辑门店节点")
    def bns_node_editShop(self, headers=None, areaCode=None, shopName=None, province=None, city=None, district=None,
                          clerkSim=None, clerkSimType=None, customerSim=None, customerSimType=None, groupId=None,
                          repeatRange=None, skipTime=None, trailSkipTime=None):
        """
        编辑门店节点
        :param headers:
        :param areaCode: 门店区域编码
        :param shopName: 门店名称
        :param province: 区域位置-省
        :param city: 区域位置-市
        :param district: 区域位置-区
        :param clerkSim:店员相似度
        :param clerkSimType:店员相似度类型（-1表示自定义，0表示低，1表示中，2表示高）
        :param customerSim:顾客相似度
        :param customerSimType:顾客相似度类型（-1表示自定义，0表示低，1表示中，2表示高）
        :param groupId:门店分组编码
        :param repeatRange:回头客识别天数
        :param skipTime:
        :param trailSkipTime:
        :return:
        """

        api_info = self._config_node["editShop"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["areaCode"]: areaCode,
            http_data["shopName"]: shopName,
            http_data["province"]: province,
            http_data["city"]: city,
            http_data["district"]: district,
            http_data["clerkSim"]: clerkSim,
            http_data["clerkSimType"]: clerkSimType,
            http_data["customerSim"]: customerSim,
            http_data["customerSimType"]: customerSimType,
            http_data["groupId"]: groupId,
            http_data["repeatRange"]: repeatRange,
            http_data["skipTime"]: skipTime,
            http_data["trailSkipTime"]: trailSkipTime,
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

    @allure_attach("区域详情")
    def bns_node_detail(self, headers=None, areaCode=None):
        """
        获取区域详情
        :param headers:
        :param areaCode:区域编码
        :return:
        """

        api_info = self._config_node["detail"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["areaCode"]: areaCode,
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

    @allure_attach("区域列表")
    def bns_node_list(self, headers=None, parentAreaCode=None, name=None, nodeLevel=None, pageNo=None, pageSize=None):
        """
        获取区域列表
        :param headers:
        :param parentAreaCode: 父节点编码
        :param name: 节点名称
        :param nodeLevel: 节点级别
        :param pageNo:页码
        :param pageSize:每页数据量
        :return:
        """

        api_info = self._config_node["list"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]
        # 请求入参
        data = {
            "condition":{
            },
            http_data["pageNo"]: pageNo,
            http_data["pageSize"]: pageSize,
        }
        if parentAreaCode is not None:data["condition"][http_data["parentAreaCode"]] = parentAreaCode
        if name is not None:data["condition"][http_data["name"]] = name
        if nodeLevel is not None:data["condition"][http_data["nodeLevel"]] = nodeLevel
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

    @allure_attach("节点树")
    def bns_node_tree(self, headers=None, parentAreaCode=None, areaType=None, expandAll=None, includeParentNode=None,
                      name=None, nodeLevel=None, provinceCity=None):
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

        api_info = self._config_node["tree"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
            http_data["areaType"]: areaType,
            http_data["expandAll"]: expandAll,
            http_data["includeParentNode"]: includeParentNode,
            http_data["name"]: name,
            http_data["nodeLevel"]: nodeLevel,
            http_data["provinceCity"]: provinceCity,
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

    @allure_attach("节点树")
    def bns_node_treeGroup(self, headers=None, parentAreaCode=None, areaType=None, expandAll=None,
                           includeParentNode=None, name=None, nodeLevel=None, provinceCity=None):
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

        api_info = self._config_node["treeGroup"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["parentAreaCode"]: parentAreaCode,
            http_data["areaType"]: areaType,
            http_data["expandAll"]: expandAll,
            http_data["includeParentNode"]: includeParentNode,
            http_data["name"]: name,
            http_data["nodeLevel"]: nodeLevel,
            http_data["provinceCity"]: provinceCity,
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

