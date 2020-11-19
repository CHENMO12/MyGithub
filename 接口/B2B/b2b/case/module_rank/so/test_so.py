#!/usr/bin/python3.7
# @Time : 2020/5/6 0006 10:33
import pytest
import allure
from case import BaseCase
from bns.b2b.api import Api    # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
api_admin = Api(username=None,password=None)


@allure.feature("销售订单")
@allure.story("新建销售订单审批")
class TestPO(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_新建销售订单提交审批(self):
        # with allure.step('准备用例入参'):

        with allure.step('接口请求'):
            api_admin.bns_new_so_add()
            api_admin.bns_so_submitSaleOrder()
            res_info = api_admin.bns_so_saleOrderApprove()

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