# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 13:48
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : mylog.py
import datetime
import logging
import os

from base import exceptions, validator

'''
    所有的log信息，一定存入文件，选择是否打印到终端
    日志中一旦出现了error，确保有完整的error日志
    日志文件存放在当前文件的logDir目录下
    日志按天存储
    打印的日志信息加入了pid和tid    
'''


def create_filepath(filepath):

    validator.check_paramType_str(filepath)
    if not os.path.isabs(filepath):
        raise exceptions.FileException("参数必须是绝对路径")

    filedir = filepath[0:filepath.rfind(os.sep)]
    if not os.path.isdir(filedir):
        try:
            os.makedirs(filedir)
            # log.log_info("创建文件夹成功：{}".format(path))
        except Exception as e:
            raise exceptions.FileException("执行os.makedirs失败，异常：{}".format(e))

    if not os.path.isfile(filepath):
        with open(filepath, mode='w', encoding='utf-8'):
            pass
    else:
        pass

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Logger(object):
    def __init__(self):
        # 设置日志文件夹
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
        log_dir = project_dir + "output"

        tmp_logDir = datetime.datetime.now().strftime('%Y-%m-%d')

        log_file = log_dir + os.sep + "logData" + os.sep + "{}".format(tmp_logDir) +os.sep + "log.log"
        err_file = log_dir + os.sep + "logData" + os.sep + "{}".format(tmp_logDir) +os.sep + "error.log"

        create_filepath(log_file)
        create_filepath(err_file)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.f_handler = logging.FileHandler(log_file, encoding='utf-8')
        self.f_handler_error = logging.FileHandler(err_file, encoding='utf-8')
        self.s_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s(pid:%(process)d,tid:%(thread)d)--%(levelname)s: %(message)s')
        self.f_handler.setFormatter(formatter)
        self.f_handler_error.setFormatter(formatter)
        self.s_handler.setFormatter(formatter)
    def __set_handler(self,level):
        self.logger.addHandler(self.f_handler)
        self.logger.addHandler(self.s_handler)
        if level == 'error':
            self.logger.addHandler(self.f_handler_error)
    def __remove_handler(self,level):
        self.logger.removeHandler(self.f_handler)
        self.logger.removeHandler(self.s_handler)
        if level == 'error':
            self.logger.removeHandler(self.f_handler_error)
    def log_info(self,msg):
        self.__set_handler('info')
        self.logger.info(msg)
        self.__remove_handler('info')
    def log_warning(self,msg):
        self.__set_handler('warning')
        self.logger.warning(msg)
        self.__remove_handler('warning')
    def log_error(self,msg):
        self.__set_handler('error')
        self.logger.error(msg)
        self.__remove_handler('error')

if __name__ == '__main__':
    mlog = Logger()
    mlog.log_info('i am info')
    mlog.log_warning('i am warning')
    mlog.log_error('i am error')
