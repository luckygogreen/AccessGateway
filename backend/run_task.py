import os, sys, time
import paramiko
from concurrent.futures import ThreadPoolExecutor


def ssh_command(sub_task_obj):
    time.sleep(2)
    print('ssh_command方法已被执行')
    print('接受传入的参数：', sub_task_obj)
    host_remote_user_obj = sub_task_obj.host_to_remote_user
    print('获取host_remote_user_obj信息')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('连接IP：', host_remote_user_obj.host.ip_addr, '端口：', host_remote_user_obj.host.port, '用户名:', host_remote_user_obj.remote_user.username, '密码：', host_remote_user_obj.remote_user.password)
    try:
        ssh.connect(
            hostname=host_remote_user_obj.host.ip_addr,
            # port=host_remote_user_obj.host.port,
            port=22,
            username=host_remote_user_obj.remote_user.username,
            password=host_remote_user_obj.remote_user.password,
            # timeout=10
        )
        print('执行命令：', sub_task_obj.task.taskcontent)
        # stdin, stdout, stderr = ssh.exec_command(". ./.bash_profile;echo $PATH")
        stdin, stdout, stderr = ssh.exec_command(sub_task_obj.task.taskcontent)
        stdout_result = stdout.read()
        stderr_result = stderr.read()
        sub_task_obj.result = stdout_result + stderr_result
        print('执行结果：', sub_task_obj.result)
        if stderr_result:
            print('有错误，status=2')
            sub_task_obj.status = 2
        else:
            sub_task_obj.status = 3
            print('命令正确，status=3')
    except Exception as e:
        print('e:', e)
        sub_task_obj.status = 2
        print('有错误e，status=2')
        sub_task_obj.result = e
    sub_task_obj.save()
    print('已更新数据库')
    print('-' * 30, '以上是', sub_task_obj.id, '的输出结果', '-' * 30)
    ssh.close()


if __name__ == "__main__":
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys.path.append(base_dir)
    # print('sys.path:',sys.path)
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
        pool_number = task_obj.taskdetails_set.all().count()  # 获取一共取出多少条数据   用到反向查找  _set
        print('开启线程条数：', pool_number)
        pool = ThreadPoolExecutor(pool_number)  # 初始化线程池 定义开启多少线程
        # ssh_command(task_obj.taskdetails_set.last()) # 测试用来查看ssh_command的方法是否执行成功
        for sub_task_obj in task_obj.taskdetails_set.all():
            pool.submit(ssh_command, sub_task_obj)
        print('-' * 30, '以下是所有进程的输出结果', '-' * 30)
        pool.shutdown(wait=True)

        # # 测试用
        # print('获取任务信息成功')
        # time.sleep(5)
        # task_obj.taskcontent = 'test task success'
        # task_obj.save()
        # print('返回结果已经输入到数据库')
