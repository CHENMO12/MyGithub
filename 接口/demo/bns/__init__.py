# -*- coding: utf-8 -*-
# @Time    : 2019/9/30 0030 上午 10:25
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : bns_api_device.py

"""
api可以分为业务api和场景api
其中：
    业务api：所有参数可以自由输入
    场景api：对业务码进行分类
"""
import os
from enum import Enum
from urllib import parse

from base import validator
from base import exceptions
from base.request import Request
from base.helper import YamlHelper, FileHelper, TimeHelper, PROJECT_ROOT, JsonHelper
import config


# http通用内容
class BaseApi():
    class ContentType(Enum):
        '''
            请求数据传输格式
        '''
        URLENCODED = "application/x-www-form-urlencoded"
        JSON = "application/json"
        FILE = "multipart/form-data"

    def base_request(self, request_method, request_type, request_url, request_data=None, auth=None, headers=None,
                     cookies=None):

        if not headers: headers = dict()
        if request_type == "urlencoded":
            headers["Content-Type"] = self.ContentType.URLENCODED.value
        elif request_type == "json":
            headers["Content-Type"] = self.ContentType.JSON.value
        elif request_type == "file":
            headers["Content-Type"] = self.ContentType.FILE.value

        req = Request(verbose=True)
        response_info = req.send_request(request_url=request_url,
                                         request_method=request_method,
                                         request_type=request_type,
                                         request_data=request_data,
                                         auth=auth,
                                         headers=headers,
                                         cookies=cookies)
        return response_info

    def base_filter_data(self, data: dict):
        """
        功能：移除data字典中value是None的key，
             如果value也是个字典，其中的None或""也会被移除。
        :param data: http请求参数，字典形式
        :return: 处理过的字典
        """

        validator.check_paramType_dict(data)

        keys = data.keys()
        keys_to_remove = []
        for k in keys:
            v = data[k]
            if v is None:
                keys_to_remove.append(k)

            if isinstance(data[k], dict):
                self.base_filter_data(data[k])

        for k in keys_to_remove:
            data.pop(k)

        return data

    def base_urlencode_parse(self, data):

        return parse.urlencode(data)

    def base_yaml_info(self, yaml_file=None, module_key=None, func_key=None, curr_file=None):
        """
        功能：先将yaml文件转为字典，再在字典中通过key取value。
        :param yaml_file: yaml文件
        :param module_key: 字典的key
        :param curr_file: 默认填写 __file__
        :return:
        """
        # TODO(dongjun): module_key 如果只有一个key时，自动读取

        if not yaml_file:
            curr_dir = os.path.dirname(curr_file)
            yaml_file_list = FileHelper.get_files_from_folderOrFolderlist(curr_dir, ".yaml", recursive=False)
            if len(yaml_file_list) == 1:
                yaml_file = yaml_file_list[0]
            elif len(yaml_file_list) == 0:
                raise exceptions.FileException("当前目录下不存在yaml文件：{}".format(curr_dir))
            else:
                raise exceptions.FileException("当前目录下存在多个yaml文件，请明确指明yaml路径，：{}".format(curr_dir))

        if not module_key:
            module_key = ""
        validator.check_file_isFile(yaml_file)
        validator.check_paramType_str(module_key)

        api_dictInfo = YamlHelper.load_yaml_file(yaml_file)
        api_info = api_dictInfo.get(module_key)
        if module_key is "":
            return api_dictInfo
        elif api_info:
            if func_key:
                api_info = api_info.get(func_key)
                if api_info:
                    return api_info
                raise exceptions.DictException("yaml中func_key不存在。yaml_path：{},目标key：{}".format(yaml_file, func_key))

            return api_info
        else:
            raise exceptions.DictException("yaml中module_key不存在。yaml_path：{},目标key：{}".format(yaml_file, module_key))

    def base_url(self, port=None):
        """
            base_url:
                可能性1：域名     ( http://www.baidu.com )
                可能性2：ip+端口  ( http://192.168.90.150:8090 )
            使用场景：
                1. 正常情况下，web地址就是base_url
                2. 有些情况下，不同的url需访问不同的端口
        """

        base_url = config.get_b2b_host

        tmp_list = base_url.split(":")

        if len(tmp_list) == 3:
            if port:
                tmp_list.pop()
                tmp_list.append(str(port))
                base_url = ":".join(tmp_list)

        return base_url


