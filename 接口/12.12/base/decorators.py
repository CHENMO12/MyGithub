# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 22:10
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : decorators.py

import time
from functools import wraps

from base.helper import AllureHelper
from base.exceptions import DefinedBusinessException, WaitAPITimeoutException


def api_retry(times=3, wait_time=0.2):
    # 场景说明：通过common层的api制造数据时，如果api发生了已知业务异常。有重新请求的机会。
    def warp_func(func):
        @wraps(func)
        def retry(*args, **kwargs):
            # 重试次数
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except DefinedBusinessException:
                    time.sleep(wait_time)
            raise DefinedBusinessException("这个api连续多次执行失败：{}".format(func))

        return retry

    return warp_func


def allure_attach(interface_desc):
    '''
    功能说明：将函数的返回结果添加到allure的attach中。如base层中的方法需要此装饰器
    :param interface_desc: 接口功能描述
    '''

    #
    def warp_func(func):
        def fild_retry(*args, **kwargs):
            res_json = func(*args, **kwargs)
            AllureHelper.attachJson(res_json, "接口信息:{}".format(interface_desc))
            return res_json

        return fild_retry

    return warp_func


def api_wait(timeout=10, frequency=0.5):
    '''
        入参：次数，时间间隔，期望值
        功能描述：在没有达到期望值时，按循环间隔，访问api
    '''

    def warp_func(func):
        def fild_retry(*args, **kwargs):
            end_time = time.time() + timeout
            flag = kwargs.get("res_accurate", None)
            expected_value = 1
            try:
                if kwargs["expected_value"] is not None:
                    expected_value = kwargs["expected_value"]
            except:
                pass
            while True:
                kwargs["res_accurate"] = True
                actual_value = func(*args, **kwargs)
                if actual_value == expected_value:  # 返回值不等于0时再返回接口响应信息，否则就定时查询并校验返回
                    kwargs["res_accurate"] = flag
                    return func(*args, **kwargs)
                time.sleep(frequency)
                if time.time() > end_time:
                    break
            kwargs["res_accurate"] = flag
            return func(*args, **kwargs)
            # raise WaitAPITimeoutException("请求API：{}, 最大等待时间：{}".format(func.__name__, timeout))

        return fild_retry

    return warp_func
