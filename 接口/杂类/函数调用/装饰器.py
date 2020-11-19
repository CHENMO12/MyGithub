#!/usr/bin/python3.7
# @Time : 2020/11/03 11:48
# def deco(func):
#   print("before myfunc() called.")
#   func()
#   print("after myfunc() called.")
#   return func
# @deco
# def myfunc():
#   print("myfunc() called.")
# # myfunc = deco(myfunc) # 与上面的@deco等价
# myfunc()
# print("***********")
# myfunc()


def deco(func):
  def wrapper(*args, **kwargs): # *args, **kwargs用于接收func的参数
      print("开始执行。。。")
      data= func(*args, **kwargs)


      return data
  return wrapper
# @deco
def myfunc(a, b):
  return (a+b)
# a = myfunc(1, 2)
# print(a)

myfunc = deco(myfunc)
a= myfunc(1,2)
print(a)