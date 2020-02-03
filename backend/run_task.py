import os, sys, time
import paramiko
import json
from concurrent.futures import ThreadPoolExecutor


# 处理普通命令参数
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
            port=host_remote_user_obj.host.port,
            username=host_remote_user_obj.remote_user.username,
            password=host_remote_user_obj.remote_user.password,
            # timeout=10
        )
        print('执行命令：', sub_task_obj.task.taskcontent)
        # stdin, stdout, stderr = ssh.exec_command(". ./.bash_profile;echo $PATH")
        stdin, stdout, stderr = ssh.exec_command(sub_task_obj.task.taskcontent)
        stdout_result = stdout.read()
        stderr_result = stderr.read()
        print('打印stdout.read()的返回结果类型:', type(stdout_result))
        sub_task_obj.result = str(stdout_result + stderr_result, 'utf-8')  # 需要byte 类型的字节转换成 utf-8类型，否者输出结果b'.......\ns
        print('打印stdout.read()的返回结果:', sub_task_obj.result)
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


# 处理文件上传命令参数
def sftp_file(sub_task_obj, task_data):
    time.sleep(2)
    host_remote_user_obj = sub_task_obj.host_to_remote_user
    host_ip = host_remote_user_obj.host.ip_addr
    host_port = host_remote_user_obj.host.port
    login_username = host_remote_user_obj.remote_user.username
    login_password = host_remote_user_obj.remote_user.password

    try:
        # host_connect = paramiko.Transport((host_ip, host_port))
        host_connect = paramiko.Transport(host_ip, host_port)
        host_connect.connect(username=login_username, password=login_password)
        sftp = paramiko.SFTPClient.from_transport(host_connect)
        if task_data['file_trans_type'] == 'sendto':
            sftp.put(task_data['local_path'], task_data['service_path'])  # SFTP上传文件
            result_msg = "The file has been successfully uploaded to the target server.File location:%s" % task_data['service_path']
        else:
            local_file_path = conf.settings.DOWNLOAD_PATH
            if not os.path.isdir("%s%s" % (local_file_path, task_obj.id)):
                os.mkdir("%s%s" % (local_file_path, task_obj.id))
            filename = "%s_%s" % (sub_task_obj.host_to_remote_user.host.ip_addr, task_data["service_path"].split('/')[-1])  # split用/分割，取-1最后一个
            sftp.get(task_data["service_path"], "%s%s/%s" % (local_file_path, sub_task_obj.task.id, filename))  # SFTP下载文件
            result_msg = "The file has been successfully downloaded locally from the target server.Server location:%s" % task_data['service_path']
        host_connect.close()
        sub_task_obj.status = 3
        sub_task_obj.result = result_msg
    except Exception as e:
        print('e:', e)
        sub_task_obj.status = 2
        sub_task_obj.result = e
    sub_task_obj.save()



if __name__ == "__main__":
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys.path.append(base_dir)
    # print('sys.path:',sys.path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessGateway.settings")
    import django

    django.setup()
    from Web import models
    from django import conf

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

        if task_obj.tasktype == 'filetrans':
            task_data = json.loads(task_obj.taskcontent)
            for sub_task_obj in task_obj.taskdetails_set.all():
                pool.submit(sftp_file, sub_task_obj, task_data)
        elif task_obj.tasktype == 'cmd':
            for sub_task_obj in task_obj.taskdetails_set.all():
                pool.submit(ssh_command, sub_task_obj)
        else:
            print('Your operation is illegal, the system will feedback your operation to the administrator')
        pool.shutdown(wait=True)

        # # 测试用
        # print('获取任务信息成功')
        # time.sleep(5)
        # task_obj.taskcontent = 'test task success'
        # task_obj.save()
        # print('返回结果已经输入到数据库')
