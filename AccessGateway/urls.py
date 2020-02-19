"""AccessGateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from Web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.access_login, name='access_login'),  # 登录页面
    url(r'^logout/$', views.access_logout, name='access_logout'),  # 登出页面
    url(r'^web_ssh/$', views.web_ssh, name='web_ssh'),
    url(r'^timed_execution/$', views.timed_execution, name='timed_execution'),
    url(r'^corntabs_task/$', views.corntabs_task, name='corntabs_task'),
    url(r'^interval_task/$', views.interval_task, name='interval_task'),
    url(r'^host_record/$', views.host_record, name='host_record'),
    url(r'^host_muilt/$', views.host_muilt, name='host_muilt'),
    url(r'^batch_task_mgr/$', views.batch_task_mgr),
    url(r'^recent_cmd_result_button/$', views.recent_cmd_result_button),
    url(r'^muilt_file_trans/$', views.muilt_file_trans),
    url(r'^host_select_record/$', views.host_select_record),
    url(r'^get_task_result/$', views.get_task_result),
    url(r'^button_onetask_delete/$', views.button_onetask_delete),   # timed_execution页面one time task history提交过来的删除任务按钮
    url(r'^button_interval_delete/$', views.button_interval_delete),   # interval_task 页面interval task history提交过来的删除任务按钮
    url(r'^save_internal_task/$', views.save_internal_task),   # interval_task 页面save_internal_task提交过来的添加任务函数
    # url(r'^celery_test/$', views.celery_test),  # for Celery
    # url(r'^celery_result/$', views.celery_result),  # for Celery
    url(r'^onetime_task/$', views.onetime_task),  # for timed_execution page # onetime_task function in kevin.js
    url(r'^host_filetrans/$', views.host_filetrans, name='host_filetrans'),
]
