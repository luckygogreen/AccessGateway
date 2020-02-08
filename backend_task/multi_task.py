import json
import platform

from Web import models
import subprocess  # 调用进程包
from django import conf


class MultiTaskManager(object):
    def __init__(self, request):
        # print('打印self：', self)  # 打印self： <backend_task.multitask.MultiTaskManager object at 0x04073CA0>
        self.request = request
        self.task_run()

    # 解析命令参数
    def task_parse(self):
        self.task_data = json.loads(self.request.POST.get('task_data'))
        task_type = self.task_data.get('task_type')  # 打印task_typr: cmd
        # print('打印task_typr:', task_type)
        if hasattr(self, task_type):  # 反射，判断backend.multitask.MultiTaskManager 是否有方法cmd
            task_fuc = getattr(self, task_type)  # 反射，相当于 MultiTaskManager.cmd
            task_fuc()
        else:
            print('没有该命令类型')

    # 执行命令参数
    def task_run(self):
        self.task_parse()

    # 批量命令
    def cmd(self):
        """
        1,生成任务在数据库中的记录，拿到任务ID
        2，触发任务不阻塞
        3，返回任务ID给前端
        :return:
        """
        print('Muilt CMD func is ready!!')

        task_obj = models.MultiTask.objects.create(
            tasktype='cmd',
            taskcontent=self.task_data.get('cmd_text'),
            user=self.request.user
        )  # 插入前端传入的CMD 命令
        select_host_ids = set(self.task_data['select_host_ids'])  # set() 用于去重
        # print('打印task_obj：', task_obj)
        task_log_obj = []
        for id in select_host_ids:
            task_log_obj.append(
                models.TaskDetails(
                    task=task_obj, host_to_remote_user_id=id, result='Init'
                )
            )
        # print('打印task_log_obj:', task_log_obj)
        models.TaskDetails.objects.bulk_create(task_log_obj)  # 批量创建添加数据

        sys_type = platform.system()
        print('执行命令的操作系统操作系统：', sys_type)
        if sys_type == 'Windows':
            # print('运行WindowsURL')
            task_url = "python %s/backend_task/run_task.py %s" % (conf.settings.BASE_DIR, task_obj.id)
        else:
            # print('运行MAC或其他平台URL')
            task_url = "python %s/backend_task/run_task.py %s" % (conf.settings.BASE_DIR, task_obj.id)
        print('打印task_url：', task_url)
        cmd_process = subprocess.Popen(task_url, shell='True')
        print('打印进程号:', cmd_process.pid)
        self.task_obj = task_obj

    def file(self):
        # print('File Transfer func is ready!!')
        # print('task_data:', self.task_data)
        # print('select_host_list:', self.task_data['select_host_list'])
        # print('file_trans_type:', self.task_data['file_trans_type'])
        # print('service_path:', self.task_data['service_path'])
        # print('local_path:', self.task_data['local_path'])

        task_obj = models.MultiTask.objects.create(
            tasktype='filetrans',
            taskcontent=json.dumps(self.task_data),
            user=self.request.user
        )
        select_host_id = set(self.task_data['select_host_list'])
        task_log_obj = []
        for id in select_host_id:
            task_log_obj.append(
                models.TaskDetails(
                    task=task_obj, host_to_remote_user_id=id, result='Init'
                )
            )
        # print('打印task_log_obj:', task_log_obj)
        models.TaskDetails.objects.bulk_create(task_log_obj)  # 批量创建添加数据
        task_url = "python %s/backend_task/run_task.py %s" % (conf.settings.BASE_DIR, task_obj.id)
        cmd_process = subprocess.Popen(task_url, shell='True')
        print('打印进程号:', cmd_process.pid)
        self.task_obj = task_obj
