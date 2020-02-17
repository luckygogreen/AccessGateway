from __future__ import absolute_import, unicode_literals
import pymysql
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']
pymysql.install_as_MySQLdb()  # 告诉django用pymysql代替mysqldb连接数据库