# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 15:17
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : myrequest.py

import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from .mycommon import md5

from .mylog import MyLog

'''
    如果请求失败，返回值为False
'''


class MyRequest(object):

    def __init__(self):
        self.log = MyLog()
        self.headers_json = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        self.headers_urlencoded = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.headers_formdata = {}

        self.session = requests.session()

    def post_request_by_json(self, url, data=None):
        self.log.log_info("api_url：{}".format(url))
        # 发送请求
        try:
            if data is None:
                self.log.log_info("api_data：None")
                response = requests.post(url=url, headers=self.headers_json)
            else:
                self.log.log_info("api_data：{}".format(data))
                response = requests.post(url=url, data=json.dumps(data), headers=self.headers_json)
        except requests.RequestException as e:
            self.log.log_error("RequestException api_url：{}".format(url))
            self.log.log_error("RequestException api_data：{}".format(data))
            self.log.log_error("RequestException info：{}".format(e))
            return False
        except Exception as e:
            self.log.log_error("Exception api_url：{}".format(url))
            self.log.log_error("Exception api_data：{}".format(data))
            self.log.log_error("Exception info：{}".format(e))
            return False
        return self.__setting_response_format(response, url, data)

    def __app_encryption_key(self, req_data):
        li = []
        str = ''
        for k, v in req_data.items():
            a = k + "=" + v
            li.append(a)
            str = sorted(li)
        a = "&".join(str)
        return md5(a)

    def post_request_by_urlencoded(self, url, data=None, session=False, app_key=False):
        self.log.log_info("api_url：{}".format(url))
        # 发送请求
        try:
            if data is None:
                self.log.log_info("api_data：None")
                response = requests.post(url=url, headers=self.headers_urlencoded)
            else:
                self.log.log_info("api_data：{}".format(data))
                # 如果是老平台的app请求，需要对请求参数进行自定义加密
                if app_key:
                    key = self.__app_encryption_key(data)
                    data["key"] = key
                # 如果是老平台的web端情况，需要带cookie请求
                if session:
                    response = self.session.post(url=url, data=data)
                else:
                    response = requests.post(url=url, data=data, headers=self.headers_urlencoded)
        except requests.RequestException as e:
            self.log.log_error("RequestException api_url：{}".format(url))
            self.log.log_error("RequestException api_data：{}".format(data))
            self.log.log_error("RequestException info：{}".format(e))
            return False
        except Exception as e:
            self.log.log_error("Exception api_url：{}".format(url))
            self.log.log_error("Exception api_data：{}".format(data))
            self.log.log_error("Exception info：{}".format(e))
            return False
        return self.__setting_response_format(response, url, data)

    def post_request_by_file(self, url, data, session=False):
        self.log.log_info("api_url：{}".format(url))

        # 发送请求
        try:
            self.log.log_info("api_data：{}".format(data))
            if session:
                response = self.session.post(url=url, files=data)
            else:
                response = requests.post(url=url, files=data)
        except requests.RequestException as e:
            self.log.log_error("RequestException api_url：{}".format(url))
            self.log.log_error("RequestException api_data：{}".format(data))
            self.log.log_error("RequestException info：{}".format(e))
            return False
        except Exception as e:
            self.log.log_error("Exception api_url：{}".format(url))
            self.log.log_error("Exception api_data：{}".format(data))
            self.log.log_error("Exception info：{}".format(e))
            return False
        time_total = response.elapsed.total_seconds()

        # 接口响应信息
        response_dicts = dict()
        response_dicts['response_code'] = response.status_code
        try:
            response_dicts['response_data'] = response.json()
        except Exception as e:
            self.log.log_error("Exception api_url：{}".format(url))
            self.log.log_error("Exception api_data：{}".format(data))
            self.log.log_error("parseJson Exception info：{}".format(e))
            response_dicts['response_data'] = ''
        response_dicts['response_time'] = time_total
        self.log.log_info("api_response_dicts：{}".format(response_dicts))
        return response_dicts

    def post_request_by_multipart(self, url, fields, boundary, session=False):
        self.log.log_info("api_url：{}".format(url))

        # 发送请求
        data = MultipartEncoder(
            fields=fields,
            boundary="%s" % boundary
        )
        self.headers_formdata['Content-Type'] = data.content_type
        try:
            self.log.log_info("api_data：{}".format(data))
            if session:
                response = self.session.post(url=url, data=data, headers=self.headers_formdata)
            else:
                response = requests.post(url=url, data=data, headers=self.headers_formdata)
        except requests.RequestException as e:
            self.log.log_error("RequestException api_url：{}".format(url))
            self.log.log_error("RequestException api_data：{}".format(data))
            self.log.log_error("RequestException info：{}".format(e))
            return False
        except Exception as e:
            self.log.log_error("Exception api_url：{}".format(url))
            self.log.log_error("Exception api_data：{}".format(data))
            self.log.log_error("Exception info：{}".format(e))
            return False
        return self.__setting_response_format(response, url, data)

    def get_request(self, url, data=None):
        self.log.log_info("api_url：{}".format(url))
        # 发送请求
        try:
            if data is None:
                self.log.log_info("api_data：None")
                response = requests.get(url=url, headers=self.headers_urlencoded)
            else:
                self.log.log_info("api_data：{}".format(data))
                response = requests.get(url=url, data=data, headers=self.headers_urlencoded)
        except requests.RequestException as e:
            self.log.log_error("RequestException api_url：{}".format(url))
            self.log.log_error("RequestException info：{}".format(e))
            return False
        except Exception as e:
            self.log.log_error("Exception api_url：{}".format(url))
            self.log.log_error("Exception info：{}".format(e))
            return False
        return self.__setting_response_format(response, url, data)

    def __setting_response_format(self, response, url, data):
        time_total = response.elapsed.total_seconds()
        response_dicts = dict()
        response_dicts['request_addrPath'] = "/" + "/".join(url.split("/")[3:])
        response_dicts['request_data'] = data
        response_dicts['response_code'] = response.status_code

        # 进行http的状态码的检测
        if response_dicts['response_code'] == 200:
            # 检测接口返回的数据是否为json格式
            try:
                response_dicts['response_data'] = response.json()
            except Exception as e:
                self.log.log_error("Exception api_url：{}".format(url))
                self.log.log_error("Exception api_data：{}".format(data))
                self.log.log_error("parseJson Exception info：{}".format(e))
                self.log.log_warning("http响应数据不是json格式，估么这是个BUG！！！")
                exit("http响应数据不是json格式，估么这是个BUG！！！")
                # response_dicts['response_data'] = ''
            response_dicts['response_time'] = time_total
            self.log.log_info("api_response_dicts：{}".format(response_dicts))
            return response_dicts
        elif response_dicts['response_code'] == 400:
            self.log.log_error(response_dicts)
            self.log.log_error("客户端请求错误,Exception api_url：{}".format(url))
            exit("http状态码400，客户端请求错误")
        elif response_dicts['response_code'] == 401:
            self.log.log_error(response_dicts)
            self.log.log_error("未授权或授权过期,Exception api_url：{}".format(url))
            exit("http状态码401，未授权或授权过期")
        elif response_dicts['response_code'] == 404:
            self.log.log_error(response_dicts)
            self.log.log_error("请求接口不存在,Exception api_url：{}".format(url))
            exit("http状态码404，请求接口不存在")
        elif response_dicts['response_code'] == 500:
            self.log.log_error(response_dicts)
            self.log.log_error("服务内部错误,Exception api_url：{}".format(url))
            exit("http状态码500，服务内部错误")
        elif response_dicts['response_code'] == 502:
            self.log.log_error(response_dicts)
            self.log.log_error("服务器异常,Exception api_url：{}".format(url))
            self.log.log_error('''
                ############################################
                # 请排查如下情况：                            #
                #    1. 网络问题，能不能ping通。              #
                #    2. 远程服务有没有启动，端口是否可用        #
                #    3. 远程服务请求是否繁忙导致的时好时坏       #
                ############################################
            ''')
            exit("http状态码502，服务器异常")
        elif response_dicts['response_code'] == 503:
            self.log.log_error(response_dicts)
            self.log.log_error("服务暂时不可用,Exception api_url：{}".format(url))
            exit("http状态码503，服务暂时不可用")


if __name__ == '__main__':
    login_url = "http://172.16.3.90:8766/auth/getAccessToken"
    login_data = {
        'username': "13612959780",
        'passwd': "e10adc3949ba59abbe56e057f20f883e",
    }
    req = MyRequest()
    res = req.post_request_by_json(login_url, login_data)
    print(res)
