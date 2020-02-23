from __future__ import absolute_import, unicode_literals

import pytz
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
    # print(id)
    # print(data['task_name'])
    # print(data['cmd_text'])
    # print(data['periodic_task_type'])
    # print(data['timazone_select'])
    # print(data['interval_value'])
    # print(data['time_value'])
    # print(data['periodic_task_type'])
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
        result = create_interval_task(intelval_schedule_obj, id, data)
    return result


# handle_periodic_task
@shared_task
def handle_periodic_task(uid, data_dict):
    task_data = json.loads(data_dict)
    task_name = task_data['periodic_task_name']
    if beatmodels.PeriodicTask.objects.filter(userid=int(uid), name=task_name):
        taskname_used = 'taskname_used'
        result = json.dumps(taskname_used)
        return result
    sechdule_type = task_data['periodic_task_sechdule_type']
    task_command = task_data['periodic_task_command']
    task_timezone = task_data['periodic_task_timezone']
    select_host = task_data['select_host']
    if sechdule_type == 'Corntab':
        corntab_month_val = task_data['corntab_month_val']
        corntab_day_val = task_data['corntab_day_val']
        corntab_weekday_val = task_data['corntab_weekday_val']
        corntab_hour_val = task_data['corntab_hour_val']
        corntab_minute_val = task_data['corntab_minute_val']
        corntab_dict = {
            "user_id": int(uid),
            "cmd_text": task_command,
            "task_type": 'cmd',
            "task_name": task_name,
        }
        if beatmodels.CrontabSchedule.objects.filter(
                minute=corntab_minute_val,
                hour=corntab_hour_val,
                day_of_week=corntab_weekday_val,
                day_of_month=corntab_day_val,
                month_of_year=corntab_month_val,
                timezone=pytz.timezone(task_timezone)  # 把字符串转换成timezone格式
                # timezone=time.timezone(task_timezone),
        ):
            corntab_sechdule_obj = beatmodels.CrontabSchedule.objects.get(
                minute=corntab_minute_val,
                hour=corntab_hour_val,
                day_of_week=corntab_weekday_val,
                day_of_month=corntab_day_val,
                month_of_year=corntab_month_val
            )
        else:
            corntab_sechdule_obj = beatmodels.CrontabSchedule.objects.create(
                minute=corntab_minute_val,
                hour=corntab_hour_val,
                day_of_week=corntab_weekday_val,
                day_of_month=corntab_day_val,
                month_of_year=corntab_month_val
            )
        if corntab_sechdule_obj:
            periodic_task_obj = beatmodels.PeriodicTask.objects.create(
                name=task_name,
                task="Web.tasks.shell_cmd_task",
                crontab=corntab_sechdule_obj,
                args=json.dumps(select_host),
                kwargs=json.dumps(corntab_dict),
                userid=int(uid),
                schedule_type=sechdule_type
            )
            if periodic_task_obj:
                build_crontab_history(uid)
                success_message = 'success'
                result = json.dumps(success_message)
                return result
            else:
                servererror_message = 'servererror'
                result = json.dumps(servererror_message)
                return result
        else:
            servererror_message = 'servererror'
            result = json.dumps(servererror_message)
            return result
    elif sechdule_type == 'Interval':
        result = json.dumps('for future improve[interval]')
        return result
    elif sechdule_type == 'Clocked':
        result = json.dumps('for future improve[clocked]')
        return result
    else:
        result = json.dumps('Do noting')
        return result


# build crontab sechdule type JSON history
def build_crontab_history(uid):
    corntab_task_list = []
    corntab_task_queryset = beatmodels.PeriodicTask.objects.filter(schedule_type='corntab', userid=int(uid))
    for each_task in corntab_task_queryset:
        corntab_list_dict = {
            'task_id': each_task.id,
            'task_name': each_task.name,
            'task_sechdule': 'm:%s-d:%s-w:%s-h:%s-m:%s' % (
                each_task.crontab.month_of_year,
                each_task.crontab.day_of_month,
                each_task.crontab.day_of_week,
                each_task.crontab.hour,
                each_task.crontab.minute,
            ),
            'timezone': str(each_task.crontab.timezone),
            'sechdule_type': each_task.schedule_type,
            'task_status': each_task.enabled
        }
        corntab_task_list.append(corntab_list_dict)

    dir_path = "%s/statics/data/%s/" % (conf.settings.BASE_DIR, uid)
    file_path = "%s/statics/data/%s/crontabtaskhistory.json" % (conf.settings.BASE_DIR, uid)
    all_about_json.write_json_file(dir_path, file_path, corntab_task_list)


# all type of sechdule periodic task delete button task
@shared_task
def all_sechdule_delete_task(uid, taskid):
    try:
        beatmodels.PeriodicTask.objects.get(id=int(taskid)).delete()
        message = "deleteSuccess"
        build_crontab_history(uid)
    except Exception as e:
        message = str(e)
    return message


# all type of sechdule periodic task change status button task
@shared_task
def all_sechdule_status_change_task(uid, taskid, taskstatus):
    uid = json.loads(uid)
    taskid = json.loads(taskid)
    taskstatus = json.loads(taskstatus)
    if taskstatus == False:
        try:
            periodic_task_obj = beatmodels.PeriodicTask.objects.get(id=int(taskid))
            periodic_task_obj.enabled = True
            periodic_task_obj.save()
            message = 'statuschangeTure'
            build_crontab_history(uid)
        except Exception as e:
            message = 'errorNoChange'
    else:
        try:
            periodic_task_obj = beatmodels.PeriodicTask.objects.get(id=int(taskid))
            periodic_task_obj.enabled = False
            periodic_task_obj.save()
            message = 'statuschangeFalse'
            build_crontab_history(uid)
        except Exception as e:
            message = 'errorNoChange'
    result = message
    return result


# all type of sechdule periodic task change Task name button task
@shared_task
def all_sechdule_taskname_change_task(uid,data):
    data = json.loads(data)
    uid = json.loads(uid)
    task_id = data['task_id']
    task_name = data['task_name']
    message = ''
    if beatmodels.PeriodicTask.objects.filter(name=task_name):
        message = 'name_used'
    else:
        task_obj = beatmodels.PeriodicTask.objects.get(id=int(task_id))
        task_obj.name = task_name
        task_obj.save()
        build_crontab_history(uid)
        message = 'success'
    return message

# add host
@shared_task
def add_host_task():
    result = json.dumps('ok')
    return result


# add user IDC tag
@shared_task
def create_user_idc_tag_task(uid,idc_tag):
    message = ''
    idc_tag = json.loads(idc_tag).strip()
    if webmodels.IDC.objects.filter(name=idc_tag,user_id=int(uid)):
        message = 'name_used'
    else:
        webmodels.IDC.objects.create(
            name=idc_tag,
            user_id=int(uid)
        )
        message = 'success'
    result = message
    return result


# add user group tag
@shared_task
def create_user_group_tag_task(uid,group_tag):
    message = ''
    group_tag = json.loads(group_tag).strip()
    if webmodels.UserProfile.objects.get(id=int(uid)).host_group.filter(name=group_tag):
        message = 'name_used'
    else:
        user_obj = webmodels.UserProfile.objects.get(id=int(uid))
        group_obj = webmodels.HostGroup.objects.create(
            name=group_tag
        )
        user_obj.host_group.add(group_obj)
        user_obj.save()
        message = 'success'
    result = message
    return result


# add new host
@shared_task
def create_user_new_host_task(uid,data):
    message = 'name_useeed'
    result = json.dumps(message)
    return result