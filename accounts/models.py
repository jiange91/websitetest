from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(default=timezone.now)
    mod_time = models.DateTimeField(auto_now=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-c_time']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username + ':   ' + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = 'confirmation code'
        verbose_name_plural = 'confirmation codes'
