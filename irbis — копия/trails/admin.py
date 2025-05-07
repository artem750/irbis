from django.contrib import admin
from trails.models import Trail  # Импортируйте вашу модель

# Регистрация модели в админке
admin.site.register(Trail)
