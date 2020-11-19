#!/usr/bin/python3.7
# @Time : 2020/11/09 15:24
# -*- coding: utf-8 -*-
# @Time : 2020-11-09 11:37:29
import json
import jsonpath
from base.decorators import allure_attach
from base.helper import JsonHelper
from bns.data import BusinessApi
from config import get_data_host


def json_path(res, pattern):
    if isinstance(res, dict):
        try:
            res = jsonpath.jsonpath(res, pattern)
        except:
            raise Exception("pattern({})不正确或res({})为空".format(res, pattern))
        return res
    else:
        raise Exception('不是json字符串')


class GenId(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

        # self._config_queryData = self.base_yaml_info(
        #     curr_file=__file__,
        #     module_key=__name__.split(".")[-2]
        # )

    @allure_attach("获取id")
    def bns_queryData_id(self):
        # TODO: 请完成函数注释!!!

        # 请求入参

        self.headers['x-requested-with'] = 'true'
        # 请求地址
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/sso/operate/sso/admin/permissionrole/nav/queryModuleList".format(get_data_host),
            headers=self.headers
        )
        # self.log.log_info("获取id返回数据:{}".format(response.json()))
        # print(response.json())
        parentModulePermissionId = json_path(response.json(), "$..fpermissionId")[0]
        # print(parentModulePermissionId)
        return parentModulePermissionId

    @allure_attach("获取fpermissionId")
    def get_fpermissionId(self, ):
        self.headers['x-requested-with'] = 'true'
        response = self.session.get(
            # TODO: 请确认url是否需要变化！！！
            url="{}/data/data/admin/querySsoPermision?fpermissionParentId={}".format(get_data_host,
                                                                                     self.bns_queryData_id()),
            headers=self.headers
        )
        return response.json()

    def get_fdataRoleId(self):
        self.headers['x-requested-with'] = 'true'
        # 请求地址
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/data/data/admin/opt/via/queryAdminInfo".format(get_data_host),
            headers=self.headers
        )
        # self.log.log_info("获取id返回数据:{}".format(response.json()))
        fdataRoleId = json_path(response.json(), "$..fdataRoleId")[0]
        # print(type(parentModulePermissionId))
        return fdataRoleId

    def get_real_id(self, first_name=None, second_name=None):
        res = self.get_fpermissionId()
        # real_id = json_path(res,"$.Report_Data.childList.[?(@.fpermissionName == {})]".format(name))
        # 多重过滤
        pattren = "$..[?(@.fpermissionName=='{}')].childList[?(@.fpermissionName=='{}')].fpermissionId".format(
            first_name, second_name)
        real_id = json_path(res, pattren)
        return real_id[0]


if __name__ == '__main__':
    a = GenId()
    data = a.get_real_id(first_name='BBC3.0自助查询服务', second_name='订单查询')

    print(data)
