import platform
import time

from Web import models
import json
from django import conf
from public_def import all_about_json
import datetime
import pytz
from django_celery_beat import models as beatmodels


# 获取Dashboard 页面的基本数字信息，注册人数，分组数，主机数，命令数
def get_accessgateway_info(request):
    # print(request.user)  # 打印登录用户
    info_result = {}
    host_number = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related().count()
    host_group_number = models.UserProfile.objects.get(id=request.user.id).host_group.select_related().count()
    cmd_number = models.UserProfile.objects.get(id=request.user.id).multitask_set.select_related().count()
    user_number = models.UserProfile.objects.all().count()
    task_number = models.TaskDetails.objects.all().count()
    task_error_number = models.TaskDetails.objects.filter(status=2).count()
    task_success_number = models.TaskDetails.objects.filter(status=3).count()
    # print('可操作服务器数', host_number)
    # print('可操作工作组数', host_group_number)
    # print('运行命令数', cmd_number)
    # print('总用户数', user_number)
    info_result['host_number'] = host_number
    info_result['host_group_number'] = host_group_number
    info_result['cmd_number'] = cmd_number
    info_result['user_number'] = user_number
    info_result['task_number'] = task_number
    info_result['task_error_number'] = task_error_number
    info_result['task_success_number'] = task_success_number
    # print("要返回的数组结果：", info_result)
    return info_result


# Dashboard页面的Command History执行方法
def command_history(request):
    select_host_ids = json.loads(request.POST.get("select_host_ids"))
    select_host_result_list = []
    for host_id in select_host_ids:
        task_details_obj = models.TaskDetails.objects.filter(host_to_remote_user_id=host_id).select_related()
        for task in task_details_obj.order_by('-id'):
            if task.task.tasktype == 'filetrans':
                command = 'File Transfer'
            else:
                command = task.task.taskcontent
            select_host_result_dict = {
                'id': task.id,
                'type': task.task.get_tasktype_display(),
                'cmd': command,
                'status': task.get_status_display(),
                'result': task.result,
                'date': task.data.strftime("%Y-%m-%d %H:%I:%S")
            }
            select_host_result_list.append(select_host_result_dict)
    dir_path = "%s/statics/data/%s/" % (conf.settings.BASE_DIR, request.user.id)
    file_path = "%s/statics/data/%s/host_record_result.json" % (conf.settings.BASE_DIR, request.user.id)
    all_about_json.write_json_file(dir_path, file_path, select_host_result_list)  # 调用生成json方法


# host_record批量命令页面，最近操作的命令Recent Command取10条
def recent_command(request, type, show_number):
    selected_type = 'cmd'
    if type == 'file':
        selected_type = 'filetrans'
    print("recent_command成功被执行")
    command_obj = models.UserProfile.objects.get(id=request.user.id).multitask_set.select_related().order_by(
        '-id').filter(tasktype=selected_type)[:show_number]
    recent_command_list = []
    for cmd in command_obj:
        recent_command_dict = {
            'id': cmd.id,
            'cmd': cmd.taskcontent,
            'type': cmd.get_tasktype_display(),
            'userid': cmd.user.id,
            'username': cmd.user.name,
            'useremail': cmd.user.email,
            'date': cmd.data.strftime("%Y-%m-%d %H:%I:%S")
        }
        recent_command_list.append(recent_command_dict)
    dir_path = "%s/statics/data/%s/" % (conf.settings.BASE_DIR, request.user.id)
    file_path = "%s/statics/data/%s/recent_command_%s.json" % (conf.settings.BASE_DIR, request.user.id, selected_type)
    all_about_json.write_json_file(dir_path, file_path, recent_command_list)


# host_muilt处理批量命令页面返回的最新任务详情
def get_result_by_cmdid(cmdid, request):
    print('view_extra.get_result_by_cmdid 被成功执行')
    cmd_obj = models.MultiTask.objects.get(id=cmdid)
    task_obj = models.TaskDetails.objects.filter(task=cmd_obj)
    result_list = []
    for task in task_obj:
        result_dict = {
            'cmdid': cmdid,
            'cmdtype': cmd_obj.get_tasktype_display(),
            'command': cmd_obj.taskcontent,
            'userid': cmd_obj.user.id,
            'username': cmd_obj.user.name,
            'useremail': cmd_obj.user.email,
            'taskid': task.id,
            'taskip': task.host_to_remote_user.host.ip_addr,
            'taskport': task.host_to_remote_user.host.port,
            'taskstatus': task.get_status_display(),
            'taskresult': task.result,
            'taskdate': task.data.strftime("%Y-%m-%d %H:%I:%S")

        }
        result_list.append(result_dict)
    dir_path = "%s/statics/data/%s/" % (conf.settings.BASE_DIR, request.user.id)
    file_path = "%s/statics/data/%s/get_result_by_cmdid.json" % (conf.settings.BASE_DIR, request.user.id)
    all_about_json.write_json_file(dir_path, file_path, result_list)

    return result_list


