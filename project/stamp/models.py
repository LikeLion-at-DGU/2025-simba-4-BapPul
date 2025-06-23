from django.db import models
from django.utils import timezone
from accounts.models import Profile
from menu.models import Review
from django.db.models.signals import post_save
from django.dispatch import receiver

class RiceMap(models.Model):
    """유저별 밥지도"""
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rice_maps')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.nickname}의 밥지도 ({self.created_at.date()})"

class RiceGrain(models.Model):
    """밥풀 (사진 리뷰 1건 당 1개, 하루에 1개만 인정)"""
    rice_map = models.ForeignKey(RiceMap, on_delete=models.CASCADE, related_name='rice_grains')
    date = models.DateField(default=timezone.now)  # 하루 1개 제한 체크용
    review_id = models.IntegerField()  # 해당 리뷰와 연결
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rice_map', 'date')  # 하루에 한 개만!

    def __str__(self):
        return f"밥풀 - {self.date} - {self.rice_map.owner.nickname}"

class Riceball(models.Model):
    """밥풀 9개가 모이면 생성되는 주먹밥"""
    rice_map = models.ForeignKey(RiceMap, on_delete=models.CASCADE, related_name='riceballs')
    created_at = models.DateTimeField(auto_now_add=True)
    reward_given = models.BooleanField(default=False)  # 포인트 지급 여부

    def __str__(self):
        return f"주먹밥 - {self.rice_map.owner.nickname} - {self.created_at.date()}"
