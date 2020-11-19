# -*- coding: utf-8 -*-
# @Time    : 2019/9/30 0030 上午 10:26
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : bns_api_device.py
import os
import re

import allure

from base.exceptions import ParameterizeFunctionException, CsvContentException
from base.helper import AllureHelper, TimeHelper, FileHelper, YamlHelper, CsvHelper, PROJECT_ROOT
from base import validator, exceptions
from bns import BaseApi
from base import validator
import testdata


class BaseCase:

    def csv_info(self, csv_file=None, curr_file=None):
        """
        功能: 将csv文件转为列表
        :param csv_file: csv文件
        :param curr_file: 默认填写__file__
        :return:
        """

        if not csv_file:
            curr_dir = os.path.dirname(curr_file)
            csv_file_list = FileHelper.get_files_from_folderOrFolderlist(curr_dir, ".csv", recursive=False)
            if len(csv_file_list) == 1:
                csv_file = csv_file_list[0]
            elif len(csv_file_list) == 0:
                raise exceptions.FileException("当前目录下不存在csv文件：{}".format(curr_dir))
            else:
                raise exceptions.FileException("当前目录下存在多个csv文件，请明确指明csv路径，：{}".format(curr_dir))

        validator.check_file_isFile(csv_file)

        info_list = CsvHelper.load_csv_file(csv_file)

        return info_list

    def assert_actual_contain_expect(self, desc_msg, actual_value, expect_value):
        """
        断言方法：expect_value被actual_value包含
        :param desc_msg: 对expect_value的一个解释说明(描述下期望值的具体含义)
        :param actual_var: 实际值
        :param expect_var: 期望值
        """

        if not isinstance(actual_value, str):
            actual_value = str(actual_value)

        if not isinstance(expect_value, str):
            expect_value = str(expect_value)

        validator.check_paramType_str(desc_msg, expect_value, actual_value)

        with allure.step('[断言校验]实际值包含期望值：{}'.format(desc_msg)):
            AllureHelper.attachText("", "实际值：{}".format(actual_value))
            AllureHelper.attachText("", "期望值：{}".format(expect_value))
            assert expect_value in actual_value

    def assert_actual_notContain_expect(self, desc_msg, actual_value, expect_value):
        """
        断言方法：expect_value不被actual_value包含
        :param desc_msg: 对不期望被包含内容的一个解释说明
        :param actual_var: 实际值
        :param expect_var: 期望值
        """

        if not isinstance(actual_value, str):
            actual_value = str(actual_value)

        if not isinstance(expect_value, str):
            expect_value = str(expect_value)

        validator.check_paramType_str(desc_msg, expect_value, actual_value)

        with allure.step('[断言校验]实际值不包含期望值：{}'.format(desc_msg)):
            AllureHelper.attachText("", "实际值：{}".format(actual_value))
            AllureHelper.attachText("", "期望值：{}".format(expect_value))
            assert expect_value not in actual_value

    def assert_actual_equal_expect(self, desc_msg, actual_value, expect_value):
        """
        断言方法：expect_value等于actual_value
        :param desc_msg: 需要校验的值
        :param actual_var: 实际值
        :param expect_var: 期望值
        """

        validator.check_paramType_str(desc_msg)

        if type(actual_value) != type(expect_value):
            actual_value = str(actual_value)
            expect_value = str(expect_value)

        with allure.step('[断言校验]实际值等于期望值：{}'.format(desc_msg)):
            AllureHelper.attachText("", "实际值：{}".format(actual_value))
            AllureHelper.attachText("", "期望值：{}".format(expect_value))
            assert expect_value == actual_value

    def assert_actual_notEqual_expect(self, desc_msg, actual_value, expect_value):
        """
        断言方法：expect_value等于actual_value
        :param desc_msg: 需要校验的值
        :param actual_var: 实际值
        :param expect_var: 期望值
        """

        validator.check_paramType_str(desc_msg)

        if type(actual_value) != type(expect_value):
            actual_value = str(actual_value)
            expect_value = str(expect_value)

        with allure.step('[断言校验]实际值不等于期望值：{}'.format(desc_msg)):
            AllureHelper.attachText("", "实际值：{}".format(desc_msg, actual_value))
            AllureHelper.attachText("", "期望值：{}".format(desc_msg, expect_value))
            assert expect_value != actual_value

    def assert_actual_ge_expect(self, desc_msg, actual_value, expect_value):
        """
        断言方法：actual_value >= expect_value
        :param desc_msg: 需要校验的值
        :param actual_var: 实际值
        :param expect_var: 期望值
        """

        validator.check_paramType_str(desc_msg)
        validator.check_paramType_int(actual_value, expect_value)

        with allure.step('[断言校验]实际值大于或等于期望值：{}'.format(desc_msg)):
            AllureHelper.attachText("", "实际值：{}".format(actual_value))
            AllureHelper.attachText("", "期望值：{}".format(expect_value))
            assert expect_value >= actual_value

    def assert_actual_gt_expect(self, desc_msg, actual_value, expect_value):
        """
        断言方法：actual_value > expect_value
        :param desc_msg: 需要校验的值
        :param actual_var: 实际值
        :param expect_var: 期望值
        """

        validator.check_paramType_str(desc_msg)
        validator.check_paramType_int(actual_value, expect_value)

        with allure.step('[断言校验]实际值大于期望值：{}'.format(desc_msg)):
            AllureHelper.attachText("", "实际值：{}".format(actual_value))
            AllureHelper.attachText("", "期望值：{}".format(expect_value))
            assert expect_value > actual_value

    def assert_actual_le_expect(self, desc_msg, actual_value, expect_value):
        """
        断言方法：actual_value <= expect_value
        :param desc_msg: 需要校验的值
        :param actual_var: 实际值
        :param expect_var: 期望值
        """

        validator.check_paramType_str(desc_msg)
        validator.check_paramType_int(actual_value, expect_value)

        with allure.step('[断言校验]实际值小于或等于期望值：{}'.format(desc_msg)):
            AllureHelper.attachText("", "实际值：{}".format(actual_value))
            AllureHelper.attachText("", "期望值：{}".format(expect_value))
            assert expect_value <= actual_value

    def assert_actual_lt_expect(self, desc_msg, actual_value, expect_value):
        """
        断言方法：actual_value < expect_value
        :param desc_msg: 需要校验的值
        :param actual_var: 实际值
        :param expect_var: 期望值
        """

        validator.check_paramType_str(desc_msg)
        validator.check_paramType_int(actual_value, expect_value)

        with allure.step('[断言校验]实际值小于期望值：{}'.format(desc_msg)):
            AllureHelper.attachText("", "实际值：{}".format(actual_value))
            AllureHelper.attachText("", "期望值：{}".format(expect_value))
            assert expect_value < actual_value

    def assert_actualTime_in_timeErrorRange(self, actual_time, offset_sec=None):
        '''
        功能：实际时间是否在当前时间允许的误差范围内
        :param actual_time: 待校验的时间，其时间格式为：%Y-%m-%d %H:%M:%S
        :param offset_sec: 时间误差偏移量
        :return:
        '''

        # 默认参数定义
        if not offset_sec:
            offset_sec = 5
        # time_format = "%Y-%m-%d %H:%M:%S"

        # 获取到实际的时间戳
        actual_timestamp = TimeHelper.get_timestamp_from_time(actual_time)

        # 获取期望的时间戳范围
        floor_expect_timestamp = actual_timestamp - offset_sec
        ceil_expect_timestamp = actual_timestamp + offset_sec

        with allure.step('[断言校验]实际时间在期望时间区间范围内,误差偏移量是 {}秒'.format(offset_sec)):
            AllureHelper.attachText("", "实际时间：{}".format(actual_time))
            AllureHelper.attachText("", "期望时间区间：{}--{}".format(TimeHelper.get_time_from_timestamp(floor_expect_timestamp),TimeHelper.get_time_from_timestamp(ceil_expect_timestamp)))

            assert actual_timestamp >= floor_expect_timestamp and actual_timestamp <= ceil_expect_timestamp

    def _get_random_param(self, func_name):
        """
        功能: 实现csv的参数随机化
        :param func_name:
        :return:
        """

        try:
            res = eval("testdata.{}".format(func_name))()
            return res
        except AttributeError:
            raise ParameterizeFunctionException("请确认函数是否存在:testdata/gen_bnsData/{}".format(func_name))
        except Exception as e:
            raise ParameterizeFunctionException("testdata/gen_bnsData/{}: {}".format(func_name, e))

    def _get_depend_param(self, func_name):
        """
        功能: 在csv中解决接口的字段依赖问题
        :param func_name:
        :return:
        """

        try:
            res = eval("testdata.dep_bnsData.{}".format(func_name))()
            return res
        except AttributeError as e:
            print(e)
            raise ParameterizeFunctionException("请确认函数是否存在:testdata/dep_bnsData/{}".format(func_name))
        except Exception as e:
            raise ParameterizeFunctionException("testdata/dep_bnsData/{}: {}".format(func_name, e))

    def parse_csv_param(self, test_data: dict, module_key: str):
        """
        功能: 解析csv中的参数
        :param test_data: 一行字典形式的用例数据
        :param module_key:
        :return: 返回一个list
        """

        validator.check_paramType_dict(test_data)
        validator.check_paramType_str(module_key)

        csvKeys_list = test_data.keys()
        keywords_list = ["$", "$(", "(", ")"]

        generator_objs_list = test_data["generator_objs_list"] = list()

        for csvKey in csvKeys_list:
            value = test_data[csvKey]

            if not value:
                continue

            # 解析依赖字段
            if any(keyword in value for keyword in keywords_list):

                pattern = r"\$\((.*?)\)"
                c = re.compile(pattern, re.S)
                depend_fields_list = re.findall(c, value)
                # depend_fields_list 返回的是到所有$()中的内容
                print("depend_fields_list: {}".format(depend_fields_list))

                depend_values_list = []
                if depend_fields_list:
                    depend_fields_format = re.sub(r"\$\(.*?\)", r"{}", value)
                    for depend_field in depend_fields_list:
                        # 遍历每一个$()中匹配到的内容
                        print("depend_field:{}".format(depend_field))

                        depend_key = None
                        # 如果depend_field包含有点, 则有两种情况(有key和无key)
                        if "." in depend_field:
                            depend_field, depend_key = depend_field.split(".")
                            if not depend_key:
                                depend_key = csvKey

                        func_name = "depend_{}".format(depend_field)
                        generator_obj = self._get_depend_param(func_name)

                        generator_objs_list.append(generator_obj)

                        depend_param = generator_obj.__next__()
                        print(depend_param)

                        if not isinstance(depend_param, dict):
                            depend_values_list.append(depend_param)
                        else:
                            if not depend_key:
                                depend_key = csvKey

                            depend_param = depend_param.get(depend_key)

                            if not depend_param:
                                raise Exception("依赖字典中的key不存在:{}".format(depend_key))
                            depend_values_list.append(depend_param)

                    # 待填充列表: 对应所有实际在{}中填充的值
                    print("depend_values_list: {}".format(depend_values_list))
                    value = depend_fields_format.format(*depend_values_list)

                    # 解析列表
                    if value.startswith("["):
                        if not value.endswith("]"):
                            raise CsvContentException("这不是一个列表字符串: {}".format(value))
                        try:
                            value = eval(value)
                            test_data[csvKey] = value
                            continue
                        except:
                            raise CsvContentException("这不是一个列表字符串: {}".format(value))

                    # 解析字典
                    if value.startswith("{"):
                        if not value.endswith("}"):
                            raise CsvContentException("这不是一个字典字符串: {}".format(value))
                        try:
                            tmp_value = eval(value)
                            test_data[csvKey] = tmp_value
                            continue
                        except:
                            raise CsvContentException("这不是一个字典字符串: {}".format(value))

                    test_data[csvKey] = value
                    continue
                else:
                    raise exceptions.CsvContentException("csv填写内容异常: {}".format(value))

            if not isinstance(value, str):
                continue

            # 解析随机字段
            if isinstance(value, str) and (value.lower() == "r" or value.lower() == "random"):
                func_name = "random_{}_{}".format(module_key, csvKey)
                test_data[csvKey] = self._get_random_param(func_name)
                continue

            # 解析列表
            if value.startswith("["):
                if not value.endswith("]"):
                    raise CsvContentException("这不是一个列表字符串: {}".format(value))
                try:
                    value = eval(value)
                    test_data[csvKey] = value
                    continue
                except:
                    raise CsvContentException("这不是一个列表字符串: {}".format(value))

            # 解析字典
            if value.startswith("{"):
                if not value.endswith("}"):
                    raise CsvContentException("这不是一个字典字符串: {}".format(value))
                try:
                    tmp_value = eval(value)
                    test_data[csvKey] = tmp_value
                    continue
                except:
                    raise CsvContentException("这不是一个字典字符串: {}".format(value))

            # 解析空字符串
            if value in ["e", "empty"]:
                test_data[csvKey] = ""
                continue

            # 解析布尔值False
            if value in ["False", "false", "f", "F"]:
                test_data[csvKey] = False
                continue

            # 解析布尔值True
            if value in ["True", "true", "t", "T"]:
                test_data[csvKey] = True
                continue

        return test_data


