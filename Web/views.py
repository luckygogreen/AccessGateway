from django.shortcuts import render, redirect, HttpResponse
from public_def import Kuser_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from Web import models


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
    return render(request, 'web_ssh.html')


# 批量命令页面
@login_required
def host_muilt(request):
    hostlist_with_group = {}
    hostlist = []
    host_group = models.UserProfile.objects.get(id=request.user.id).host_group.select_related()  # 查询登录用户的授权服务器组
    for u_group in host_group:  # 循环服务器组，获取单个组名
        host_user = u_group.host_to_remote_users.select_related()  # 获取该组名下的所有服务器列表和登录账户
        host_list = []
        for each_host_user in host_user:
            host_id = each_host_user.host.id
            host_name = each_host_user.host.name
            host_ip = each_host_user.host.ip_addr
            host_list.append([host_id,host_name,host_ip])
        hostlist_with_group[u_group.name] = host_list
    host_obj = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related()
    return render(request, 'host_muilt.html',{'hostlist_with_group':hostlist_with_group,'host_obj':host_obj})


# 批量文件页面
@login_required
def host_filetrans(request):
    return render(request, 'host_filetrans.html')
