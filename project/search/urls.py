from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'search'

urlpatterns = [
    path('', views.search, name= 'home'),
    path('recommend_result', views.recommend_result, name = 'recommend_result'),
    path('random_wait', views.random_wait, name='random_wait'),
    path('random_result', views.random_result, name='random_result'),
    path('like/<int:menu_id>/',views.like_menu, name='like_menu'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)