# -*- coding: utf-8 -*-
# @Time : 2020-04-26 15:09:32

import pytest
import allure

from case import BaseCase
from bns.b2b.api import Api  # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
import testdata  # 可随机化的简单参数
from case import utils  # 可复用的用例步骤

api_admin = Api(username=None, password=None)


@allure.feature("菜单")
@allure.story("菜单查询")
class TestQuerymenuMenu(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功查询到菜单列表(self):
        # with allure.step('准备用例入参'):

        with allure.step('接口请求'):
            res_info = api_admin.scn_queryMenu_menu(id=None, res_accurate=False, business_exception=False)

        with allure.step('校验:接口响应信息'):
            with allure.step('校验:接口状态码'):
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.retCode")
                actual_msg = JsonHelper.parseJson_by_objectpath(res_info, "$.retMsg")
                expect_code = 200
                expect_msg = "操作成功!"
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)
                self.assert_actual_equal_expect("接口业务码", actual_msg, expect_msg)

        with allure.step('校验:关联业务'):
            # 每个关联业务写成一个step
            pass

        with allure.step('清理用例'):
            pass

    if __name__ == '__main__':
        pytest.main()
