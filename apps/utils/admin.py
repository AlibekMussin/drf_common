from datetime import datetime
from django.contrib import admin, messages
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name_ru', 'name_kk')
    readonly_fields = ['created_by_user',
                       'updated_by_user',
                       'created_at',
                       'created_at',
                       'deleted_by_user',
                       'deleted_at'
                       ]

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.deleted_at = datetime.now()
            obj.is_deleted = True
            obj.save()


def make_active(self, request, queryset):
    updated = queryset.update(is_active=True)
    self.message_user(request, f"{updated} запись(и) были успешно активированы", messages.SUCCESS)


def make_not_active(self, request, queryset):
    updated = queryset.update(is_active=False)
    self.message_user(request, f"{updated} запись(и) были успешно деактивированы", messages.SUCCESS)


make_active.short_description = "Сделать действующими"
make_not_active.short_description = "Сделать бездействующими"


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name_ru', 'name_kk', ]
    list_display = ('id',
                    'custom_is_main',
                    'custom_order_number',
                    'is_active',
                    'parent',
                    'region_type',
                    'name_ru',
                    'short_name_ru',

                    )
    list_filter = ['region_type', 'is_active', 'is_main']
    autocomplete_fields = ['parent',]

    readonly_fields = ['created_by_user',
                       'updated_by_user',
                       'created_at',
                       'created_at',
                       'deleted_by_user',
                       'deleted_at'
                       ]
    actions = [make_active, make_not_active]

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.deleted_at = datetime.now()
            obj.is_deleted = True
            obj.save()

    @admin.display(boolean=True, ordering='is_main')
    def custom_is_main(self, obj):
        return obj.is_main

    @admin.display(ordering='order_number')
    def custom_order_number(self, obj):
        return obj.order_number

    custom_is_main.short_description = 'Is main'
    custom_order_number.short_description = 'Order number'
