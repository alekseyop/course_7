from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from django_countries.fields import CountryField

NULLABLE = {"blank": True, "null": True}


class Users(AbstractUser):
    """
    Модель пользователя, наследуемая от AbstractUser, с модифицированной системой авторизации на основе email.

    Поля:
    - email: Электронная почта, используется как уникальный идентификатор для аутентификации.
    - phone_number: Номер телефона пользователя.
    - country: Страна проживания пользователя.
    - avatar: Аватар пользователя.
    - token: Токен для дополнительных операций (например, аутентификация через сторонние сервисы).
    - city: Город проживания пользователя.

    Атрибуты:
    - USERNAME_FIELD: Используем email вместо стандартного username для авторизации.
    - REQUIRED_FIELDS: Список обязательных полей для создания пользователя.
    """

    username = None  # Убираем поле username
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Электронная почта")

    phone_number = PhoneNumberField(
        unique=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
        **NULLABLE,
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    token = models.CharField(max_length=100, verbose_name="Токен", **NULLABLE)
    city = models.CharField(max_length=100, verbose_name="Город", **NULLABLE)
    telegram_id = models.CharField(max_length=50, verbose_name="Telegram ID", help_text="Введите Telegram ID")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Возвращает строковое представление пользователя — его email.
        """
        return self.email
