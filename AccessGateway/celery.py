from __future__ import absolute_import, unicode_literals # 从python包里面的绝对路径里面导入celery,unicode_literals 是python2,python3做兼容支持的
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AccessGateway.settings')
app = Celery('AccessGateway') # 名字是否可以更改？待测试
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() # 只要在项目创建tasks项目，就会被celery自动发现
# app.conf.update(result_expires=3600,)  任务过期时间


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))