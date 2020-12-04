# -*- coding: utf-8 -*-
# ! /usr/bin/python3.7
# @Time : 2020/12/04 10:41

# 点击元素
def button_click(driver,element=None):
    try:
        driver.find_element_by_css_selector(element).click()
    except:
        try:
            driver.find_element_by_xpath(element).click()
        except:
            raise Exception("找不到{}此元素".format(element))

    pass


# 输入框输入
def send_keys(driver, element, keys):
    try:
        driver.find_element_by_css_selector(element).send_keys(keys)
    except:
        try:
            driver.find_element_by_xpath(element).send_keys(keys)
        except:
            raise Exception("找不到{}此元素".format(element))
