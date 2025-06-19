# menu/models.py

from django.db import models
from search.models import School

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

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Menu(models.Model):
    name = models.CharField(max_length=100)  # 메뉴 이름 (필수)
    price = models.PositiveIntegerField()    # 가격 (필수)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='menus')
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True) 

    def __str__(self):
        return f"{self.store.name} - {self.name} ({self.price}원)"
