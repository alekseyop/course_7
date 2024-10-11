"""
Маршруты для приложения 'users'.

Определяет маршруты для взаимодействия с пользователями и управления аутентификацией через JWT.

Маршруты:
    - "/users/" (CRUD операции для пользователей с использованием ViewSet).
    - "/login/" (JWT авторизация с использованием 'TokenObtainPairView').
    - "/token/refresh/" (Обновление JWT токена через 'TokenRefreshView').
    - "/register/" (Регистрация нового пользователя через 'UsersCreateAPIView').

Используемый роутер:
    - DefaultRouter: для автоматической генерации маршрутов для ViewSet.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import (
    UsersViewSet,
    UsersCreateAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Имя приложения (используется для пространств имен в URL)
app_name = UsersConfig.name

# Создание роутера для ViewSet
router = DefaultRouter()
router.register(r"users", UsersViewSet)  # CRUD операции для пользователей

# Определение URL-маршрутов
urlpatterns = [
    path("", include(router.urls)),  # Включение маршрутов роутера
    path("login/", TokenObtainPairView.as_view(), name="login"),  # JWT авторизация
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Обновление токена
    path("register/", UsersCreateAPIView.as_view(), name="register"),  # Регистрация
]
