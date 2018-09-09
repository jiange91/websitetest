from django.db import models
from activities.models import Activities
from accounts.models import User


class LikeCount(models.Model):
    act = models.ForeignKey(Activities, on_delete=models.CASCADE)
    liked_num = models.IntegerField(default=0)


class LikeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True)
    act = models.ForeignKey(Activities, on_delete=models.CASCADE)


class ParCount(models.Model):
    act = models.ForeignKey(Activities, on_delete=models.CASCADE)
    par_num = models.IntegerField(default=0)


class ParRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    par_time = models.DateTimeField(auto_now_add=True)
    act = models.ForeignKey(Activities, on_delete=models.CASCADE)