# Vendor
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Local
from . import views as views

router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login_by_email/', views.LoginByEmailView.as_view(), name='login_by_email'),
]