from Web import models


def get_accessgateway_info(request):
    # print(request.user)  # 打印登录用户
    info_result = {}
    host_number = models.UserProfile.objects.get(id=request.user.id).host_to_remote_users.select_related().count()
    host_group_number = models.UserProfile.objects.get(id=request.user.id).host_group.select_related().count()
    cmd_number = models.UserProfile.objects.get(id=request.user.id).multitask_set.select_related().count()
    user_number = models.UserProfile.objects.all().count()
    print('可操作服务器数', host_number)
    print('可操作工作组数', host_group_number)
    print('运行命令数', cmd_number)
    print('总用户数', user_number)
    info_result['host_number'] = host_number
    info_result['host_group_number'] = host_group_number
    info_result['cmd_number'] = cmd_number
    info_result['user_number'] = user_number
    print("要返回的数组结果：",info_result)
    return info_result

