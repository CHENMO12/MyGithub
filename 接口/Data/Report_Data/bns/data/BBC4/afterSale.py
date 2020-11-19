#!/usr/bin/python3.7
# @Time : 2020/11/13 16:08
import json

from base.decorators import allure_attach
from bns.data import BusinessApi
from config import get_data_host
from testdata.gen_id import GenId

gen_id = GenId()


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

        # self._config_queryData = self.base_yaml_info(
        #     curr_file=__file__,
        #     module_key=__name__.split(".")[-2]
        # )


    @allure_attach("BBC4.0订单查询")
    def bns_afterSale_four(self, data=None, forder_id=None):
        # TODO: 请完成函数注释!!!
        if data is None: data = {"fdataRoleId":gen_id.get_fdataRoleId(),"fpermissionId":gen_id.get_real_id(first_name='BBC4.0自助查询服务', second_name='售后订单查询'),"fsortName":"","fsortType":1,"currentPage":1,"pageSize":10,"commonFieldDtoList":[{"ftableAlias":"fao","ffieldName":"forder_aftersale_id","ftype":3,"fstringQuery":""},{"ftableAlias":"fao","ffieldName":"fafter_sale_application_time","ftype":1,"fstartValue":"","fendValue":""},{"ftableAlias":"fao","ffieldName":"faftersale_status_var","ftype":2},{"ftableAlias":"fao","ffieldName":"faftersale_type_var","ftype":2},{"ftableAlias":"fao","ffieldName":"funame","ftype":3,"fstringQuery":""},{"ftableAlias":"fao","ffieldName":"forder_id","ftype":3,"fstringQuery":forder_id},{"ftableAlias":"fao","ffieldName":"fcompany_abbreviation","ftype":3,"fstringQuery":""}],"ffieldNames":["fao.forder_aftersale_id","fao.fafter_sale_application_time","fao.faftersale_status_var","fao.faftersale_type_var","fao.fmerchants_head","fao.faftersale_reason_var","fao.fsku_name","fao.fsku_code","fao.forder_pay_type_var","fao.forder_id","fao.finternational_code","fao.fcompany_name","fao.fcompany_abbreviation","fao.fbrand_name","fao.faftersale_supplier_amount","fao.faftersale_commany_amount"]}
        # 请求入参

        self.headers['x-requested-with'] = 'true'
        # 请求地址
        response = self.session.post(
            # TODO: 请确认url是否需要变化！！！
            url="{}/data/data/admin/order/read/queryData".format(get_data_host),
            data=json.dumps(data),
            headers=self.headers
        )
        self.log.log_info("BBC4.0售后订单接口返回数据:{}".format(response.json()))
        return response.json()


if __name__ == '__main__':
    a = BnsApi()
    a.bns_afterSale_four(forder_id='XS6039440289394165')
