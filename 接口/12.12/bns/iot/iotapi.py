# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 16:37
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : api.py

from bns.iot.iotDevice import scn_api_iotDevice
from bns.iot.iotUser import scn_api_iotUser


class IotApi(
            scn_api_iotDevice.ScnApi,
            scn_api_iotUser.ScnApi
          ):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)