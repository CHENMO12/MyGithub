#!/usr/bin/python3.7
# @Time : 2020/5/11 0011 15:52 
class Config():
    url = "http://boss.dev.xybbc.xy"

    # 页面元素
    # 登入页面
    acount = "#username"
    password = "#password"
    login_button = "#root > section > main > div > div > div > form > div:nth-child(3) > div > div > div > button"
    # 数据服务平台
    bbc_menu = "#root > div > section > section > div > main > div > div > div > div > div > div:nth-child(5) > div.ant-card-cover > img"
    # 查询服务
    bbc_search = "#root > div > section > section > div > main > div > div > div > div > div > div:nth-child(2) > div:nth-child(1) > div.ant-card-cover > img"
    # bbc3.0自助查询服务
    bbc3_all_menu = "#root > div.ant-design-pro.ant-pro-basicLayout.screen-xxl.ant-pro-basicLayout-fix-siderbar > section > aside > div > ul > li:nth-child(1) > div.ant-menu-submenu-title"
    bbc3_order = "#\/data\/search\/BBCThreeSearch\$Menu > li.ant-menu-item.ant-menu-item-only-child.ant-menu-item-selected > a > span:nth-child(2)"
