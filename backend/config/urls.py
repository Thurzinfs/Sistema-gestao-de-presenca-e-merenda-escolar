from django.contrib import admin
from django.urls import path

from config.api import app

urlpatterns = [path('admin/', admin.site.urls), path('api/v1/', app.urls)]
