import allure
import pytest
import os
import json


@allure.feature('test_module_01')
@allure.story('简单校验')
@allure.description("用例详细描述")
@allure.step('步骤说明')
def test_case_01():
    """
    用例描述：Test case 01
    """
    with allure.step('校验:接口响应信息'):
        pass
    data = {'a': 111, '1': '333', '21': [1, 2, 3]}
    format_data = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)  # 美化json格式
    allure.attach(str(data), '接口请求信息:11111', allure.attachment_type.JSON)

    assert 1 == 1


@allure.feature('test_module_02')
@allure.story('简单校验')
@allure.description("用例详细描述")
@allure.step('步骤说明')
def test_case_02():
    """
    用例描述：Test case 02
    """

    paras = "这是用例参数"
    assert 0 == 0
    allure.attach("用例参数", "{0}".format(paras))

# if __name__ == '__main__':
#     pytest.main(['-s', '-q', "demo_allure.py", '--alluredir', './report/xml'])
#
#
#     cmd = "allure generate ./report/xml/ -o ./report/html --clean"
#     os.popen(cmd)
