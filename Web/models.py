from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# 服务器表
class Host(models.Model):
    name = models.CharField(max_length=128, unique=True)  # 存服务器名称
    ip_address = models.GenericIPAddressField(unique=True)  # 用来存IP地址的字段
    ip_port = models.SmallIntegerField(default=22)  # 存端口号，默认为22
    idc = models.ForeignKey('IDC', on_delete=models.CASCADE)

    # remote_users = models.ManyToManyField('RomoteUser')  # 存远程登录的用户名密码
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '服务器表：Host'
        verbose_name_plural = '服务器表：Host'


# 服务器分组
class HostGroup(models.Model):
    name = models.CharField(max_length=128, unique=True)
    # hosts = models.ManyToManyField('Host')
    host_to_remote_users = models.ManyToManyField('HostToRemoteUser')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '服务器分组表：HostGroup'
        verbose_name_plural = '服务器分组表：HostGroup'


# 机房表
class IDC(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房表：IDC'
        verbose_name_plural = '机房表：IDC'


# 创建账号函数
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

    def create_superuser(self, email, name, password=None):
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


# 账号表
class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=32, verbose_name="full name")
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    objects = UserProfileManager()  # 变量名必须要是 objects ，不能为其他
    host_to_remote_users = models.ManyToManyField('HostToRemoteUser', blank=True, null=True)
    host_group = models.ManyToManyField('HostGroup', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = '堡垒机账号表：UserProfile'
        verbose_name_plural = '堡垒机账号表：UserProfile'


# 绑定主机和用户的对应关系
class HostToRemoteUser(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE)
    remote_user = models.ForeignKey('RomoteUser', on_delete=models.CASCADE)

    def __str__(self):
        return '%s:%s}' %(self.host,self.remote_user)

    class Meta:
        verbose_name = '绑定主机和用户的对应关系：HostToRemoteUser'
        verbose_name_plural = '绑定主机和用户的对应关系：HostToRemoteUser'
        unique_together = ('host', 'remote_user')


# 远程机器表
class RomoteUser(models.Model):
    auth_type_choices = ((0, 'ssh-password'), (1, 'ssh-key'))  # 密码类型
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0)
    username = models.CharField(max_length=32)  # 存用户名
    password = models.CharField(max_length=64, blank=True, null=True)  # 存明文密码

    def __str__(self):
        return '{}:{}'.format(self.username, self.password)

    class Meta:
        verbose_name = '远程机器表：RomoteUser'
        verbose_name_plural = '远程机器表：RomoteUser'
        unique_together = ('auth_type', 'username', 'password')


# 操作日志表
class AuditLog(models.Model):
    class Meta:
        verbose_name = '操作日志表：AuditLog'
        verbose_name_plural = '操作日志表：AuditLog'
