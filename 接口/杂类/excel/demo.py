#!/usr/bin/python3.7
# @Time : 2020/09/28 20:02
import xlrd

data = xlrd.open_workbook("F:\接口\杂类\excel\demo.xls")

data = data.sheet_by_name("Sheet1")

rows = data.row_values(1)  # 获取第二行的数据

two_cols = data.col_values(1)  # 获取第二列的数据
one_cols = data.col_values(0)  # 获取第一列的数据

for i in range(1, 4):
    print(one_cols[i])
    print(two_cols[i])
