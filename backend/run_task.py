import os, sys, time
import paramiko
from concurrent.futures import ThreadPoolExecutor

def ssh_command(sub_task_obj):
    print('ssh_command方法已被执行')
    host_remote_user_obj = sub_task_obj.host_to_remote_user
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('连接IP：', host_remote_user_obj.host.ip_addr, '端口：', host_remote_user_obj.host.port, '用户名:', host_remote_user_obj.remote_user.username, '密码：', host_remote_user_obj.remote_user.password)
    ssh.connect(
        hostname=host_remote_user_obj.host.ip_addr,
        # port=host_remote_user_obj.host.port,
        port=22,
        username=host_remote_user_obj.remote_user.username,
        password=host_remote_user_obj.remote_user.password
    )
    print('执行命令：', sub_task_obj.task.taskcontent)
    stdin, stdout, stderr = ssh.exec_command(sub_task_obj.task.taskcontent)
    stdout_result = stdout.read()
    stderr_result = stderr.read()
    sub_task_obj.result = stdout_result + stderr_result
    print('执行stdout_result：', sub_task_obj.result)
    print('执行stderr_result：', sub_task_obj.result)
    print('执行结果：', sub_task_obj.result)
    if stderr:
        sub_task_obj.status = 2
    else:
        sub_task_obj.status = 1
    sub_task_obj.save()
    ssh.close()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessGateway.settings")
    import django

    django.setup()
    from Web import models

    print('打印:sys.argv', sys.argv)
    print('打印:len(sys.argv)', len(sys.argv))
    print('打印:sys.argv[0]', sys.argv[0])
    if len(sys.argv) == 1:
        exit('程序终止')
    else:
        task_id = sys.argv[1]
        print('打印:sys.argv[1]', sys.argv[1])
        task_obj = models.MultiTask.objects.get(id=task_id)
        print('任务启动')
        pool = ThreadPoolExecutor(10)
        ssh_command(task_obj.taskdetails_set.last())
        # for sub_task_obj in task_obj.taskdetails_set.all():
        #     print('111')
        #     pool.submit(ssh_command, sub_task_obj)
        # pool.shutdown(wait=True)

        # # 测试用
        # print('获取任务信息成功')
        # time.sleep(5)
        # task_obj.taskcontent = 'test task success'
        # task_obj.save()
        # print('返回结果已经输入到数据库')
