from django.urls import path
from .views import HabitListCreateView, HabitDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "habits"

urlpatterns = [
    # Маршрут для списка привычек и создания новой
    path("habits/", HabitListCreateView.as_view(), name="habit-list-create"),
    # Маршрут для просмотра, обновления или удаления конкретной привычки
    path("habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
