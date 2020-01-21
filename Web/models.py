from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.

# 服务器表
class Host(models.Model):
    name = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.SmallIntegerField(default=22)
    idc = models.ForeignKey("IDC", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# 服务器机组
class HostGroup(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # hosts = models.ManyToManyField("Host")
    host_to_remote_users = models.ManyToManyField("HostToRemoteUser")

    def __str__(self):
        return self.name


# 服务器和登录账号关联
class HostToRemoteUser(models.Model):
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    remote_user = models.ForeignKey("RemoteUser", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("host", "remote_user")

    def __str__(self):
        return "%s %s" % (self.host, self.remote_user)


# 服务器登录账号
class RemoteUser(models.Model):
    auth_type_choices = ((0, 'ssh-password'), (1, 'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        unique_together = ('auth_type', 'username', 'password')

    def __str__(self):
        return "%s:%s" % (self.username, self.password)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


# 堡垒机账号
class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,

    )
    name = models.CharField(max_length=64, verbose_name="姓名")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserProfileManager()
    host_to_remote_users = models.ManyToManyField("HostToRemoteUser", blank=True, null=True)
    host_group = models.ManyToManyField("HostGroup", blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email


# 机房信息
class IDC(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


# 存储审计日志
class AuditLog(models.Model):
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name="堡垒机账号", null=True, blank=True)
    host_to_remote_user = models.ForeignKey("HostToRemoteUser", on_delete=models.CASCADE, null=True, blank=True)
    log_type_choices = ((0, 'login'), (1, 'cmd'), (2, 'logout'))
    log_type = models.SmallIntegerField(choices=log_type_choices, default=0)
    content = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.host_to_remote_user, self.content)


# 存储任务信息，大任务
class MultiTask(models.Model):
    task_type_choices = (
        ('cmd', 'CMD'),
        ('filetrans', 'FILES'),
    )
    tasktype = models.CharField(max_length=32, choices=task_type_choices)
    taskcontent = models.CharField(max_length=256, verbose_name='Task content')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.taskcontent


# 存储任务信息返回的个线程数据，小任务
class TaskDetails(models.Model):
    task = models.ForeignKey(MultiTask, on_delete=models.CASCADE)
    host_to_remote_user = models.ForeignKey(HostToRemoteUser, on_delete=models.CASCADE)
    status_choices = (
        (0,'initialized'),
        (1,'timeout'),
        (2,'Error'),
        (3,'Success'),
    )
    status = models.PositiveIntegerField(choices=status_choices,default=0)
    result = models.TextField(verbose_name='CMD result')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result
