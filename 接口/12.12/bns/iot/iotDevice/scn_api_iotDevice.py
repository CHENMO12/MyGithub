# -*- coding: utf-8 -*-
# @Time : 2019-11-11 18:36:33
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from bns.iot.iotDevice.bns_api_iotDevice import BnsApi
from testdata import gen_bnsData


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    def scn_iotDevice_apply(self, deviceId):
        """
        默认审批者: approver = 1
        :param deviceId: 设备id
        :return:
        """
        # 审批者
        approver = 1
        # 申请删除设备
        applyDesc = gen_bnsData.random_iotDevice_applyDesc()
        self.bns_iotDevice_applyDelete(deviceId=deviceId, applyDesc=applyDesc, approver=approver)
        # 通过 applyDesc 来获取到 applyId
        list_info = self.bns_iotDevice_applyList(pageNo=1, pageSize=20)
        applyId = JsonHelper.parseJson_by_objectpath(list_info, "$..*[@.approvalDesc is '{}'].id".format(applyDesc), res_firstOne=True)
        # 审批通过
        self.bns_iotDevice_handleApply(applyId=applyId, approver=approver, approvalStatus=1, # 通过
                                       approvalSuggestion=gen_bnsData.random_iotDevice_approvalSuggestion())
