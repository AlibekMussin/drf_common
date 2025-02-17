import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class GenderChoice(models.TextChoices):
    """Пол"""
    MALE = 'MALE', 'Мужчина'
    FEMALE = 'FEMALE', 'Женщина'
    NOT_DEFINED = 'NOT_DEFINED', 'Не определен'


class LanguageChoice(models.TextChoices):
    """Язык"""
    KK = 'KK', 'Казахский'
    RU = 'RU', 'Русский'
    EN = 'EN', 'Английский'


class User(AbstractUser):
    language = models.CharField(
        choices=LanguageChoice.choices,
        default=LanguageChoice.KK,
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Язык интерфейса"
    )
    is_blocked = models.BooleanField(
        default=False,
        verbose_name="Заблокирован"
    )
    activate_token = models.UUIDField(
        null=True,
        blank=True,
        verbose_name="Хэш для активации аккаунта"
    )
    groups = models.ManyToManyField(
        Group,
        related_name='group_users',  # Уникальное имя для обратной ссылки
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='permission_users',  # Уникальное имя для обратной ссылки
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.activate_token:
            self.activate_token = uuid.uuid4()
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Person(models.Model):
    """ Данные физических лиц """
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="person"
    )
    last_name = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Зашифрованная фамилия"
    )
    first_name = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Имя"
    )
    patronymic = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Отчество"
    )
    gender = models.CharField(
        "Пол",
        choices=GenderChoice.choices,
        default=GenderChoice.MALE,
        max_length=32
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
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
        name = ''
        if self.last_name:
            name += self.last_name + ' '
        if self.first_name and self.first_name is not None:
            name += self.first_name + ' '
        if self.patronymic and self.patronymic is not None:
            name += self.patronymic + ' '

        return name.strip()

    @property
    def full_name(self):
        last_name = self.last_name
        full_name = f"{last_name}"
        if self.first_name:
            full_name = f"{last_name} {self.first_name}"
        if self.patronymic and self.patronymic is not None:
            full_name = f"{last_name} {self.first_name} {self.patronymic}"
        return full_name.strip()

    @property
    def full_name_with_initials(self):
        last_name = self.last_name
        full_name = f"{last_name}"
        if self.first_name:
            full_name = f"{last_name} {self.first_name[0]}."
        if self.patronymic and self.patronymic is not None:
            full_name = f"{last_name} {self.first_name[0]}. {self.patronymic[0]}."
        return full_name.strip()

    class Meta:
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"
