# -*- coding: utf-8 -*-
# ! /usr/bin/python3.7
# @Time : 2020/12/04 16:03
from class_page import login, select_menu, data_main, bbc3_select


class API(login.Login, select_menu.SelectMenu, data_main.DataMain, bbc3_select.BBC3Select):
    pass
