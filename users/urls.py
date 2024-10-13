from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import UsersViewSet, UsersCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UsersViewSet)  # CRUD для пользователей

urlpatterns = [
    path("", include(router.urls)),  # Включение маршрутов роутера
    path("login/", TokenObtainPairView.as_view(), name="login"),  # JWT авторизация
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Обновление токена
    path("register/", UsersCreateAPIView.as_view(), name="register"),  # Регистрация
]
