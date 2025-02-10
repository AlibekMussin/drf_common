# Vendor
from django.contrib import admin

# Local
from . models import *


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    search_fields = ['id', 'hash_name',]
    list_display = ['id',
                    'original_name',
                    'created_at',]
