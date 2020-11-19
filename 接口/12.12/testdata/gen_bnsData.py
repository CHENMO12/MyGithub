# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 11:47
# @Author  : chinablue
# @Email   : dongjun@reconova.cn
# @File    : gen_bnsData.py

"""
    文件作用:
        存放可参数化的简单业务值

    命名规则:

        "{}_{}_{}".format(
            "模块key",           # 一个平台被分为多个模块
            "模块功能的详细描写",  # 如果不需要详细描述,可以不写
            "参数属性"           # 接口参数的属性说明
        )

    命名举例:

        例1: 对设备名字进行参数化,但设备有多种类型
        code:
            from base.helper import StringHelper
            def device_captureCamera_name():
                return "抓拍相机{}".format(StringHelper.get_random_normalString(5))

        例2: 对设备备注进行参数化
        code:
            from base.helper import StringHelper
            def device_remark():
                return "设备备注{}".format(StringHelper.get_random_normalString(5))

    使用场景:

        1. scn api 的封装
        2. 模块用例和场景用例
"""
import random

from base.helper import StringHelper
from base.helper import JsonHelper
from testdata.addr import node_addr
from base.helper import TimeHelper
from base.helper import FileHelper
import os

now_date = TimeHelper.get_time_from_timestamp()[:10]

################# 声明一些重要的路径或资源路径 #################
# 项目根目录
__project_rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 上报图片的目录
img1_dir = __project_rootdir + os.sep + 'testdata' + os.sep + 'upload_pics_1' + os.sep
# 上报像素图片的目录
pixel_img_dir = __project_rootdir + os.sep + 'testdata' + os.sep + 'upload_pics_facePixel' + os.sep

def random_iotDevice_deviceCode(length=None):
    if not length:
        length=14
    return StringHelper.get_random_normalString(length)


def random_iotDevice_deviceBarCode(length=None):
    if not length:
        length=10
    return StringHelper.get_random_normalString(length)


def random_iotDevice_hardwareVersion():
    return random.choice(["V500001001", "V500002001", "V500003001"])


def random_iotDevice_lensType():
    return random.choice([6, 8, 12, 16])


def random_iotDevice_applyDesc():
    return "申请设备下架{}".format(StringHelper.get_random_normalString(10))

def random_iotDevice_approvalSuggestion():
    return "申请单审批建议{}".format(StringHelper.get_random_normalString(10))

def random_device_deviceName():
    return "设备名称{}".format(StringHelper.get_random_normalString(10))


def random_node_brandName():
    return "品牌名称{}".format(StringHelper.get_random_normalString(10))


def random_node_shopName():
    return "门店名称{}".format(StringHelper.get_random_normalString(10))


def random_node_nodeName():
    return "抓拍子节点{}".format(StringHelper.get_random_normalString(10))

def random_node_collectNodeName():
    return "汇总节点{}".format(StringHelper.get_random_normalString(10))

def random_node_firstPartnerName():
    return "一级合作方{}".format(StringHelper.get_random_normalString(10))

def random_node_secondPartnerName():
    return "二级合作方{}".format(StringHelper.get_random_normalString(10))

def random_node_thirdPartnerName():
    return "三级合作方{}".format(StringHelper.get_random_normalString(10))

def random_node_floorName():
    return "楼层节点{}".format(StringHelper.get_random_normalString(10))

def get_random_addNode_mallAddr():
    ele = random.choice(node_addr)

    # 获取省
    province = JsonHelper.parseJson_by_objectpath(ele, "$.value")

    # 获取市
    city_list = JsonHelper.parseJson_by_objectpath(ele, "$.children.value")
    city = random.choice(city_list)

    # 获取区
    district_list = JsonHelper.parseJson_by_objectpath(ele,"$.children.*[ @.'value' is '{}' ].children..*[@.value]".format(city),res_allowNone=True)
    district = random.choice(district_list)

    return province, city, district

def random_snap_startDateTime():
    return  "{} 00:00:00".format(now_date)

def random_snap_endDateTime():
    return "{} 23:59:59".format(now_date)

def get_face_picture(index=None):
    '''
    功能描述：
        当index不填时，随机获取一张
        当index指定时，获取指定索引的图片
    '''
    img_dir = img1_dir
    return FileHelper.get_file_from_dir(img_dir,file_index=index)

