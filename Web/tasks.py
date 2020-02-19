from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django import conf
import subprocess
import json
import paramiko
from Web import models as webmodels
from django_celery_beat import models as beatmodels
from concurrent.futures import ThreadPoolExecutor
import time
from public_def import all_about_json
from backend_task.view_extra import create_interval_task

@shared_task(typing=False)
def shell_cmd_task(*args, **kwargs):
    print("shell_cmd_task启动")
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
    # print("task_log_list:", task_log_list)
    webmodels.TaskDetails.objects.bulk_create(task_log_list)  # 批量创建添加数据  接入list参数
    task_url = "python %s/backend_task/run_task.py %s" % (conf.settings.BASE_DIR, task_obj.id)
    rewrite_task_status.delay(kwargs["user_id"])
    cmd_process = subprocess.Popen(task_url, shell='True')
    print('打印进程号:', cmd_process.pid)


@shared_task
def test_task():
    print("测试 shell_cmd")
    return "good job"


@shared_task
def rewrite_task_status(userid):
    print("rewrite_task_status启动")
    one_time_task_history_list = []
    one_time_task_history_obj = beatmodels.PeriodicTask.objects.filter(userid=int(userid))

    for each_task in one_time_task_history_obj:
        if each_task.clocked:
            one_time_task_history_dict = {
                'task_id': each_task.id,
                'task_name': each_task.name,
                'task_time': str(each_task.clocked.clocked_time),
                'task_status': each_task.enabled,
            }
            one_time_task_history_list.append(one_time_task_history_dict)
    dir_path = "%s/statics/data/%s/" % (conf.settings.BASE_DIR, userid)
    file_path = "%s/statics/data/%s/onetimetaskhistory.json" % (conf.settings.BASE_DIR, userid)
    all_about_json.write_json_file(dir_path, file_path, one_time_task_history_list)


# 创建周期任务时间数据
@shared_task
def create_interval_schedule(id, data):
    data = json.loads(data)
    print(id)
    print(data['task_name'])
    print(data['cmd_text'])
    print(data['periodic_task_type'])
    print(data['timazone_select'])
    print(data['interval_value'])
    print(data['time_value'])
    print(data['periodic_task_type'])
    if beatmodels.PeriodicTask.objects.filter(name=data['task_name']):
        result = json.dumps('taskname_used')
    else:
        if beatmodels.IntervalSchedule.objects.filter(every=int(data['interval_value']), period=data['time_value']):
            intelval_schedule_obj = beatmodels.IntervalSchedule.objects.get(
                every=int(data['interval_value']),
                period=data['time_value']
            )
        else:
            intelval_schedule_obj = beatmodels.IntervalSchedule.objects.create(
                every=int(data['interval_value']),
                period=data['time_value']
            )
        result = create_interval_task(intelval_schedule_obj,id, data)
    return result

