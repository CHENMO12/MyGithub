import logging
import os
import sys
import datetime


# 创建logger，如果参数为空则返回root logger
# logger = logging.getLogger("")
# logger.setLevel(logging.DEBUG)  # 设置logger日志等级
#
# #创建handler
# fh = logging.FileHandler("test.log", encoding="utf-8")
# ch = logging.StreamHandler()
#
# # 设置输出日志格式
# formatter = logging.Formatter(
#     fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     datefmt="%Y/%m/%d %X"
# )
#
# # 注意 logging.Formatter的大小写
#
# # 为handler指定输出格式，注意大小写
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
#
# # 为logger添加的日志处理器
# logger.addHandler(fh)
# logger.addHandler(ch)
#
# # 输出不同级别的log
# logger.warning("泰拳警告")
#
# logger.info("提示")
# logger.error("错误")
#
# current_path = os.path.abspath(os.path.dirname(__file__)+'\log')+ os.sep
# print(current_path)
# # now_time = datetime.datetime.now().strftime('%Y-%m-%d')
# # log_path = current_path + str(now_time) + '_log'
# # print(log_path)
# #
# # handler = logging.handlers.SMTPHandler(mail_host, mail_from, mail_to, '%s__JOB FAILED Attention__' % date.today())
# #
# # handler.setLevel(logging.ERROR)
# #
# # handler.setFormatter(logging.Formatter(format))
# #
# # logger.addHandler(handler)


class Log:
    def __init__(self):
        # 创建handler
        self.logger = logging.getLogger("")
        self.logger.setLevel(logging.DEBUG)
        pass

    def log_info(self, msg):
        self.__handle_file(loginfo='log.log')
        self.logger.info(msg)
        self.logger.removeHandler(self.log_hander)
        self.logger.removeHandler(self.steam_hander)
        pass

    def log_error(self, msg):
        self.__handle_file(loginfo='error.log')
        self.logger.error(msg)
        # 需要移除hander  不然会输出多个
        self.logger.removeHandler(self.log_hander)
        self.logger.removeHandler(self.steam_hander)
        pass

    def log_warning(self, msg):
        self.__handle_file(loginfo='warning.log')
        self.logger.warning(msg)
        self.logger.removeHandler(self.log_hander)
        self.logger.removeHandler(self.steam_hander)
        pass

    def __handle_file(self, loginfo):
        path = self.__creat_file(loginfo)
        self.log_hander = logging.FileHandler(path, encoding="utf-8")
        self.steam_hander = logging.StreamHandler()
        # 日志格式
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y/%m/%d %X"
        )
        self.logger.addHandler(self.log_hander)
        self.logger.addHandler(self.steam_hander)
        self.log_hander.setFormatter(formatter)
        self.steam_hander.setFormatter(formatter)
        pass

    def __creat_file(self, loginfo):
        # current_path = os.path.abspath(os.path.dirname(__file__)+'log')+ os.sep
        current_path = os.getcwd() + '/log' + os.sep
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        log_path = current_path + str(now_time)
        isExists = os.path.exists(log_path)
        filepath = log_path + os.sep + loginfo

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(log_path)
            if not os.path.isfile(filepath):
                with open(filepath, mode='w', encoding='utf-8'):
                    pass
            return filepath
        else:
            if not os.path.isfile(filepath):
                with open(filepath, mode='w', encoding='utf-8'):
                    pass
            return filepath


log = Log()
log.log_info('测试')
log.log_error("测试01")
log.log_warning("test")