# 固定代码模板
class TemplateCase():
    _api = BaseApi()

    def __init__(self, yaml_file, module_key, func_key):

        self.module_key = module_key
        self.func_key = func_key

        # 将yaml信息转为dict
        yamlInfo_to_dict = self._api.base_yaml_info(
            yaml_file=yaml_file,
            module_key=module_key,
            func_key=func_key
        )

        # 检查yaml中是否有以下key："url", "method", "contentType", "data"
        expect_dictKey = ["desc", "url", "method", "contentType", "data"]
        validator.check_existKey_dict(yamlInfo_to_dict, *expect_dictKey)

        # 解析yaml信息
        self.http_params = yamlInfo_to_dict["data"] if yamlInfo_to_dict["data"] else {}
        self.http_desc = yamlInfo_to_dict["desc"]

    def _parseYaml_params_eqSelf(self, http_params):
        """
        功能：处理http的参数
            如果param：["listPage", "listSize", "deviceName"]
            则返回结果：listPage=listPage, listSize=listSize, deviceName=deviceName
        :param http_params:
        :return:
        """

        validator.check_paramType_dict(http_params)

        api_params_list_eqNone = []
        if http_params:
            for param in http_params.keys():
                api_params_list_eqNone.append("{0}={0},".format(param))

        return "\n\t\t\t\t".join(api_params_list_eqNone)

    def _parseYaml_params_testdata(self, http_params):
        """
        功能：处理http的参数
            如果param：["listPage", "listSize", "deviceName"]
            则返回结果：listPage=listPage, listSize=listSize, deviceName=deviceName
        :param http_params:
        :return:
        """

        validator.check_paramType_dict(http_params)

        api_params_list_eqNone = []
        if http_params:
            for param in http_params.keys():
                api_params_list_eqNone.append('{0} = test_data["{0}"]'.format(param))

        return "\n        ".join(api_params_list_eqNone)

    def _parseYaml_params_parameterize(self, http_params, module_key):
        """
        功能：生成scn的参数化模板
        :param http_params:
        :return:
        """

        validator.check_paramType_dict(http_params)

        parameterize_func_list = []
        if http_params:
            for param in http_params.keys():
                parameterize_func_list.append("{0} = testdata.random_{1}_{0}()".format(param, module_key))

        return "\n            ".join(parameterize_func_list)

    def _content_field(self):
        """
        :return: 接口字段级用例的模板代码内容
        """

        return """# -*- coding: utf-8 -*-
# @Time : {0}
import sys
import allure
import pytest

from base.helper import JsonHelper
from case import BaseCase

_testData_list = BaseCase().csv_info(curr_file=__file__)

# 获取api操作对象, 默认权限为平台管理员
api_object_admin = BnsApi()


class Test{5}(BaseCase):

    @pytest.mark.parametrize("test_data", _testData_list)
    def test_field_{1}_{2}(self, test_data):

        first_layer = test_data["first_layer"]
        sencod_layer = test_data["sencod_layer"]
        third_layer = test_data["third_layer"]

        if first_layer:
            allure.dynamic.epic(first_layer)
        if sencod_layer:
            allure.dynamic.feature(sencod_layer)
        if third_layer:
            allure.dynamic.story(third_layer)
        
        module_key = sys._getframe().f_code.co_name.split("_")[2]
        test_data = self.parse_csv_param(test_data, module_key)
        
        {4}
        
        with allure.step("步骤: 请求接口"):

            res_json = api_object_admin.bns_{1}_{2}(
                {3}
            )

        with allure.step("步骤: 提取接口的业务状态码"):
            
            actual_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")

        with allure.step("校验: 业务状态码是否正确"):

            self.assert_actual_equal_expect("业务状态码", actual_code, test_data["expect_code"])
            
        if test_data["expect_msg"]:

            with allure.step("步骤: 提取接口的提示信息"):

                actual_msg = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.message")

            with allure.step("校验: 提示信息是否正确"):

                self.assert_actual_contain_expect("提示信息", actual_msg, test_data["expect_msg"])

        if test_data["clean_data"]:

            with allure.step("步骤: 数据清理操作"):
                
                # TODO: 调用删除接口
                pass
                
        generator_objs_list = test_data.get("generator_objs_list")
        if generator_objs_list:
            for generator_obj in generator_objs_list:
                try:
                    generator_obj.__next__()
                except StopIteration:
                    pass
""".format(TimeHelper.get_time_from_timestamp(),
           self.module_key,
           self.func_key,
           self._parseYaml_params_eqSelf(self.http_params),
           self._parseYaml_params_testdata(self.http_params),
           self.module_key.capitalize()
           )

    def _content_csv(self):
        csv_header = list(self.http_params.keys())
        csv_header.insert(0, "third_layer")
        csv_header.insert(0, "sencod_layer")
        csv_header.insert(0, "first_layer")
        csv_header.insert(0, "case_title")
        csv_header.append("expect_code")
        csv_header.append("clean_data")
        return ",".join(csv_header)

    def _content_module(self):
            """
            :return: 接口模块级用例的模板代码内容
            """

            return """# -*- coding: utf-8 -*-
# @Time : {0}

import pytest
import allure

from case import BaseCase
from bns.facepass.api import Api    # 业务api的调用入口
from base.helper import JsonHelper  # json信息提取
import testdata                     # 可随机化的简单参数
from case import utils              # 可复用的用例步骤

#### tmp use ####
api_admin = Api(username=None,password=None)
#### tmp use ####

@pytest.fixture(scope="function")
def depend_{1}Info():

    with allure.step("前置条件: 添加xxx"):
        # 调用scn api,期望返回一个信息字典info
        # info = api_admin.scn_device_add_snapCamera()
        # 从信息字典中取出唯一性信息, 如id信息
        # {1}Id = info["{1}Id"]
        
    yield info
    
    with allure.step("清理前置条件: 删除xxx"):

        # 从bns api中调用模块的delete方法
        # api_admin.bns_device_delete(deviceId=deviceId)        


@allure.feature("xxx标签")
@allure.story("{4}")
class Test{2}{3}(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    def test_正测_成功xxx_xxx(self):

        with allure.step('准备用例入参'):
            
            {5}

        with allure.step('接口请求'):
            
            res_info = api_admin.bns_{1}_{7}(
                
                {6}
            
            )

        with allure.step('校验:接口响应信息'):
        
            with allure.step('校验:接口状态码'):
        
                actual_code = JsonHelper.parseJson_by_objectpath(res_info, "$.response_data.code")
                expect_code = 0
                self.assert_actual_equal_expect("接口业务码", actual_code, expect_code)

        with allure.step('校验:关联业务'):
            
            # 每个关联业务写成一个step
            pass   

        with allure.step('清理用例'):
            pass   

    """.format(TimeHelper.get_time_from_timestamp(),
               self.module_key,
               self.module_key.capitalize(),
               self.func_key.capitalize(),
               self.http_desc,
               self._parseYaml_params_parameterize(self.http_params, self.module_key),
               self._parseYaml_params_eqSelf(self.http_params),
               self.func_key
               )

    def gen_template_fieldCase(self, file_path=None):
        """
        功能：将模板代码内容写入文件
        :param _content: 模板内容
        :param file: 默认路径为（$PROJECT_ROOT/output/template/scn_api_device.py）
        :return:
        """
        if not file_path:
            # 初始化默认生成文件的路径
            file_path = self.default_filepath_fieldCase
            validator.check_file_isExist(file_path)

            FileHelper.create_filepath(filepath=file_path)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(self._content_field())

    def gen_template_moduleCase(self, file_path=None):
        """
        功能：将模板代码内容写入文件
        """
        if not file_path:
            # 初始化默认生成文件的路径
            file_path = self.default_filepath_moduleCase
            validator.check_file_isExist(file_path)

            FileHelper.create_filepath(filepath=file_path)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(self._content_module())

    def gen_template_csv(self, file_path=None):
        """
        功能：将模板代码内容写入文件
        :param _content: 模板内容
        :param file: 默认路径为（$PROJECT_ROOT/output/template/scn_api_device.py）
        :return:
        """
        if not file_path:
            # 初始化默认生成文件的路径
            file_path = self.default_filepath_csv
            validator.check_file_isExist(file_path)
            # TODO: 如果csv内容多于1行, 则不能随意删除

            FileHelper.create_filepath(filepath=file_path)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(self._content_csv())

    @property
    def default_filepath_fieldCase(self):

        file_path = '{0}{2}{1}{2}test_field_{0}_{1}.py'.format(self.module_key, self.func_key, os.sep)

        file_path = PROJECT_ROOT + os.sep + "case" + os.sep + "field_rank" + os.sep + file_path
        print(file_path)
        return  file_path

    @property
    def default_filepath_moduleCase(self):

        file_path = '{0}{2}{1}{2}test_module_{0}_{1}.py'.format(self.module_key, self.func_key, os.sep)

        file_path = PROJECT_ROOT + os.sep + "case" + os.sep + "module_rank" + os.sep + file_path
        print(file_path)
        return  file_path

    @property
    def default_filepath_csv(self):

        file_path = '{0}{2}{1}{2}testData_{0}_{1}.csv'.format(self.module_key, self.func_key, os.sep)

        file_path = PROJECT_ROOT + os.sep + "case" + os.sep + "field_rank" + os.sep + file_path
        return  file_path