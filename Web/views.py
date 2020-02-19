import json
from django.shortcuts import render, redirect, HttpResponse
from public_def import Kuser_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from Web import models
from backend_task.multi_task import MultiTaskManager
from backend_task import view_extra
from backend_task.ag_command_history import CommandHistory
from celery.result import AsyncResult
import time
import platform
from django_celery_beat import models as beatmodels
from backend_task.view_extra import get_one_time_task_history,get_interval_task_history_with_request
from Web.tasks import create_interval_schedule


# def celery_test(request):
#     time.sleep(2)
#     task = add.delay(9, 9)
#     res = "%s:%s" % (task.get(), task)
#     return HttpResponse(res)
#     # mul.delay(3,5)
#     # xsum.delay(8)
#
#
# def celery_result(request):
#     task_id = "8ab1e14c-8eae-491a-98db-489d2b7d41cf"
#     res = AsyncResult(id=task_id).result
#     return HttpResponse(res)


# 登录页面
def access_login(request):
    islogin = False
    err_message = ''
    if request.method == 'POST':
        islogin, err_message = Kuser_login.user_login(request)
        if islogin:
            return redirect('/')
    return render(request, 'login.html', {'err_message': err_message})


# 登出页面
def access_logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard(request):
    # 打印系统信息开始
    print("*" * 60)
    print("***【System:%s】***" % platform.platform())
    print("****************【Time:%s】****************" % time.strftime("%Y-%m-%d %H:%I:%S"))
    print("*" * 60)
    info_result = view_extra.get_accessgateway_info(request)  # 获取堡垒机基本信息
    CommandHistory(request)
    # print(command_history.command_history_list)   # 打印数据列表
    return render(request, 'index.html', {
        'host_number': info_result['host_number'],
        'host_group_number': info_result['host_group_number'],
        'cmd_number': info_result['cmd_number'],
        'task_number': info_result['task_number'],
        'task_error_number': info_result['task_error_number'],
        'task_success_number': info_result['task_success_number'],
        'user_number': info_result['user_number']})


# 操作记录页面
@login_required
def host_record(request):
    host_list = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related()
    return render(request, 'host_record.html', {'host_list': host_list})


# 主机页面
@login_required
def web_ssh(request):
    hostlist = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related()
    return render(request, 'web_ssh.html', {'hostlist': hostlist})


# 获取用户权限下的服务器以及服务器组信息
@login_required
def host_hostgroup(request):
    host_obj = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related()
    host_group_obj = models.UserProfile.objects.get(id=request.user.id).host_group.select_related()
    return host_obj, host_group_obj


# 批量命令处理页面
@login_required
def host_muilt(request):
    view_extra.recent_command(request, 'cmd', 30)
    host_obj, host_group_obj = host_hostgroup(request)
    return render(request, 'host_muilt.html', {'host_obj': host_obj, 'host_group_obj': host_group_obj})


# 批量文件传送页面
@login_required
def host_filetrans(request):
    view_extra.recent_command(request, 'file', 30)
    host_obj, host_group_obj = host_hostgroup(request)
    return render(request, 'host_filetrans.html', {'host_obj': host_obj, 'host_group_obj': host_group_obj})


# 定时操作页面
@login_required
def timed_execution(request):
    # 打印系统信息开始
    print("*" * 60)
    print("***【System:%s】***" % platform.platform())
    print("****************【Time:%s】****************" % time.strftime("%Y-%m-%d %H:%I:%S"))
    print("*" * 60)
    # view_extra.recent_command(request, 'cmd', 30)
    host_obj, host_group_obj = host_hostgroup(request)
    return render(request, 'timed_execution.html', {'host_obj': host_obj, 'host_group_obj': host_group_obj})


# 处理timed_execution 页面Ajax提交的一次性任务按钮save_onetime_task  in kevin.js
@login_required
def onetime_task(request):
    result = view_extra.create_onetime_task(request)
    print("result:", result)
    return HttpResponse(json.dumps(result))


