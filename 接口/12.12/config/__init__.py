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
get_iot_web_domain = domain_cfg.get_value("env_test", "iot_web_domain")
get_iot_super_username = domain_cfg.get_value("env_test", "iot_super_username")
get_iot_super_password = domain_cfg.get_value("env_test", "iot_super_password")
get_dkyj_web_domain = domain_cfg.get_value("env_test", "dkyj_web_domain")
get_dkyj_super_username = domain_cfg.get_value("env_test", "dkyj_super_username")
get_dkyj_super_password = domain_cfg.get_value("env_test", "dkyj_super_password")
get_db_host = domain_cfg.get_value("env_test", "db_host")
get_db_username = domain_cfg.get_value("env_test", "db_username")
get_db_password = domain_cfg.get_value("env_test", "db_password")
get_upload_host = domain_cfg.get_value("env_test", "upload_host")
get_upload_port = domain_cfg.get_value("env_test", "upload_port")
get_upload_port_auth = domain_cfg.get_value("env_test", "upload_port_auth")

