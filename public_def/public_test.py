import os
import json

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessGateway.settings")
    import django

    django.setup()
    import time
    from django_celery_beat import models as beatmodels
    from Web import models as webmodels

# Example PeriodicTask create
# PeriodicTask.objects.create(
#     interval=schedule,
#     name='Importing contacts',
#     task='proj.tasks.import_contacts',
#     args=json.dumps(['arg1', 'arg2']),
#     kwargs=json.dumps({'be_careful': True,}),
#     expires=datetime.utcnow() + timedelta(seconds=30)
# )
    def reset_sun_time():
        from django_celery_beat.models import PeriodicTask, PeriodicTasks
        PeriodicTask.objects.all().update(last_run_at=None)
        for task in PeriodicTask.objects.all():
            PeriodicTasks.changed(task)


    # def test_periodic_task():
    #     periodic_task_obj = beatmodels.PeriodicTask.objects.all()
    #     for i in periodic_task_obj:
    #         print("定时任务：%s, time: %s" % (i.name, i.clocked))
    #
    # def test_create_peridic_task():
    #     periodictask_obj =beatmodels.PeriodicTask.objects.create(
    #         # clocked=beatmodels.ClockedSchedule.objects.get(id=19),
    #         interval = beatmodels.IntervalSchedule.objects.get(id=3),
    #         name = 'yigeheshang',
    #         task = 'Web.tasks.shell_cmd',
    #     )
    #     print("periodictask_obj",periodictask_obj.id)
    #
    # def test_update_periodic_task():
    #     periodictask_obj = beatmodels.PeriodicTask.objects.get(id=15)
    #     periodictask_obj.enabled = False
    #     periodictask_obj.save()

# test_create_peridic_task()
# test_periodic_task()
# test_update_periodic_task()
reset_sun_time()