from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/user/', include('apps.user.urls')),
    path('api/v1/file/', include('apps.file.urls')),
    path('api/v1/admin/', admin.site.urls),

]
