# -*- coding: utf-8 -*-
# @Time    : 2020/1/8 14:49
class demo1(Exception):
    pass

def demo(a):
    if 2/a > 1:
        print("ok")
        # 抛出异常  必须继承Exception类
        raise demo1("AAAA")

try:
    demo(1)


except  ZeroDivisionError:
     print("分母不能为0")

# 捕获异常
# except demo1:
#     print(22222)
print(1111)
