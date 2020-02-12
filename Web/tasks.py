# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y

@shared_task
def testtast():
    print("测试定时任务成功")
    return "super ok"


@shared_task
def xsum(numbers):
    return sum(numbers)

