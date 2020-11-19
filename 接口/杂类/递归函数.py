#!/usr/bin/python3.7
# @Time : 2020/10/10 17:49
def recu_add(n):
    if n == 1:   # 出口  当n=1时  跳出自我调用
        return 1
    else:
        return n + recu_add(n - 1)

a=recu_add(5)
print(a)