from django.urls import path
from . import views
from .views import rice_map

app_name = 'stamp'

urlpatterns = [
    path('', views.rice_map_main, name='rice_map_main'),
    path('map/', views.rice_map, name='rice_map'),
]
