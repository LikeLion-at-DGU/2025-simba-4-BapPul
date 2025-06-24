# menu/urls.py

from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('<int:store_id>/menu/<int:menu_id>/', views.store_detail, name='store_detail'),
    path('<int:store_id>/reviews/', views.store_review_list, name='store_review_list'),
    path('<int:store_id>/location/<int:menu_id>/', views.store_location, name='store_location'),  # 선택적으로 menu_id 받는 버전 추가
    path('<int:store_id>/<int:menu_id>/review/', views.store_review, name='store_review'),
    path('<int:store_id>/<int:menu_id>/review/confirm/', views.review_confirm, name='review_confirm'),
    path('like/<int:menu_id>/', views.like_menu_in_menu_app, name='like_menu'),
]