# timed_execution 页面提交的ajax一次性保存任务
def create_onetime_task(request):
    result = creat_clock_schedule(request)
    return result

def get_one_time_task_history(request):
    one_time_task_history_list = []
    one_time_task_history_obj = beatmodels.PeriodicTask.objects.filter(userid=request.user.id)

    for each_task in one_time_task_history_obj:
        if each_task.clocked:
            one_time_task_history_dict = {
                'task_id':each_task.id,
                'task_name':each_task.name,
                'task_time':str(each_task.clocked.clocked_time),
                'task_status':each_task.enabled,
            }
            one_time_task_history_list.append(one_time_task_history_dict)
    dir_path = "%s/statics/data/%s/" % (conf.settings.BASE_DIR,request.user.id)
    file_path = "%s/statics/data/%s/onetimetaskhistory.json" % (conf.settings.BASE_DIR,request.user.id)
    all_about_json.write_json_file(dir_path,file_path,one_time_task_history_list)

def creat_clock_schedule(request):
    task_data = json.loads(request.POST.get('task_data'))
    task_name = task_data.get('task_name')
    cmd_text = task_data.get('cmd_text')
    date_picker = task_data.get('date_picker')
    timazone_select = task_data.get('timazone_select')
    time_picker = task_data.get('time_picker')
    user_id = task_data.get('user_id')
    select_host_ids = task_data.get('select_host_ids')
    print("task name :", task_name)
    if beatmodels.PeriodicTask.objects.filter(name=task_name):
        result = 2
        return result
    else:
        print("%s 任务名有效：" % task_name)

    new_date = date_picker.split('/', -1)  # 把日期分割全部取出,取出后是列表格式
    new_time_hour = time_picker.split(':', -1)[0]  # 把时间按照分割,取第一位,小时
    new_time_mins = int(time_picker.split(':', -1)[1].split(' ', -1)[0])  # 把分割后的时间按照空格再次分割,取出来是分钟和上下午标识
    if time_picker.split(':', -1)[1].split(' ', -1)[1] == "PM" and new_time_hour != "12":  # 判断是否是PM下午
        new_time_hour = int(new_time_hour) + 12  # 如果是+12小时转换成24小时制
    data_time = "%s-%s-%s %s:%s:%s" % (new_date[2], new_date[0], new_date[1], new_time_hour, new_time_mins, '00')  # 将分割后的数据整理成固定格式的字符串
    data_time_really = datetime.datetime.strptime(data_time, "%Y-%m-%d %H:%M:%S")  # 将字符串转换成datatime格式
    tz = pytz.timezone(timazone_select)  # 获取当前时区对应的时区格式的数据
    print("tz:", tz)
    data_time_timezone = tz.localize(data_time_really)
    # data_time_timezone = data_time_really.replace(tzinfo=tz)  # 把转换好的 datetime 格式,替换为有时区的 datetime 格式 这个转换时间会有18分钟的误差,时区不对
    # print('data_time_really:',data_time_really)  # 打印未加时区的日期   2020-02-20 18:45:00
    # print('data_time_timezone:',data_time_timezone)   # 打印加过时区后的日期格式  2020-02-20 18:45:00+08:06
    if beatmodels.ClockedSchedule.objects.filter(clocked_time=data_time_timezone):
        clocked_schedule_obj = beatmodels.ClockedSchedule.objects.get(clocked_time=data_time_timezone)
    else:
        clocked_schedule_obj = beatmodels.ClockedSchedule.objects.create(clocked_time=data_time_timezone)

    print("data_time_really:", data_time_really)
    print("data_time_timezone:", data_time_timezone)
    print("tz.localize(datetime.datetime.now()):", tz.localize(datetime.datetime.now()))
    print("clocked_schedule_obj.clocked_time:", clocked_schedule_obj.clocked_time)
    print("datetime.datetime.now().replace(tzinfo=tz)", datetime.datetime.now().replace(tzinfo=tz))

    if clocked_schedule_obj:
        new_periodic_task_obj = creat_periodic_task(clocked_schedule_obj, task_name, cmd_text, 'cmd', user_id, select_host_ids,request)
        return new_periodic_task_obj
    else:
        result = 0
        return result


def creat_periodic_task(clocked_schedule_obj, task_name, cmd_text, task_type, user_id, select_host_ids,request):
    print("user_id", type(user_id), user_id)
    task_dict = {
        "user_id": user_id,
        "cmd_text": cmd_text,
        "task_type": task_type,
        "task_name": task_name,
    }
    periodic_task_obj = beatmodels.PeriodicTask.objects.create(
        name=task_name,
        task="Web.tasks.shell_cmd_task",
        clocked=clocked_schedule_obj,
        one_off=True,
        args=json.dumps(select_host_ids),
        kwargs=json.dumps(task_dict),
        userid=int(user_id)
    )
    print("任务表的时间：", periodic_task_obj.clocked.clocked_time)
    print("一次性任务名：", task_name)
    print("一次性任务ID：", periodic_task_obj.id)
    get_one_time_task_history(request)
    result = periodic_task_obj.id
    return result
