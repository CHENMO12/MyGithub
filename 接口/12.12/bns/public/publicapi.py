# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 16:37
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : api.py

from bns.public.publicDevice import scn_api_publicDevice
from bns.public.publicDevice import bns_api_publicDevice


class PublicApi(
            scn_api_publicDevice.ScnApi,
            bns_api_publicDevice.BnsApi
          ):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)