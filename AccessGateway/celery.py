from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AccessGateway.settings')
app = Celery('AccessGateway') # 名字是否可以更改？待测试
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks() # 只要在项目创建tasks项目，就会被celery自动发现


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))