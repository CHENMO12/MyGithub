# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 19:06
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : exceptions.py

'''
    跟踪记录所有抛出的异常
'''

# 数据异常
class ParamTypeException(Exception):
    '''
        数据类型异常
    '''
    pass

# http异常
class HttpException(Exception):
    '''
        Http异常
    '''
    pass

class HttpRequestException(HttpException):
    '''
        Http异常:http请求异常
    '''
    pass

class HttpResponseException(HttpException):
    '''
        Http异常:http响应异常
    '''
    pass

class ListOptionsException(Exception):
    '''
        列表选项异常
        例如：某个字段只能选择1,2,3；而你选择了4
    '''
    pass

class ExtractJsonException(Exception):
    '''
        提取json信息异常
    '''
    pass

class FileException(Exception):
    '''
        文件异常
    '''
    pass

class DictException(Exception):
    '''
        字典异常
    '''
    pass




class MyBaseError(Exception):
    pass


class FileNotFound(Exception):
    pass

class FileContentEmpty(Exception):
    pass

class FileFormatError(Exception):
    pass

class ParamNotStrType(Exception):
    pass
class ParamNotIntType(Exception):
    pass

class ParamEmptyStr(Exception):
    pass

class VariableNotFound(Exception):
    pass

class ParamsError(Exception):
    pass

class FunctionNotFound(Exception):
    pass


class HttpRequestError(Exception):
    pass

class NotJsonFormat(Exception):
    pass

class HttpResponseBodyNotJsonFormat(NotJsonFormat):
    pass

class HttpResponseErrorUnauthorized(Exception):
    pass

class HttpUrlNotExist(Exception):
    pass

class HttpServerInnerError(Exception):
    pass

class HttpServerRunException(Exception):
    ############################################
    # 请排查如下情况：                            #
    #    1. 网络问题，能不能ping通。              #
    #    2. 远程服务有没有启动，端口是否可用        #
    #    3. 远程服务请求是否繁忙导致的时好时坏       #
    ############################################
    pass

class HttpUnknownError(Exception):
    pass


class DefinedBusinessException(Exception):
    pass

class UndefinedBusinessException(Exception):
    pass

class WaitAPITimeoutException(Exception):
    pass

class CsvContentException(Exception):
    pass

class ParameterizeFunctionException(Exception):
    pass
