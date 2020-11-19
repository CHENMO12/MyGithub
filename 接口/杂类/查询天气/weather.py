from xpinyin import Pinyin
import urllib.request as r
import requests
import json
import objectpath
import pymysql
import datetime
import time


# 例：lists = ['wu', 'han']
def pinyin_2_hanzi(pinyinList):
    from Pinyin2Hanzi import DefaultDagParams
    from Pinyin2Hanzi import dag

    dagParams = DefaultDagParams()
    # 取第一个值
    result = dag(dagParams, pinyinList, path_num=10, log=True)[0].path[0]
    return result


p = Pinyin()
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='998179', db='test', charset='utf8')
sql = "SELECT city_name FROM weather"
cursor = db.cursor()
cursor.execute(sql)
data = cursor.fetchall()
# cursor.close()
# db.close()

while True:
    # try:
    # if data:
    a = input('请输入城市,世界任何城市:')
    a = p.get_pinyin(a).replace("-", "")

    url = "http://api.openweathermap.org/data/2.5/forecast?q={}," \
          "cn&mode=json&lang=zh_cn&&APPID=6a67ed641c0fda8b69715c43518b6996&units=metric".format(
        a)
    # rst = r.urlopen(url).read().decode('utf-8')
    rst = requests.get(url=url).json()
    # print(rst)
    tree = objectpath.Tree(rst)
    description = tree.execute("$.*.list..description")
    temp_min = tree.execute("$.*.list..temp_min")
    temp_max = tree.execute("$.*.list..temp_max")
    feels_like = tree.execute("$.*.list..feels_like")
    wind_speed = tree.execute("$.*.list..speed")
    list_des = []
    list_temp_min = []
    list_temp_max = []
    list_feels_like = []
    list_wind_speed = []
    for i in description:
        list_des.append(i)
    for i in temp_max:
        list_temp_max.append(i)
    for i in temp_min:
        list_temp_min.append(i)
    for i in feels_like:
        list_feels_like.append(i)
    for i in wind_speed:
        list_wind_speed.append(i)
    print("天气情况：%s" % list_des[0])
    print("最高温度：%s" % max(list_temp_max))
    print("体感温度：%s" % list_feels_like[0])
    print("最低温度：%s" % min(list_temp_min))
    print("最高风速：%s" % max(list_wind_speed))
    print("最低风速：%s" % min(list_wind_speed))
    # curent_time = datetime.datetime.now().strftime("%Y-%m-%d")
    # sql = ("INSERT INTO weather(city_name,temp,des,create_time) VALUES ('{}',{},'{}','{}')").format(a, int(
    #     list_feels_like[0]), list_des[0], curent_time)
    # db.ping(reconnect=True)
    # cursor.execute(sql)
    # cursor.close()
    # db.commit()
    # db.close()
# except:
#     print("输入不正确...")
#     continue
