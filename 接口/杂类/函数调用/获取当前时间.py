# -*- coding: utf-8 -*-
# @Time    : 2019/12/25 15:12
import time
import datetime

img_time = datetime.datetime.now().strftime("%Y-%m-%d")+ " 00:00 "
print(img_time)


import time
import datetime
t = time.time()
# print (int(t))                  #秒级时间戳
print (int(round(t * 1000)))  #毫秒级时间戳