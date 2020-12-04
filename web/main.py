# -*- coding: utf-8 -*-
# ! /usr/bin/python3.7
# @Time : 2020/12/04 10:13

import os

import pytest

# 指定需要执行的用例集合
testcase_dir = "case\data.py"
# testcase_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + "case"+ os.sep + "scene_rank"
testcase = testcase_dir + os.sep
pytest.main(['-s', '-v', '{}'.format(testcase)])
