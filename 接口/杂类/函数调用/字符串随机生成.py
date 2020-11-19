import uuid
import datetime

srt03 = "".join(uuid.uuid1().__str__())
print(srt03)
srt01 = "品牌" + "22"

list = ["1", "2", "3"]
list2 = []
list2.append(list)
print(list2)
dateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
print(dateTime)