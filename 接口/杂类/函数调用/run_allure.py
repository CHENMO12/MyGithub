# -*- coding: utf-8 -*
import os
import pytest

pytest.main(['-s', '-q', "./demo_allure.py", '--alluredir', './report/xml'])
cmd = "allure generate ./report/xml -o ./report/html --clean"
os.system(cmd)
