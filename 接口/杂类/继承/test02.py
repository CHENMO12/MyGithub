# -*- coding: utf-8 -*-
# @Time    : 2019/7/1 21:15
# @Author  : Huizi Cai
from 继承.test01 import Test


class Test02(Test):
    def __init__(self, age):  # 重写父类的init 方法
        super().__init__("kobe")  # 继承父类的属性
        # super(Test02, self).__init__(age)
        self.age = age
        print("hahahha")


if __name__ == '__main__':
    test = Test02("18")
    test00 = Test("19")
