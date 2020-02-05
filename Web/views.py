import json

from django.shortcuts import render, redirect, HttpResponse
from public_def import Kuser_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from Web import models
from backend.multi_task import MultiTaskManager
from backend import ag_info
from backend.host_info import SSHHost
from backend.ag_command_history import CommandHistory


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
    info_result = ag_info.get_accessgateway_info(request)  # 获取堡垒机基本信息
    command_history = CommandHistory(request)
    # print(command_history.command_history_list)   # 打印数据列表
    return render(request, 'index.html', {'host_number': info_result['host_number'], 'host_group_number': info_result['host_group_number'], 'cmd_number': info_result['cmd_number'], 'user_number': info_result['user_number']})
# 操作记录页面
@login_required
def host_record(request):
    host_list = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related()
    return render(request,'host_record.html',{'host_list':host_list})

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
    host_obj, host_group_obj = host_hostgroup(request)
    return render(request, 'host_muilt.html', {'host_obj': host_obj, 'host_group_obj': host_group_obj})


# 批量文件传送页面
@login_required
def host_filetrans(request):
    host_obj, host_group_obj = host_hostgroup(request)
    return render(request, 'host_filetrans.html', {'host_obj': host_obj, 'host_group_obj': host_group_obj})

# 定时操作页面
@login_required
def timed_execution(request):
    return render(request,'timed_execution.html')

# 处理CMD提交过来的任务
@login_required
def batch_task_mgr(request):
    mutile_task_obj = MultiTaskManager(request)
    response = {
        'task_id': mutile_task_obj.task_obj.id,
        'select_host_list': list(mutile_task_obj.task_obj.taskdetails_set.all().values('id', 'host_to_remote_user__host__ip_addr', 'host_to_remote_user__host__name', 'host_to_remote_user__remote_user__username'))
    }
    print('response:', response)
    return HttpResponse(json.dumps(response))

# 处理所选择的服务器列表
@login_required
def host_select_record(request):
    ag_info.write_select_host_task_to_json(request)
    return HttpResponse("ok")

# 处理传输文件命令
@login_required
def muilt_file_trans(request):
    file_trans_obj = MultiTaskManager(request)
    response = {
        'task_id': file_trans_obj.task_obj.id,
        'select_host_list': list(file_trans_obj.task_obj.taskdetails_set.all().values('id', 'host_to_remote_user__host__ip_addr', 'host_to_remote_user__host__name', 'host_to_remote_user__remote_user__username'))
    }
    return HttpResponse(json.dumps(response))


# 处理连接服务器命令，返回的结果
@login_required
def get_task_result(request):
    task_id = request.GET.get('task_id')
    task_details_obj = models.TaskDetails.objects.filter(task_id=task_id)
    log_data = list(task_details_obj.values('id', 'status', 'result'))
    return HttpResponse(json.dumps(log_data))

