from django.db import models
from django.utils import timezone
from accounts.models import Profile
from menu.models import Review
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models.signals import post_save
from django.dispatch import receiver


class RiceMap(models.Model):
    #유저별 밥지도
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rice_maps')
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner.nickname}의 밥지도 ({self.created_at.date()})"

class RiceGrain(models.Model):
    rice_map = models.ForeignKey(RiceMap, on_delete=models.CASCADE, related_name='rice_grains')
    date = models.DateField(default=timezone.now)  # 생성되는 날짜
    review = models.OneToOneField(Review, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rice_map', 'date')  # 하루 한 개 제한

    def __str__(self):
        return f"밥풀 - {self.date} - {self.rice_map.owner.nickname}"

@receiver(post_save, sender=Review)
def create_rice_grain_for_review(sender, instance, created, **kwargs):
    print("✅ post_save 시그널 호출됨")
    if not created:
        return

    profile = instance.writer

    # ✅ 가장 최신의 밥지도 가져오기
    rice_map = RiceMap.objects.filter(owner=profile).order_by('-created_at').first()

    # ❗ 밥지도가 하나도 없는 경우 (이상적인 상황은 아님) → 새로 생성
    if not rice_map:
        rice_map = RiceMap.objects.create(owner=profile)

    today = timezone.now().date()

    # ✅ 오늘 밥풀이 이미 있으면 중단
    if RiceGrain.objects.filter(rice_map=rice_map, date=today).exists():
        return

    # ✅ 밥풀 생성
    RiceGrain.objects.create(
        rice_map=rice_map,
        review=instance,
        date=today
    )

    # ✅ 밥풀 수 체크 → 9개면 주먹밥 + 맵 종료 + 새 맵 생성
    grain_count = rice_map.rice_grains.count()
    if grain_count == 9:
        Riceball.objects.create(rice_map=rice_map)
        rice_map.finished_at = timezone.now().date()
        rice_map.save()

        RiceMap.objects.create(owner=profile)



class Riceball(models.Model):
    #밥풀 9개가 모이면 생성되는 주먹밥
    rice_map = models.ForeignKey(RiceMap, on_delete=models.CASCADE, related_name='riceballs')
    created_at = models.DateTimeField(auto_now_add=True)
    reward_given = models.BooleanField(default=False)  # 포인트 지급 여부
    point = models.PositiveIntegerField(default=2000)

    def __str__(self):
        return f"주먹밥 - {self.rice_map.owner.nickname} - {self.created_at.date()}"


@receiver(post_save, sender=Profile)
def create_default_rice_map(sender, instance, created, **kwargs):
    if created:
        RiceMap.objects.create(owner=instance)