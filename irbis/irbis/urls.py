from django.contrib import admin
from django.urls import path, include
from views import show_map  # Импорт вашего представления

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', show_map, name='map'),
    path('trails/', include('trails.urls')),
]