def get_alarmId(timestamp=None):

    if timestamp is None:
        timestamp = timestamp

    tmp_time = TimeHelper.get_time_from_timestamp(timestamp)
    timestamp = TimeHelper.get_timestamp_from_time(assigned_time=tmp_time)
    part_1 = TimeHelper.get_time_from_timestamp(timestamp=timestamp, time_format="%Y-%m-%d_%H-%M-%S")
    part_2 = StringHelper.random_digit(100,999)
    part_3 = StringHelper.random_digit(1000,9999)
    part_4 = StringHelper.random_digit(0,9)
    return "{}_{}_{}_{}".format(part_1, part_2, part_3, part_4)

def get_face_picture_38pixel():
    return pixel_img_dir + "1_38_38.png"

def get_face_picture_40pixel():
    return pixel_img_dir + "2_40_40.jpg"

def get_face_picture_66pixel():
    return pixel_img_dir + "3_66_66.jpg"

def get_face_picture_68pixel():
    return pixel_img_dir + "6_68_68.jpg"

def get_face_picture_90pixel():
    return pixel_img_dir + "4_90_90.jpg"

def get_face_picture1_90pixel():
    return pixel_img_dir + "7_90_90.jpg"

def get_face_picture_00pixel():
    return pixel_img_dir + "5_0_0.jpg"

def get_face_picture_102pixel():
    return pixel_img_dir + "8_102_102.jpg"

def get_face_picture_88pixel():
    return pixel_img_dir + "9_88_88.jpg"

def get_face_picture_92pixel():
    return pixel_img_dir + "10_92_92.jpg"

def get_face_picture_108pixel():
    return pixel_img_dir + "11_108_108.jpg"

def get_face_picture_52pixel():
    return pixel_img_dir + "12_52_52.png"

def get_face_picture_44pixel():
    return pixel_img_dir + "13_44_44.jpg"

def get_face_picture_60pixel():
    return pixel_img_dir + "14_60_60.jpg"

def get_face_picture_59pixel():
    return pixel_img_dir + "14_58_58.jpg"

def get_face_picture_70pixel():
    return pixel_img_dir + "16_70_70.jpg"

def get_face_picture_40_70pixel():
    return pixel_img_dir + "18_40_40.png"

def get_face_picture_64pixel():
    return pixel_img_dir + "17_64_64.jpg"


def random_memberlevel_levelName():
    return "会员级别{}".format(StringHelper.get_random_normalString(6))


def random_member_membername():
    return "会员姓名{}" .format(StringHelper.get_random_normalString(10))

def get_member_membercardNo():
    return "会员卡号{}" .format(StringHelper.get_random_normalString(10))


def random_employee_remark():
    return "店员备注{}" .format(StringHelper.get_random_normalString(10))


def random_employee_employeename():
    return "店员姓名{}" .format(StringHelper.get_random_normalString(10))

def random_operateUser_userPhone():

    return StringHelper.get_random_phoneno()

def random_operateUser_userName():

    return "人员名字{}".format(StringHelper.get_random_normalString(5))

def random_iotUser_userName():

    return "人员名字{}".format(StringHelper.get_random_normalString(7))

def random_iotUser_userPhone():

    return StringHelper.get_random_phoneno()

def random_iotUser_userEmail():

    return StringHelper.get_random_email()

def random_publicDevice_deviceCode(length=None):
    if not length:
        length=14
    return StringHelper.get_random_normalString(length)

def random_publicDevice_deviceBarCode(length=None):
    if not length:
        length=10
    return StringHelper.get_random_normalString(length)

def random_publicDevice_hardwareVersion():
    return random.choice(["V500001001", "V500002001", "V500003001"])

def random_publicDevice_lensType():
    return random.choice([6, 8, 12, 16])



if __name__ == '__main__':
    for ele in node_addr:
        province = JsonHelper.parseJson_by_objectpath(ele, "$.value")
        city_list = JsonHelper.parseJson_by_objectpath(ele, "$.children.value")
        for city in city_list:
            district_list = JsonHelper.parseJson_by_objectpath(ele,"$.children.*[ @.'value' is '{}' ].children..*[@.value]".format(city), res_allowNone=True)
            if district_list is False:
                print("{}省{}市不存在区".format(province, city))


