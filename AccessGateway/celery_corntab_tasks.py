# from __future__ import absolute_import,unicode_literals
from celery import Celery
from celery.schedules import crontab

app = Celery()

#  当celery 调用定时任务时，会把定时任务交给celery_beat处理，celery beat监听到任务后才交给redis处理
@app.on_after_configure.connect       # on_after_configure.connect = 函数启动就立刻执行下面的函数
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 5 seconds.
    sender.add_periodic_task(5.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 10 seconds
    sender.add_periodic_task(10.0, test.s('world'), expires=10)  # .s相当于 delay()  # expires=10 就是任务结果保存10秒

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=12, minute=50, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    print(arg)