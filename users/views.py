"""
ViewSet и APIView для управления пользователями.

Классы:
    - UsersViewSet: ViewSet для выполнения CRUD операций с пользователями (доступ только для аутентифицированных пользователей).
    - UsersCreateAPIView: APIView для регистрации новых пользователей (доступ разрешен без авторизации).

Классы разрешений:
    - IsAuthenticated: доступ к CRUD операциям предоставляется только аутентифицированным пользователям.
    - AllowAny: доступ к регистрации открыт для всех пользователей.
"""

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from users.models import Users
from users.serializers import UsersSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)


class UsersViewSet(viewsets.ModelViewSet):
    """
    ViewSet для выполнения операций CRUD с пользователями.

    Доступ разрешен только для аутентифицированных пользователей.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут выполнять операции


class UsersCreateAPIView(CreateAPIView):
    """
    APIView для регистрации новых пользователей.

    Доступ открыт для всех пользователей (без необходимости авторизации).
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]  # Доступ разрешен всем для регистрации новых пользователей
