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
    url(r'^host_record/$', views.host_record, name='host_record'),
    url(r'^host_muilt/$', views.host_muilt, name='host_muilt'),
    url(r'^batch_task_mgr/$', views.batch_task_mgr),
    url(r'^recent_cmd_result_button/$', views.recent_cmd_result_button),
    url(r'^muilt_file_trans/$', views.muilt_file_trans),
    url(r'^host_select_record/$', views.host_select_record),
    url(r'^get_task_result/$', views.get_task_result),
    url(r'^host_filetrans/$', views.host_filetrans, name='host_filetrans'),
]
