from rest_framework import viewsets
from rest_framework.generics import CreateAPIView


from users.models import Users
from users.serializers import UsersSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)  # Для разрешения доступа


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]  # Закрываем доступ авторизацией


class UsersCreateAPIView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ для регистрации без авторизации
