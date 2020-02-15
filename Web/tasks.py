# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time

@shared_task
def shell_cmd_task():
    print("测试 shell_cmd")

