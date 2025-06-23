from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
  path('start/', start_view, name='start'),
  path('login/', login, name="login"),
  path('logout/', logout, name='logout'),
  path('signup/', signup, name='signup'),
  path('mypage/', mypage, name='mypage'),
  path('mypage/<int:id>/likes/', my_likes, name='my_likes'),
  path('mypage/<int:id>/visits', my_visits, name='my_visits'),
  path('mypage/<int:id>/reviews', my_reviews, name='my_reviews'),
  path('edit-profile/', edit_profile, name='edit_profile'),
]