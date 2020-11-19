# -*- coding: utf-8 -*-
# @Time    : 2019-07-14 23:39:12
# @File    : main.py

import os

import pytest

# 指定需要执行的用例集合
testcase_dir = "case\scene_rank\\test_smoke_cases.py"
# testcase_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + "case"+ os.sep + "scene_rank"
testcase = testcase_dir + os.sep
pytest.main(['-s', '-v', '{}'.format(testcase)])

import time
time.sleep(1)

import os
cmd = "allure generate ./output/report/xml/ -o ./output/report/html --clean"
os.system(cmd)