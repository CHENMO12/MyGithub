#!/usr/bin/python3.7
# @Time : 2020/8/5 0005 14:35
for i in range(0, 10):
    with open("./write.txt", "a", ) as f:
        f.write(str(i))
