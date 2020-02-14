import os
from public_def import all_about_json
from django import conf
import time,datetime


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessGateway.settings")
    import django
    django.setup()
    import pytz
    from django_celery_beat import models as beatmodels

    def list_timezone():
        timezone_list = []
        for tz in pytz.all_timezones:
            timezone_list.append(tz)
        print(timezone_list)
        dir_path = "%s/statics/data/public/" % conf.settings.BASE_DIR
        file_path = "%s/statics/data/public/timezone.json" % conf.settings.BASE_DIR
        all_about_json.write_json_file(dir_path,file_path,timezone_list)

    def test_timezone():
        dt = "2016-05-05 20:28:54"
        # dt1 = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        dt2 = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        tz = pytz.timezone('Asia/Thimbu')
        dt4 = dt2.replace(tzinfo=tz)
        print("dt2",dt2)
        print(type(dt2))
        print("dt4",dt4)
        print(type(dt4))

# test_timezone()
list_timezone()