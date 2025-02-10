# Vendor
from django.db import models

class File(models.Model):
    original_name = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name="Оригинальное название"
    )
    hash_name = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name="Хэшированное название"
    )
    file = models.FileField(
        verbose_name="Файл",
        upload_to='uploads/',
        null=True,
        blank=True,
    )
    file_path = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name="Физическое расположение файла"
    )
    mime_type = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name="Формат документа"
    )
    size = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name="Размер (кБ)"
    )
    created_at = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True,
        editable=False,
        db_index=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"[{self.id}] - {str(self.original_name)}"

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
