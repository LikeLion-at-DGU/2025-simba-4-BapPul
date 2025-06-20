from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search, name= 'home'),
    path('recommend_result', views.recommend_result, name = 'recommend_result'),
]