# 处理一次性任务timed_execution页面one time task history提交过来的删除任务事件
@login_required
def button_onetask_delete(request):
    print("button_onetask_delete 被执行")
    try:
        beatmodels.PeriodicTask.objects.get(id=int(request.POST.get("seleteid"))).delete()
        message = "Success"
        print("一次性任务被成功删除")
        get_one_time_task_history(request)
    except Exception as e:
        message = str(e)
        print(message)
    return HttpResponse(json.dumps(message))


# 处理周期任务 页面 interval task history提交的删除任务事件
@login_required
def button_interval_delete(request):
    print("button_interval_delete 被执行")
    try:
        beatmodels.PeriodicTask.objects.get(id=int(request.POST.get("seleteid"))).delete()
        message = "Success"
        print("周期性任务被成功删除")
        get_interval_task_history_with_request(request)
    except Exception as e:
        message = str(e)
        print(message)
    return HttpResponse(json.dumps(message))


# 处理CMD提交过来的任务
@login_required
def batch_task_mgr(request):
    mutile_task_obj = MultiTaskManager(request)
    response = {
        'task_id': mutile_task_obj.task_obj.id,
        'select_host_list': list(
            mutile_task_obj.task_obj.taskdetails_set.all().values('id', 'host_to_remote_user__host__ip_addr',
                                                                  'host_to_remote_user__host__name',
                                                                  'host_to_remote_user__remote_user__username'))
    }
    # print('response:', response)
    # view_extra.recent_command(request)
    return HttpResponse(json.dumps(response))


# 处理host_muilt 批量命令页面传回的命令ID，返回该命令所涉及到的所有命令结果和数据
@login_required
def recent_cmd_result_button(request):
    print('recent_cmd_result_button被成功执行')
    result_list = view_extra.get_result_by_cmdid(request.GET.get('cmdid'), request)
    return HttpResponse(json.dumps(result_list))


# 处理所选择的服务器列表
@login_required
def host_select_record(request):
    view_extra.command_history(request)
    return HttpResponse("1")


# 处理传输文件命令
@login_required
def muilt_file_trans(request):
    file_trans_obj = MultiTaskManager(request)
    response = {
        'task_id': file_trans_obj.task_obj.id,
        'select_host_list': list(
            file_trans_obj.task_obj.taskdetails_set.all().values('id', 'host_to_remote_user__host__ip_addr',
                                                                 'host_to_remote_user__host__name',
                                                                 'host_to_remote_user__remote_user__username'))
    }
    return HttpResponse(json.dumps(response))


# 处理连接服务器命令，返回的结果
@login_required
def get_task_result(request):
    task_id = request.GET.get('task_id')
    task_details_obj = models.TaskDetails.objects.filter(task_id=task_id)
    log_data = list(task_details_obj.values('id', 'status', 'result'))
    return HttpResponse(json.dumps(log_data))


@login_required
def interval_task(request):
    # 打印系统信息开始
    print("*" * 60)
    print("***【System:%s】***" % platform.platform())
    print("****************【Time:%s】****************" % time.strftime("%Y-%m-%d %H:%I:%S"))
    print("*" * 60)
    host_obj, host_group_obj = host_hostgroup(request)
    return render(request, 'interval_task.html', {'host_obj': host_obj, 'host_group_obj': host_group_obj})


def save_internal_task(request):
    result = create_interval_schedule.delay(request.user.id, request.POST.get('interval_task_data'))
    return HttpResponse(result.get())


@login_required
def corntabs_task(request):
    # 打印系统信息开始
    print("*" * 60)
    print("***【System:%s】***" % platform.platform())
    print("****************【Time:%s】****************" % time.strftime("%Y-%m-%d %H:%I:%S"))
    print("*" * 60)
    # view_extra.recent_command(request, 'cmd', 30)
    host_obj, host_group_obj = host_hostgroup(request)
    return render(request, 'corntabs_task.html', {'host_obj': host_obj, 'host_group_obj': host_group_obj})
