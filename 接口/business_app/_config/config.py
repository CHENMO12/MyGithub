# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 12:27
# @Author  : Huizi


from configparser import ConfigParser
import os


class Config(object):
    # 定义变量

    # titles
    ENV_TEST = "env_test"
    # values
    VALUE_WEB_DOMAIN = "web_domain"
    VALUE_NETTY_HOST = "netty_host"
    # VALUE_OLD_NETTY_PORT = "old_netty_port"
    # VALUE_NEW_NETTY_PORT = "new_netty_port"
    VALUE_USERNAME = "username"
    VALUE_PASSWORD = "password"
    VALUE_DEVICE = "device"

    # 项目根目录
    project_rootdir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def __init__(self):
        self.config = ConfigParser()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")
        self.config.read(self.conf_path, encoding='utf-8')

        # 加载配置文件
        self.get_web_domain = self.__get_conf(Config.ENV_TEST, Config.VALUE_WEB_DOMAIN)
        self.get_netty_host = self.__get_conf(Config.ENV_TEST, Config.VALUE_NETTY_HOST)
        # self.get_old_netty_port = self.__get_conf(Config.ENV_TEST, Config.VALUE_OLD_NETTY_PORT)
        # self.get_new_netty_port = self.__get_conf(Config.ENV_TEST, Config.VALUE_NEW_NETTY_PORT)
        self.get_username = self.__get_conf(Config.ENV_TEST, Config.VALUE_USERNAME)
        self.get_password = self.__get_conf(Config.ENV_TEST, Config.VALUE_PASSWORD)
        self.get_device = self.__get_conf(Config.ENV_TEST, Config.VALUE_DEVICE)


    def __get_conf(self,title,value):
        return self.config.get(title,value)
    def set_conf(self, title, value, text):
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)
    def add_conf(self, title):
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)
if __name__ == '__main__':
    cfg = Config()
    print(cfg.get_web_domain)
    print(cfg.get_netty_host)
    # print(cfg.get_old_netty_port)
    # print(cfg.get_new_netty_port)
    print(cfg.get_username)
    print(cfg.get_password)