# 固定代码模板
class TemplateApi():
    _api = BaseApi()

    def __init__(self, yaml_file, module_key, func_key):
        # TODO(dongjun): 目前暂不支持一次生成多个业务api的代码模板

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

    def _parseYaml_params_eqNone(self, http_params):
        """
        功能：处理http的参数
            如果param：["listPage", "listSize", "deviceName"]
            则返回结果：listPage=None, listSize=None, deviceName=None
        :param http_params:
        :return:
        """

        validator.check_paramType_dict(http_params)

        api_params_list_eqNone = []
        if http_params:
            for param in http_params.keys():
                api_params_list_eqNone.append("{}=None".format(param))

        return ", ".join(api_params_list_eqNone)

    def _parseYaml_params_addPrefixEdit_eqNone(self, http_params):
        """
        功能：处理http的参数
            如果param：["listPage", "listSize", "deviceName"]
            则返回结果：edit_listPage=None, edit_listSize=None, edit_deviceName=None
        :param http_params:
        :return:
        """

        validator.check_paramType_dict(http_params)

        api_params_list_eqNone = []
        if http_params:
            for param in http_params.keys():
                api_params_list_eqNone.append("edit_{}=None".format(param))

        return ", ".join(api_params_list_eqNone)

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

        return "\n\t\t\t\t\t\t\t\t\t\t".join(api_params_list_eqNone)

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
                parameterize_func_list.append(
                    "if {0} is None: {0} = gen_bnsData.random_{1}_{0}()".format(param, module_key))

        return "\n        ".join(parameterize_func_list)

    def _parseYaml_params_responseApiDict(self, http_params):
        """
        功能：生成scn的返回信息模板

        :param http_params:
        :return:
        """

        validator.check_paramType_dict(http_params)

        parameterize_func_list = []
        if http_params:
            for param in http_params.keys():
                parameterize_func_list.append("if {0} is not None: info_dict.setdefault('{0}', {0})".format(param))

        return "\n            ".join(parameterize_func_list)

    def _parseYaml_params_request(self, http_params):
        """
        功能：处理http的参数
            如果param：["listPage", "listSize", "deviceName"]
            则返回结果：
                    http_data["listPage"]: listPage,
			        http_data["listSize"]: listSize,
			        http_data["deviceName"]: deviceName,
        :param http_params:
        :return:
        """

        validator.check_paramType_dict(http_params)

        api_params_list = []
        if http_params:
            for param in http_params.keys():
                api_params_list.append('http_data["{0}"]: {0},'.format(param))

        return "\n\t\t\t".join(api_params_list)

    def _content_bns(self):
        """
        :return: 业务api的模板代码内容
        """

        return """# -*- coding: utf-8 -*-
# @Time : {0}
from base.decorators import allure_attach


class BnsApi(BusinessApi):

    def __init__(self, username=None, password=None):

        super().__init__(username=username,password=password)

        self._config_{1} = self.base_yaml_info(
            curr_file=__file__,
            module_key=__name__.split(".")[-2]
        )

    @allure_attach("{5}")
    def bns_{1}_{2}(self, headers=None, {3}):
        # TODO: 请完成函数注释!!!

        api_info = self._config_{1}["{2}"]

        http_url = api_info["url"]
        http_port = api_info.get("port")
        http_method = api_info["method"]
        http_contentType = api_info["contentType"]
        http_data = api_info["data"]

        # 请求入参
        data = {{
            {4}
        }}
        data = self.base_filter_data(data)

        # 请求地址
        response = self.business_request(
            # TODO: 请确认url是否需要变化！！！
            request_url="{{}}{{}}".format(self.base_url(http_port), http_url),
            request_method=http_method,
            request_type=http_contentType,
            request_data=data,
            headers=headers
        )

        return response

""".format(
            TimeHelper.get_time_from_timestamp(),
            self.module_key,
            self.func_key,
            self._parseYaml_params_eqNone(self.http_params),
            self._parseYaml_params_request(self.http_params),
            self.http_desc
        )

    def _content_scn(self):
        """
        :return: 场景api的模板代码内容
        """

        if "add" in self.func_key:
            return """# -*- coding: utf-8 -*-
# @Time : {0}
from base.decorators import api_retry
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper
from testdata import gen_bnsData


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @api_retry()
    def scn_{1}_{2}(self, headers=None, {3}, res_accurate=False, business_exception=False):
        # TODO: 请确定参数并完成参数注释

        # 参数化
        {6}

        # 发送业务请求
        res_json = self.bns_{1}_{2}(headers=headers,\n\t\t\t\t\t\t\t\t\t\t{4})

        # 定义一个http状态码的白名单, 如果状态码不在白名单中,则直接返回
        white_list = [200, 201]
        # 获取当前请求的http状态码
        http_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_code")
        # 如果请求返回的状态码不是期望的http状态码, 则直接返回该状态码
        if http_code not in white_list:
            return res_json

        # 提取业务码
        actually_business_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")
        # 异常码集合
        exception_list = [
            # 400004,   # 设备类型不合法
        ]

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                pass
                # return deviceCode

            # 全部信息返回
            info_dict = dict()
            # TODO: 请确认,是否需要接收其他必要信息, 如添加后产生的唯一性标识信息
            {7}
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:{5}")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:{5}")

            """.format(
                TimeHelper.get_time_from_timestamp(),
                self.module_key,
                self.func_key,
                self._parseYaml_params_eqNone(self.http_params),
                self._parseYaml_params_eqSelf(self.http_params),
                self.http_desc,
                self._parseYaml_params_parameterize(self.http_params, self.module_key),
                self._parseYaml_params_responseApiDict(self.http_params)
            )
        elif "edit" in self.func_key:
            return """# -*- coding: utf-8 -*-
# @Time : {0}
from base.decorators import retry_common_api
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    @retry_common_api()
    def scn_{1}_{2}(self, headers=None, {3}, res_accurate=False, business_exception=False):
        # TODO: 请确定参数并完成参数注释

        # 参数化

        # TODO: 参数化--获取详情信息
        # detail_info = {{}}

        # TODO: 参数化--确认不可编辑参数

        # TODO: 参数化--确认可编辑参数
        # deviceName = detail_info.get("name")
        # if edit_deviceName is not None: deviceName = edit_deviceName

        # 发送业务请求
        res_json = self.bns_{1}_{2}(headers=headers,\n\t\t\t\t\t\t\t\t\t\t{4})

        # 定义一个http状态码的白名单, 如果状态码不在白名单中,则直接返回
        white_list = [200, 201]
        # 获取当前请求的http状态码
        http_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_code")
        # 如果请求返回的状态码不是期望的http状态码, 则直接返回该状态码
        if http_code not in white_list:
            return res_json

        # 提取业务码
        actually_business_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")
        # 异常码集合
        exception_list = [
            # 400004,   # 设备类型不合法
        ]

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                pass
                # return deviceCode

            # 全部信息返回
            info_dict = dict()
            # TODO: 参考对应的add接口信息
            # if deviceType: info_dict.setdefault('deviceType', deviceType)
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:{5}")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:{5}")

            """.format(
                TimeHelper.get_time_from_timestamp(),
                self.module_key,
                self.func_key,
                self._parseYaml_params_addPrefixEdit_eqNone(self.http_params),
                self._parseYaml_params_eqSelf(self.http_params),
                self.http_desc
            )
        else:
            return """# -*- coding: utf-8 -*-
# @Time : {0}
from base.decorators import retry_common_api
from base.exceptions import DefinedBusinessException, UndefinedBusinessException
from base.helper import JsonHelper


class ScnApi(BnsApi):

    def __init__(self, username=None, password=None):
        super().__init__(username=username, password=password)

    def scn_{1}_{2}(self, headers=None, {3}, res_accurate=False, business_exception=False):
        # TODO: 请确定参数并完成参数注释

        # 参数化
        # if func_param is None: func_param = gen_bnsData.xxx()

        # 发送业务请求
        res_json = self.bns_{1}_{2}(headers=headers,\n\t\t\t\t\t\t\t\t\t\t{4})

        # 定义一个http状态码的白名单, 如果状态码不在白名单中,则直接返回
        white_list = [200, 201]
        # 获取当前请求的http状态码
        http_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_code")
        # 如果请求返回的状态码不是期望的http状态码, 则直接返回该状态码
        if http_code not in white_list:
            return res_json

        # 提取业务码
        actually_business_code = JsonHelper.parseJson_by_objectpath(res_json, "$.response_data.code")
        # 异常码集合
        exception_list = [
            # 400004,   # 设备类型不合法
        ]

        # 正常业务状态码下, 函数的返回信息
        if actually_business_code == 0:

            # 解析返回信息或调用自定义函数

            # 精确返回的内容
            if res_accurate:
                pass
                # return deviceCode

            # 全部信息返回
            info_dict = dict()
            return info_dict if info_dict else JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(已知异常), 函数的返回信息
        elif actually_business_code in exception_list:

            if business_exception:
                raise DefinedBusinessException("接口已知业务异常:{5}")

            return JsonHelper.parseJson_by_objectpath(res_json, "$.response_data")

        # 异常业务状态码下(未知异常), 函数的返回信息
        else:
            raise UndefinedBusinessException("接口未知业务异常:{5}")

    """.format(
                TimeHelper.get_time_from_timestamp(),
                self.module_key,
                self.func_key,
                self._parseYaml_params_eqNone(self.http_params),
                self._parseYaml_params_eqSelf(self.http_params),
                self.http_desc
            )

    def gen_template_bns(self, file_path=None):
        """
        功能：将模板代码内容写入文件
        :param _content: 模板内容
        :param file: 默认路径为（$PROJECT_ROOT/output/template/bns_api_device.py）
        :return:
        """
        if not file_path:
            # 初始化默认生成文件的路径
            file_path = self.default_filepath_bns
            FileHelper.delete_file(filepath=file_path)
            FileHelper.create_filepath(filepath=file_path)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(self._content_bns())

    def gen_template_scn(self, file_path=None):
        """
        功能：将模板代码内容写入文件
        :param _content: 模板内容
        :param file: 默认路径为（$PROJECT_ROOT/output/template/scn_api_device.py）
        :return:
        """
        if not file_path:
            # 初始化默认生成文件的路径
            file_path = self.default_filepath_scn
            FileHelper.delete_file(filepath=file_path)
            FileHelper.create_filepath(filepath=file_path)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(self._content_scn())

    @property
    def default_filepath_bns(self):
        file_path = PROJECT_ROOT + os.sep + "output" + os.sep + "template" + os.sep + "bns_api_{}.py".format(
            self.module_key)
        return file_path

    @property
    def default_filepath_scn(self):
        file_path = PROJECT_ROOT + os.sep + "output" + os.sep + "template" + os.sep + "scn_api_{}.py".format(
            self.module_key)
        return file_path





















