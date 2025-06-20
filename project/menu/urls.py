# menu/urls.py

from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('<int:store_id>/menu/<int:menu_id>/', views.store_detail, name='store_detail'),
    path('<int:store_id>/reviews/', views.store_review_list, name='store_review_list'),
    path('<int:store_id>/location/', views.store_location, name = 'store_location'),
]