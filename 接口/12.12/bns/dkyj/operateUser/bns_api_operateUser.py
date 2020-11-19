# -*- coding: utf-8 -*-
# @Time : 2019-11-27 16:37:36
from base.decorators import allure_attach
from bns.dkyj import BusinessApi
from base.helper import EncryptHelper



class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_operateUser = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("添加运营用户")
    def bns_operateUser_add(self, headers=None, userName=None, userPhone=None, roleId=None, areaCodesList=None, **kwargs):
        """
        功能：添加一个运营用户
        :param headers:
        :param userName: 用户真实姓名，string，必填
        :param userPhone: 用户手机号，string，必填
        :param roleId: 角色id,  权限对应（2.技术支持 3.数据校正 4.安装人员）
        :param areaCodesList: 角色绑定的区域节点
        :return:
        """
        api_info = self._config_operateUser["add"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        userRolesList = list()
        dict_ele = dict()
        dict_ele.setdefault("roleId", roleId)
        dict_ele.setdefault("areaCodes", areaCodesList)
        userRolesList.append(dict_ele)

        ################### 多组参数逻辑判断 start #####################
        for i in range(2, 1000):

            key1 = "roleId{}".format(i)
            value1 = kwargs.get(key1)
            key2 = "areaCodesList{}".format(i)
            value2 = kwargs.get(key2)

            if value1 and value2:
                dict_ele = dict()
                dict_ele.setdefault("roleId", value1)
                dict_ele.setdefault("areaCodes", value2)
                userRolesList.append(dict_ele)
            else:
                break

        ################### 多组参数逻辑判断 end   #####################
        data = {
            http_data["userName"]: userName,
            http_data["userPhone"]: userPhone,
            "userRoles": userRolesList,
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

    @allure_attach("删除运营用户")
    def bns_operateUser_delete(self, headers=None, userId=None):
        """
        功能: 删除运营用户
        :param headers:
        :param userId: 用户id
        :return:
        """

        api_info = self._config_operateUser["delete"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["userId"]: userId,
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

    @allure_attach("运营用户列表")
    def bns_operateUser_list(self, headers=None, userInfo=None, userRole=None, pageNo=None, pageSize=None):
        """
        功能: 运营用户列表
        :param headers:
        :param userInfo: 用户名字或用户手机号, 支持模糊查询
        :param userRole: 用户角色, 枚举类型: technician,data_correct,install
        :param pageNo: 页码
        :param pageSize: 页大小
        :return:
        """

        api_info = self._config_operateUser["list"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["userInfo"]: userInfo,
            http_data["userRole"]: userRole,
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

    @allure_attach("修改密码")
    def bns_operateUser_modifyPassword(self, headers=None, oldPasswordMd5=None, newPassword=None):
        '''

        :param headers:
        :param oldPasswordMd5: 旧密码，MD5值
        :param newPassword: 新密码
        :return:
        '''

        api_info = self._config_operateUser["modifyPassword"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["oldPasswordMd5"]: oldPasswordMd5,
            http_data["newPassword"]: EncryptHelper.md5(newPassword),
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

    @allure_attach("获取账户权限列表")
    def bns_operateUser_getUserRoleList(self, headers=None):
        '''

        :param headers:
        :return:
        '''

        api_info = self._config_operateUser["getUserRoleList"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
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

    @allure_attach("切换账户权限角色")
    def bns_operateUser_changeUserRole(self, headers=None, userId=None):
        '''

        :param headers:
        :param userId: 账户权限对应的用户ID
        :return:
        '''

        api_info = self._config_operateUser["changeUserRole"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {
            http_data["userId"]: userId,
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


if __name__ == '__main__':
    str = "q23586"
    res = EncryptHelper.md5(str)
    print(res)


