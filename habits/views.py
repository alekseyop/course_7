from django.core.exceptions import ValidationError
from requests import Response
from rest_framework import generics, viewsets, permissions, status
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .tasks import send_telegram_message


class IsOwner(permissions.BasePermission):
    """
    Кастомное разрешение, позволяющее доступ только владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение предоставляется только если пользователь является владельцем объекта
        return obj.user == request.user
class HabitPagination(PageNumberPagination):
    """
    Класс пагинации для привычек.

    Параметры:
        - page_size (int): Количество привычек на одной странице (по умолчанию 5).
    """

    page_size = 5


class HabitListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка привычек и создания новой привычки.

    Методы:
        - GET: Возвращает список привычек текущего аутентифицированного пользователя.
        - POST: Создает новую привычку, связанную с текущим пользователем.

    Права доступа:
        - Только аутентифицированные пользователи (IsAuthenticated).

    Особенности:
        - При создании новой привычки она автоматически привязывается к пользователю,
          отправившему запрос.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает список привычек, принадлежащих текущему аутентифицированному пользователю.
        """
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Привязывает создаваемую привычку к текущему пользователю.
        Выполняет проверку на валидность перед сохранением.
        """
        try:
            serializer.save(user=self.request.user)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления или удаления конкретной привычки.

    Методы:
        - GET: Возвращает информацию о конкретной привычке текущего пользователя.
        - PUT: Обновляет информацию о привычке.
        - DELETE: Удаляет привычку.

    Права доступа:
        - Только владелец привычки может получить доступ (IsAuthenticated + IsOwner).
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # Добавляем проверку прав владельца

    def get_permissions(self):
        """
        Возвращает права доступа для текущего запроса.
        """
        return [permission() for permission in self.permission_classes]

    def get_object(self):
        """
        Возвращает объект привычки, принадлежащий текущему пользователю.
        """
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)  # Проверяем права на уровне объекта
        return obj

class ReminderViewSet(viewsets.ViewSet):
    """
    Вьюсет для отправки напоминаний о привычках в Telegram.

    Методы:
        - send_reminder: Отправляет напоминание о привычке через Telegram.

    Права доступа:
        - Только аутентифицированные пользователи (IsAuthenticated).

    Особенности:
        - Используется асинхронная задача для отправки напоминания в Telegram.
        - Ожидается, что у пользователя в профиле есть поле `telegram_chat_id` для отправки сообщений.
    """

    permission_classes = [IsAuthenticated]

    def send_reminder(self, request, habit_id):
        """
        Отправляет напоминание о привычке в Telegram.

        Args:
            request (Request): Запрос пользователя.
            habit_id (int): Идентификатор привычки.

        Returns:
            Response: Ответ с подтверждением отправки напоминания.
        """
        habit = Habit.objects.get(id=habit_id, user=request.user)
        chat_id = request.user.profile.telegram_chat_id  # предполагается, что есть поле в профиле
        send_telegram_message.delay(habit_id, chat_id)
        return Response({"status": "Напоминание отправлено!"})


class PublicHabitListView(generics.ListAPIView):
    """
    Представление для получения списка публичных привычек.

    Методы:
        - GET: Возвращает список публичных привычек (is_public=True).

    Права доступа:
        - Доступно для всех (AllowAny).

    Пагинация:
        - Используется пагинация HabitPagination (по 5 привычек на странице).
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPagination
