# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 15:25
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : fixed_businessData.py

"""
    文件作用:
        存放固定业务值

    命名规则:
        采用大驼峰方式定义一个class类
        "{}{}".format(
            "模块key",     # 一个平台被分为多个模块
            "参数属性"     # 接口参数的属性说明
        )

    命名举例:

        例1: 人员类型分为:普通人员类型和特殊人员类型
        code:

            class PersonType(Enum):
                commonPerson = 1     # 普通人员
                specialPerson = 2    # 特殊人员

    使用场景:

        1. scn api 的封装
        2. 模块用例和场景用例
"""

from enum import Enum

class LogicTypeId(Enum):
    outshop = 1
    intoshop = 2
    cashier = 3
    floor = 4
    heatmap = 5

class LogicType(Enum):
    # 进店-1， 店外-2， 收银台-3， 楼层入口-4， 热力-5
    intoshop = 1
    outshop = 2
    cashier = 3
    floor = 4
    heatmap = 5

#抓拍类型，0:人脸;3:头肩;5:无特征人脸;6:低质量
class SnapType(Enum):
    face = 0
    head_shoulder = 3
    nofeature = 5
    lowquality = 6
    nofacedetect = 7

class UserStatus(Enum):
    stateless = 0
    wanderoutshop = 1
    intoshop = 2
    wanderinshop = 3
    outshop = 4

class UserType(Enum):
    guest = 0
    member = 1
    clerk = 2

class operateUserId(Enum):
    techSupport = 2
    data_correct = 3
    installation_person = 4

class personId(Enum):
    mall_manager = 4  # 商场管理员
    mall_clerk = 5  # 商场员工

class CollectTypeId(Enum):
    # 门店汇总-1， 楼层汇总-2， 其他汇总3
    shopcollect = 1
    floorcollect = 2
    othercollect = 3

class NodeLevel(Enum):
    platform = -2
    partner = -1
    brand = 0
    group = 1
    shop = 2
    floor = 3
    collect = 4
    logic = 5
