from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search, name= 'home'),
    path('recommend_result', views.recommend_result, name = 'recommend_result'),
    path('random', views.random, name='random'),
    path('random_result', views.random_result, name='random_result'),
]