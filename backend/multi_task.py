
import json
import platform

from Web import models
import subprocess  # 调用进程包
from django import conf


class MultiTaskManager(object):
    def __init__(self, request):
        print('打印self：', self)  # 打印self： <backend.multitask.MultiTaskManager object at 0x04073CA0>
        self.request = request
        self.task_run()

    # 解析命令参数
    def task_parse(self):
        self.task_data = json.loads(self.request.POST.get('task_data'))
        task_type = self.task_data.get('task_type')  # 打印task_typr: cmd
        print('打印task_typr:', task_type)
        if hasattr(self, task_type):  # 反射，判断backend.multitask.MultiTaskManager 是否有方法cmd
            print('进入反射')
            task_fuc = getattr(self, task_type)  # 反射，相当于 MultiTaskManager.cmd
            print('打印self2:', self)
            print('打印反射结果：', task_fuc)
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
        print('批量命令函数已经启动')

        task_obj = models.MultiTask.objects.create(
            tasktype='cmd',
            taskcontent=self.task_data.get('cmd_text'),
            user=self.request.user
        )  # 插入前端传入的CMD 命令
        select_host_ids = set(self.task_data['select_host_ids'])  # set() 用于去重
        print('打印task_obj：', task_obj)
        task_log_obj = []
        for id in select_host_ids:
            task_log_obj.append(
                models.TaskDetails(
                    task=task_obj, host_to_remote_user_id=id, result='Init...%s' % (id)
                )
            )
        print('打印task_log_obj:', task_log_obj)
        models.TaskDetails.objects.bulk_create(task_log_obj)  # 批量创建添加数据

        # 方法1，运行run_task方法，调用单独脚本，取路径,全新进程
        sys_type = platform.system()
        print('打印操作系统：', sys_type)
        if sys_type == 'Windows':
            print('运行WindowsURL')
            task_url = "python %s/backend/run_task.py %s" % (conf.settings.BASE_DIR, task_obj.id)
        else:
            print('运行MAC或其他平台URL')
            task_url = "python %s/backend/run_task.py %s" % (conf.settings.BASE_DIR, task_obj.id)
        print('打印task_url：', task_url)
        cmd_process = subprocess.Popen(task_url, shell='True')
        self.task_id = task_obj.id

        # # 方法2，运行run_task方法,直接调用函数方法，同一个进程
        # run_task.task_runner(task_obj.id)
        # self.task_id = task_obj.id
