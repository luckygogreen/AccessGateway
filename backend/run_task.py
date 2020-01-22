# 方法1，运行run_task方法1，调用单独脚本，取路径
import os, sys, time

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
        print('获取任务信息成功')

        time.sleep(5)
        task_obj.taskcontent = 'test task success'
        task_obj.save()
        print('返回结果已经输入到数据库')


# # 方法2，运行run_task方法,直接调用函数方法
# from Web import models
# import time
# def task_runner(task_id):
#     if task_id:
#         task_obj = models.MultiTask.objects.get(id=task_id)
#         print('获取任务信息成功')
#
#         time.sleep(15)
#         task_obj.taskcontent = 'test task success'
#         task_obj.save()
#         print('返回结果已经输入到数据库')
