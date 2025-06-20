from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
  path('start/', start_view, name='start'),
  path('login/', login, name="login"),
  path('logout/', logout, name='logout'),
  path('signup/', signup, name='signup'),
  path('mypage/<int:id>', mypage, name='mypage'),
]