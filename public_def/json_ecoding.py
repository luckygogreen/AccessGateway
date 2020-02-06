import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)



# python3运行报错：TypeError: Object of type 'type' is not JSON serializable解决方法
# 2.在你发生错误的文件当中 比如a.py
# 第一步：
# from MyEncoder import MyEncoder
# 第二步：
# 将json.dumps（data）改写为json.dumps(data,cls=MyEncoder,indent=4)
# 3.至于json.dumps函数里面的cls，indent参数请自行查询其他博客。
# ————————————————
# 版权声明：本文为CSDN博主「国氏一雄」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/xiaohuo0930/article/details/90373181