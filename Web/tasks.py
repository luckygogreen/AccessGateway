from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django import conf
import subprocess
import json
import paramiko
from Web import models as webmodels
from concurrent.futures import ThreadPoolExecutor
import time


@shared_task(typing=False)
def shell_cmd_task(*args, **kwargs):
    host_id_list = set(args)
    #############取出所有传入的参数核对数据Begin#############
    # for arg in host_id_list:
    #     print('列表值:%s,类型:%s' %(arg,type(arg)))
    # print("user_id:",kwargs["user_id"])
    # print("cmd_text:",kwargs["cmd_text"])
    # print("task_type:",kwargs["task_type"])
    # print("task_name:",kwargs["task_name"])
    #############取出所有传入的参数核对数据End##############
    task_obj = webmodels.MultiTask.objects.create(
        tasktype=kwargs["task_type"],
        taskcontent=kwargs["cmd_text"],
        user=webmodels.UserProfile.objects.get(id=int(kwargs["user_id"])),
        task_name=kwargs["task_name"]
    )
    task_log_list = []
    for id in host_id_list:
        task_log_list.append(
            webmodels.TaskDetails(
                task=task_obj, host_to_remote_user_id=int(id), result='Init'
            )
        )
    print("task_log_list:", task_log_list)
    webmodels.TaskDetails.objects.bulk_create(task_log_list)  # 批量创建添加数据  接入list参数
    task_url = "python %s/backend_task/run_task.py %s" % (conf.settings.BASE_DIR, task_obj.id)
    cmd_process = subprocess.Popen(task_url, shell='True')
    print('打印进程号:', cmd_process.pid)


@shared_task
def test_task():
    print("测试 shell_cmd")
    return "good job"
