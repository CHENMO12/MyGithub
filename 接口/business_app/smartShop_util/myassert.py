# -*- coding: utf-8 -*-
# @Time    : 2019/5/27 14:58
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : myassert.py

import allure
from .mycommon import attachText

def assert_equal(desc_msg,except_var,actual_var):
    with allure.step('结果校验：{}'.format(desc_msg)):
        attachText("", "期望{}：{}".format(desc_msg,except_var))
        attachText("", "实际{}：{}".format(desc_msg,actual_var))
        assert except_var == actual_var
    return (except_var,actual_var)

def assert_notequal(desc_msg,except_var,actual_var):
    with allure.step('结果校验：{}'.format(desc_msg)):
        attachText("", "期望{}：{}".format(desc_msg,except_var))
        attachText("", "实际{}：{}".format(desc_msg,actual_var))
        assert except_var != actual_var
    return (except_var,actual_var)

def assert_isContain(except_var,actual_var):
    desc_msg = "关键信息被包含"
    with allure.step('结果校验：{}'.format(desc_msg)):
        attachText("", "期望关键信息：{}".format(except_var))
        attachText("", "实际输出信息：{}".format(actual_var))
        assert except_var in str(actual_var)

def assert_isNotContain(except_var,actual_var):
    desc_msg = "关键信息不被包含"
    with allure.step('结果校验：{}'.format(desc_msg)):
        attachText("", "期望关键信息：{}".format(except_var))
        attachText("", "实际输出信息：{}".format(actual_var))
        assert except_var not in str(actual_var)


