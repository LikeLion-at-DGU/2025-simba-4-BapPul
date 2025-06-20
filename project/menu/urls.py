# menu/urls.py

from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('store/<int:store_id>/menu/<int:menu_id>/', views.store_detail, name='store_detail'),
]
