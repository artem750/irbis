

from django.urls import path
from .views import get_trails, get_trail_with_coords

urlpatterns = [
    path('get_trails/', get_trails, name='get_trails'),
    path('get_trail_with_coords/<str:trail_name>/', get_trail_with_coords, name='get_trail_with_coords'),
]
