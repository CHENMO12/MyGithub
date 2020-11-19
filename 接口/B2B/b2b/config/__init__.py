# -*- coding: utf-8 -*-
# @Time    : 2019/10/5 下午 2:48
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : bns_api_device.py

import os

from base.helper import ConfigHelper

cfgFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
domain_cfg = ConfigHelper(cfgFile)

# 读取配置文件内容
try:
    get_b2b_host = os.environ['host']
except:
    get_b2b_host = domain_cfg.get_value("env_test", "b2b_host")



# if data = os.environ['data']
# get_b2b_host = domain_cfg.get_value("env_test", "b2b_host")
get_b2b_username = domain_cfg.get_value("env_test", "b2b_username")
get_b2b_password = domain_cfg.get_value("env_test", "b2b_password")

