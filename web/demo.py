from selenium import webdriver
from config import Config
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select
import time


# wait = ui.WebDriverWait(self.driver, 10)
# wait.until(lambda driver: driver.find_element_by_css_selector()
# create a new Firefox session
class BBC:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        # 登入
        self.driver.get(Config.url)
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector(
            Config.acount).send_keys("admin")
        self.driver.find_element_by_css_selector(
            Config.password).send_keys("123456")
        self.driver.find_element_by_css_selector(
            Config.login_button).click()

    def menu_bbc(self):
        # 数据中台服务
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector(Config.bbc_menu).click()

    def bbc_search(self):
        # 查询
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector(Config.bbc_search).click()

    # bbc3.0自助查询服务
    def bbc_3(self):
        # time.sleep(1)
        # search_window = self.driver.window_handles
        # self.driver.switch_to.window(search_window[1])
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector(Config.bbc3_all_menu).click()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_css_selector(Config.bbc3_order).click()
        pass

    # bbc3.0自助查询服务
    def bbc_4(self):
        pass

    def button_click(self, element=None):
        pass


if __name__ == '__main__':
    a = BBC()
    a.login()
    a.menu_bbc()
    a.bbc_search()
    a.bbc_3()

    # a.add_po_detail()
