# Vendor
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Local
from . import views

router = routers.SimpleRouter()

urlpatterns = [
    path('download/<str:filename>/', views.download_file_view, name='download_file'),
]
