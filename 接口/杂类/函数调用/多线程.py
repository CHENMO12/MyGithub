 # -*- coding: utf-8 -*-
# @Time    : 2019/7/4 16:31
# @Author  : Huizi Cai
import _thread
import time


# 为线程定义一个函数

def print_time(threadName,name):
    count = 0
    # while count < 5:
    #     time.sleep(delay)
    #
    #     print("%s: %s" % (threadName, time.ctime(time.time())))
    while count <= 2:
        print(name)
        count += 1



# 创建两个线程
# while True:
try:
    _thread.start_new_thread(print_time, ("Thread-1", "ok"))
    _thread.start_new_thread(print_time, ("Thread-2", "good"))
except:
    print("Error: unable to start thread")

while 1:
   pass