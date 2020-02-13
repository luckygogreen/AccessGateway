# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def testtast():
    print("测试定时任务成功 %s 😁" % time.strftime("%Y-%m-%d %H:%I:%S"))
    return "good,good,good"


@shared_task
def xsum(numbers):
    return sum(numbers)
