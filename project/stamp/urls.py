from django.urls import path
from .views import rice_map

app_name = 'stamp'

urlpatterns = [
    path('rice-map/', rice_map, name='rice_map'),
]
