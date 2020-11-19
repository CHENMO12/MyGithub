# -*- coding: utf-8 -*-
# @Time    : 2019/7/5 11:24
# @Author  : Huizi Cai
import os
import sys
import pytest
from business_app._config.config import Config
cfg = Config()

if len(sys.argv) != 1:
    web_domain = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    device = sys.argv[4]

    cfg.set_conf(Config.ENV_TEST,Config.VALUE_WEB_DOMAIN,web_domain)
    cfg.set_conf(Config.ENV_TEST,Config.VALUE_USERNAME,username)
    cfg.set_conf(Config.ENV_TEST,Config.VALUE_PASSWORD,password)
    cfg.set_conf(Config.ENV_TEST,Config.VALUE_DEVICE,device)

pytest.main(['-s', '-q', "./_testcase/interface_testcase.py", '--alluredir', './report/xml'])
pytest.main(['-s', '-q', "./_testcase/business_testcase.py", '--alluredir', './report/xml'])
pytest.main(['-s', '-q', "./_testcase/advanced_testcase.py", '--alluredir', './report/xml'])
cmd = "allure generate ./report/xml/ -o ./report/html --clean"
os.popen(cmd)