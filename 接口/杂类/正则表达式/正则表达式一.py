# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 17:53
# @Author  : Huizi
import re

str = '123 /n456 /n789'
patten = r'/b4+/d*/b'
a = re.findall(patten, str)
print(a)
