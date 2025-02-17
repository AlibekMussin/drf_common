# Vendor
from django.contrib import admin

# Local
from . models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_joined'
    search_fields = ['id', 'username', 'email',]
    list_display = ['id',
                    'is_active',
                    'username',
                    'email',
                    'date_joined',]
    readonly_fields = [
        'password',
        'is_superuser',
        'is_staff',
        'date_joined',
        'user_permissions'
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['id', 'last_name', 'first_name', 'user__username',]
    autocomplete_fields = ['user',]
    list_display = ['id',
                    'user',
                    'last_name',
                    'first_name']