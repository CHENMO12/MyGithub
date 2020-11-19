# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 12:30
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : utils.py

# 将用例可复用的步骤封装成函数
import allure
from base.helper import JsonHelper
from base.helper import AllureHelper
from base.helper import JsonPath

def positive_check_data_response(res_info):
    with allure.step('校验:接口响应信息'):
        with allure.step('校验:接口状态码'):
            actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.code")
            actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.msg")
            expect_code = '200'
            expect_msg = "处理成功"
            expect_data = []
            actual_data = JsonHelper.parseJson_by_objectpath(res_info, "$.data")
            AllureHelper.assert_notEqual("接口业内容", expect_data, actual_data)
            AllureHelper.assert_equal("接口业务码", actual_code, expect_code)
            AllureHelper.assert_equal("接口业消息", actual_msg, expect_msg)

    with allure.step('校验:关联业务'):
        # 每个关联业务写成一个step
        pass

    with allure.step('清理用例'):
        pass


def positive_check_order_response(res_info,order_id):
    with allure.step('校验:接口响应信息'):
        with allure.step('校验:接口状态码'):
            actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.code")
            actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.msg")
            expect_code = '200'
            expect_msg = "处理成功"
            expect_data = order_id
            actual_data = JsonPath.json_path(res_info, "$.data..forderId")[0]
            AllureHelper.assert_equal("接口业内容", expect_data, actual_data)
            AllureHelper.assert_equal("接口业务码", actual_code, expect_code)
            AllureHelper.assert_equal("接口业消息", actual_msg, expect_msg)

    with allure.step('校验:关联业务'):
        # 每个关联业务写成一个step
        pass

    with allure.step('清理用例'):
        pass


def positive_check_afterOrder_response(res_info,order_id):
    with allure.step('校验:接口响应信息'):
        with allure.step('校验:接口状态码'):
            actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.code")
            actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.msg")
            expect_code = '200'
            expect_msg = "处理成功"
            expect_data = order_id
            actual_data = JsonPath.json_path(res_info, "$..fuserSupplierWorkOrder")[0]
            AllureHelper.assert_equal("接口业内容", expect_data, actual_data)
            AllureHelper.assert_equal("接口业务码", actual_code, expect_code)
            AllureHelper.assert_equal("接口业消息", actual_msg, expect_msg)

    with allure.step('校验:关联业务'):
        # 每个关联业务写成一个step
        pass

    with allure.step('清理用例'):
        pass