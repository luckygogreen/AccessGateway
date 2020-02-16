from __future__ import absolute_import, unicode_literals
from celery import shared_task



@shared_task
def new_celery_task():
    print("测试 new_celery_task")
    return "good job"