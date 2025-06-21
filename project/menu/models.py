# menu/models.py
from django.db import models
from search.models import School
from accounts.models import Profile
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # ✅ 여기 추가
    number = models.TextField(null=True, blank=True)
    open_time = models.TextField(null= True, blank = True)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True) 

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Menu(models.Model):
    name = models.CharField(max_length=100)  # 메뉴 이름 (필수)
    price = models.PositiveIntegerField()    # 가격 (필수)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='menus')
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True) 

    def __str__(self):
        return f"{self.store.name} - {self.name} ({self.price}원)"

class Review(models.Model):
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateField(auto_now_add=True)

    content = models.TextField(blank=True)  # 리뷰 텍스트 (선택)
    rating = models.IntegerField(default=5)  # 별점: 1~5
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)  # 사진

    def __str__(self):
        return f"{self.writer.nickname}님의 {self.menu.name} 리뷰"

class VisitLog(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='visit_logs')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='visit_logs')
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True, related_name='visit_logs')

    visited_at = models.DateTimeField(default=datetime.now)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.nickname} 방문 - {self.store.name}"
    
class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True, related_name='likes')