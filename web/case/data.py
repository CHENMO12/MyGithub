# -*- coding: utf-8 -*-
# ! /usr/bin/python3.7
# @Time : 2020/12/04 15:57
from selenium import webdriver
from config import Config
from class_page import api
from public.public import send_keys, button_click
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select
import time
import pytest

api = api.API()


# wait = ui.WebDriverWait(self.driver, 10)
# wait.until(lambda driver: driver.find_element_by_css_selector()
# create a new Firefox session
class Test:
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(Config.url)
        self.driver.implicitly_wait(5)
        send_keys(self.driver, api.acount, Config.acount)
        send_keys(self.driver, api.password, Config.password)
        button_click(self.driver, api.login_button)

    def menu_bbc(self):
        # 数据中台服务
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        button_click(self.driver, api.bbc_menu)

    def test_bbc_search(self):
        # 查询
        self.menu_bbc()
        self.driver.implicitly_wait(5)
        button_click(self.driver, api.bbc_search)

    # bbc3.0自助查询服务
    def bbc_3(self):
        # time.sleep(1)
        # search_window = self.driver.window_handles
        # self.driver.switch_to.window(search_window[1])
        self.driver.implicitly_wait(5)
        button_click(self.driver, api.bbc3_all_menu)
        self.driver.implicitly_wait(5)
        button_click(self.driver, api.bbc3_order)
        pass

    # bbc3.0自助查询服务
    def bbc_4(self):
        pass

    def teardown(self):
        self.driver.close()


if __name__ == '__main__':
    pytest.main(["-q", "data.py"])
    # a.bbc_3()

    # a.add_po_detail()
