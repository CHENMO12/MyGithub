# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 16:37
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : api.py

from bns.dkyj.node import scn_api_node
from bns.dkyj.device import scn_api_device
from bns.dkyj.snap import scn_api_snap
from bns.dkyj.memberlevel import scn_api_memberlevel
from bns.dkyj.member import scn_api_member
from bns.dkyj.operateUser import scn_api_operateUser

class Api(
          scn_api_node.ScnApi,
          scn_api_device.ScnApi,
          scn_api_snap.ScnApi,
          scn_api_memberlevel.ScnApi,
          scn_api_member.ScnApi,
          scn_api_operateUser.ScnApi,
          ):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)