import time,datetime
from itertools import count
import pytz



"asd/fdgs/43t/sda/".split("/", -1)  # 字符串切割  已/分割,-1是全部切割
count("qq/ww/ee/rr/tt/yy/uu")     # 计算字符串的个数
timeArray = time.strptime("2016-05-05 20:28:54", "%Y-%m-%d %H:%M:%S")     #将时间格式转换成时间数组
timestamp = time.mktime(timeArray)    #将时间数组转换成时间戳
data_time_really = datetime.datetime.strptime("2016-05-05 20:28:54", "%Y-%m-%d %H:%M:%S")  # 将字符串转换成datatime格式
tz = pytz.timezone('Asia/Shanghai')  # 获取当前时区对应的时区格式的数据
data_time_timezone = data_time_really.replace(tzinfo=tz) # 把转换好的 datetime 格式,替换为有时区的 datetime 格式