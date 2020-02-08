import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessGateway.settings")
    import django
    django.setup()
    import pytz

    def list_timezone():
        list
        for tz in pytz.all_timezones:
            print(tz)

list_timezone()