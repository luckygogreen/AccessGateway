from django.contrib import admin
from Web import models


admin.site.register(models.Host)
admin.site.register(models.HostGroup)
admin.site.register(models.HostToRemoteUser)
admin.site.register(models.IDC)
admin.site.register(models.UserProfile)
admin.site.register(models.RemoteUser)
