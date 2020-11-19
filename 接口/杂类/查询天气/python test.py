#!/usr/bin/python3.7
# @Time : 2020/09/16 16:37
#  求和
# list = []
# for i in range(0, 101):
#     list.append(i)
# all = sum(list)
# print(all)
# c = 0
# for i in range(1, 101):
#     c = c + i+1
# print(c)
# list = [1, 2, 3, 4, 5, 6]
# a = 3
# for i in list:
#     if i > a:
#         print(i)
#         break
list = [1, 3, 2, 4, 5, 2, 10, 8, 9]
len = len(list)
k = 0
for i in range(len):
    for h in range(0, len - i - 1):
        if list[h] > list[h + 1]:
            list[h + 1], list[h] = list[h], list[h + 1]

print(list)
