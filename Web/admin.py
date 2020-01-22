from django.contrib import admin
from Web import models

class MultiTaskAdmin(admin.ModelAdmin):
    list_display = ('id','tasktype','taskcontent','user','data')

class TaskDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','task','host_to_remote_user','status','result','data')

admin.site.register(models.Host)
admin.site.register(models.HostGroup)
admin.site.register(models.HostToRemoteUser)
admin.site.register(models.IDC)
admin.site.register(models.UserProfile)
admin.site.register(models.RemoteUser)
admin.site.register(models.AuditLog)
admin.site.register(models.MultiTask,MultiTaskAdmin)
admin.site.register(models.TaskDetails,TaskDetailsAdmin)
