# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 10:47
import random
import pytest
#
# @pytest.fixture(scope='function',params=["参数1","参数2"])
# def function(a):
#     print()
#     name = "".join(random.choice("0123456789") for i in range(5))
#     yield   name
#     print(a)
#
# # @pytest.fixture(scope='function',name='11')
# # def module():
# #     print(222222)
# #     yield
# #     print("end2")
# #
# #
# # @pytest.fixture(scope='class')
# # def cls():
# #     print(333333)
# #     yield  print("end3")
#
#
# class Test:
#     def test1(self,function,):
#         pass
#
#
#
#
#     # def test2(self):
#     #     print('测试2')
#     #
#     # def test3(self):
#     #     print('测试2')
#
# if __name__ == '__main__':
#     pytest.main()


import pytest

@pytest.fixture()
def myfixture01():
    print("执行ok")

    return "你好"
@pytest.fixture()
def myfixture(myfixture01,request):
    print("执行myfixture固件--%s" % request.param)

    return "你好"


class Test_Pytest():

    @pytest.mark.parametrize("myfixture", ["2"], indirect=True)
    def test_one(self, myfixture):
        print("test_one方法执行")
        print(myfixture)
        assert 1 == 1

    def test_two(self):
        print("test_two方法执行")
        assert "o" in "love"

    def test_three(self):
        print("test_three方法执行")
        assert 3 - 2 == 1


if __name__ == "__main__":
    pytest.main(['-s', 'test_firstFile.py'])
