from Web import models
import json, os
from django import conf
from public_function import all_about_json


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
    print("要返回的数组结果：", info_result)
    return info_result


# 判断是否存在Json文件，如果不存在则写入Json文件
def write_select_host_task_to_json(request):
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
                'type':task.task.get_tasktype_display(),
                'cmd': command,
                'status': task.get_status_display(),
                'result': task.result,
                'date': task.data.strftime("%Y-%m-%d %H:%I:%S")
            }
            select_host_result_list.append(select_host_result_dict)
    dir_path = "%s/statics/data/%s/" % (conf.settings.BASE_DIR, request.user.id)
    file_path = "%s/statics/data/%s/host_record_result.json" % (conf.settings.BASE_DIR, request.user.id)
    all_about_json.write_json_file(dir_path, file_path, select_host_result_list)  # 调用生成json方法
