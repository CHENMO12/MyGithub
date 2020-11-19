# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 13:48
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : mylog.py

import logging
import os
from .mycommon import get_time_from_timestamp

'''
    所有的log信息，一定存入文件，选择是否打印到终端
    日志中一旦出现了error，确保有完整的error日志
    日志文件存放在当前文件的logDir目录下
    日志按天存储
    打印的日志信息加入了pid和tid    
'''

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

def create_file(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass

@singleton
class MyLog(object):
    def __init__(self):
        # 设置日志文件夹
        log_dir = os.path.dirname(os.path.abspath(__file__))
        tmp_logDir = get_time_from_timestamp()[:10]
        log_file = log_dir + '/logData/{}/log.log'.format(tmp_logDir)
        err_file = log_dir + '/logData/{}/error.log'.format(tmp_logDir)
        create_file(log_file)
        create_file(err_file)

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
    mlog = MyLog()
    mlog.log_info('i am info')
    mlog.log_warning('i am warning')
    mlog.log_error('i am error')
