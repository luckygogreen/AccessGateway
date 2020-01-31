import json

from django.shortcuts import render, redirect, HttpResponse
from public_def import Kuser_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from Web import models
from backend.multi_task import MultiTaskManager


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
    return redirect('/login')


@login_required
def dashboard(request):
    print(request.user)
    return render(request, 'index.html')
    # return render(request, 'tables-bootstrap.html')


# 主机页面
@login_required
def web_ssh(request):
    hostlist = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related()
    return render(request, 'web_ssh.html', {'hostlist': hostlist})


@login_required
def host_muilt(request):
    host_obj = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related()
    host_group_obj = models.UserProfile.objects.get(id=request.user.id).host_group.select_related()
    return render(request, 'host_muilt.html', {'host_obj': host_obj, 'host_group_obj': host_group_obj})


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


# 处理连接服务器命令，返回的结果
@login_required
def get_task_result(request):
    task_id = request.GET.get('task_id')
    task_details_obj = models.TaskDetails.objects.filter(task_id=task_id)
    log_data = list(task_details_obj.values('id', 'status', 'result'))
    return HttpResponse(json.dumps(log_data))


# 批量文件页面
@login_required
def host_filetrans(request):
    return render(request, 'host_filetrans.html')
