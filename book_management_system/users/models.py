from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 添加一些自定义字段以强制创建迁移
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='电话号码')
    address = models.TextField(null=True, blank=True, verbose_name='地址')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(null=True, blank=True, verbose_name='个人简介')  # 添加新字段
    
    class Meta:
        db_table = 'custom_users'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_active_borrows(self):
        return self.borrowrecord_set.filter(status='borrowed')
