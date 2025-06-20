from django.db import models
from django.contrib.auth.models import User
from search.models import School  # School 모델은 search 앱
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 1:1 대응
    nickname = models.TextField(max_length=10)
    school = models.ForeignKey(School, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nickname} ({self.user.username})"
    
