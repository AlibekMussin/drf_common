# Vendor
from datetime import datetime
from django.core.cache import cache
from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType


class DeleteManager(models.Manager):
    """
    Объекты не удаляются из БД,
    а помечаются как удаленные и фильтруется только неудаленные
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class CommonFields(models.Model):
    """
    Содержит мета-информацию о наследующих моделях -
    кто создал, когда создал и пометка на удаление
    """

    class Meta:
        abstract = True

    name_ru = models.CharField(
        verbose_name='Название на русском',
        max_length=128,
        null=True, blank=True
    )
    name_kk = models.CharField(
        verbose_name='Название на казахском',
        max_length=128,
        null=True, blank=True
    )
    created_by_user = models.ForeignKey(
        'user.User',
        verbose_name='Создано пользователем',
        related_name='created_%(class)ss',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True,
        editable=False,
        db_index=True,
        null=True,
        blank=True
    )
    updated_by_user = models.ForeignKey(
        'user.User',
        verbose_name='Обновлено работником',
        related_name='updated_%(class)ss',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлено',
        auto_now=True,
        editable=False,
        db_index=True
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалено',
        default=False,
        editable=False,
        db_index=True
    )

    deleted_by_user = models.ForeignKey(
        'user.User',
        verbose_name='Удалено работником',
        related_name='deleted_%(class)ss',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    deleted_at = models.DateTimeField(
        verbose_name='Когда удалена запись',
        editable=False,
        null=True, blank=True
    )

    objects = DeleteManager()

    def delete(self, using=None, keep_parents=False):
        if self.is_deleted:
            return
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    def __str__(self):
        try:
            if hasattr(self, 'name'):
                try:
                    return self.name if self.name else ""
                except:
                    return "нет объекта названия"
            try:
                return super().__str__()
            except (TypeError, AttributeError):
                return "Без названия"
        except:
            return ""

    @transaction.atomic
    def save(self, *args, **kwargs):
        save_data = super().save(*args, **kwargs)
        # print("cache_clear")
        cache.clear()
        return save_data


class Country(CommonFields):
    code = models.CharField(
        max_length=512,
        verbose_name="Код для внутреннего использования",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name_ru if self.name_ru else ""

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class RegionTypeChoice(models.TextChoices):
    """Тип населенного пункта"""
    REGION = 'REGION', 'Область'
    CITY = 'CITY', 'Город'
    DISTRICT = 'DISTRICT', 'Район города'


class Region(CommonFields):  # DONE
    """Регионы"""
    short_name_ru = models.CharField(
        verbose_name='Сокращенное название на русском',
        max_length=128,
        null=True, blank=True
    )
    short_name_en = models.CharField(
        verbose_name='Сокращенное название на английском',
        max_length=128,
        null=True, blank=True
    )
    short_name_kk = models.CharField(
        verbose_name='Сокращенное название на казахском',
        max_length=128,
        null=True, blank=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Родительский регион',
        related_name='children',
        null=True,
        blank=True
    )
    is_popular = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        verbose_name='Популярный город для выбора'
    )
    is_default = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        verbose_name='Регион по умолчанию'
    )
    code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Код для внутреннего использования"
    )
    country = models.ForeignKey(
        Country,
        verbose_name="Страна",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(
        "Действующий регион",
        default=False,
        blank=True,
        null=True
    )
    coordinates = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Координаты границ региона"
    )
    coordinates_additional = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Координаты границ региона (дополнительные)"
    )
    region_type = models.CharField(
        verbose_name="Тип региона",
        choices=RegionTypeChoice.choices,
        default=RegionTypeChoice.CITY,
        max_length=32
    )
    centroid = models.JSONField(
        verbose_name="Центр региона",
        blank=True,
        null=True
    )
    layer_name = models.CharField(
        verbose_name="Ссылка на дашбоард",
        null=True,
        blank=True
    )
    arcgis_id = models.CharField(
        null=True,
        blank=True,
        verbose_name="Уникальный ID из ARCGIS (OBJECTID)"
    )
    is_main = models.BooleanField(
        "Город республиканского/ областного значения",
        default=False,
    )
    order_number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Порядковый номер для сортировки"
    )

    def __str__(self):
        if self.short_name_ru:
            return f'{self.short_name_ru} ({self.get_region_type_display()})'
        else:
            return f'{self.name_ru} ({self.get_region_type_display()})'

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
