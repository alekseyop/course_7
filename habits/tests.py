from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import Users
from .models import Habit


class HabitAPITestCase(APITestCase):
    """
    Тесты для проверки работы API привычек (Habit API).

    Методы:
        - setUp: Подготовка окружения для тестов, создание пользователя и привычки.
        - test_create_habit: Тестирует успешное создание новой привычки.
        - test_update_habit: Тестирует успешное обновление существующей привычки.
        - test_delete_habit: Тестирует успешное удаление привычки.
        - test_create_habit_invalid_data: Тестирует создание привычки с некорректными данными (не проходит валидацию).
        - test_get_habit_list: Тестирует получение списка привычек для пользователя.
    """

    def setUp(self):
        """
        Настройка тестового окружения.

        Создается пользователь и одна привычка для него.
        Пользователь аутентифицируется в системе для выполнения запросов.
        """
        self.user = Users.objects.create(email="testuser@example.com", telegram_id="123456")
        self.user.set_password("password")  # Убедитесь, что пароль хеширован
        self.user.save()

        # Создаем привычку для пользователя
        self.habit = Habit.objects.create(
            user=self.user,
            place="Park",
            time="12:00",
            action="Running",
            is_pleasant=False,
            periodicity=7,
            execution_time=60,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """
        Тестирует успешное создание новой привычки.

        Проверяется:
            - Ответ API с кодом 201 (Created).
            - Фактическое создание новой привычки в базе данных.
            - Корректность возвращенных данных привычки.
        """
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Gym",
            "time": "08:00",
            "action": "Workout",
            "is_pleasant": False,
            "periodicity": 7,
            "execution_time": 90,
            "is_public": False,
        }

        response = self.client.post(url, data, format="json")

        # Проверяем, что ответ имеет статус 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что привычка действительно создана
        self.assertEqual(Habit.objects.filter(user=self.user).count(), 2)

        # Проверяем корректность возвращенных данных
        self.assertEqual(response.data["place"], "Gym")
        self.assertEqual(response.data["action"], "Workout")

    def test_update_habit(self):
        """
        Тестирует успешное обновление существующей привычки.

        Проверяется:
            - Ответ API с кодом 200 (OK).
            - Обновление данных привычки в базе данных.
        """
        url = reverse("habits:habit-detail", args=[self.habit.id])
        data = {
            "place": "Home",
            "time": "07:00",
            "action": "Yoga",
            "is_pleasant": True,
            "periodicity": 7,
            "execution_time": 30,
            "is_public": True,
        }
        response = self.client.put(url, data, format="json")

        # Проверяем, что ответ имеет статус 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные привычки обновлены
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, "Home")
        self.assertEqual(self.habit.action, "Yoga")
        self.assertEqual(self.habit.execution_time, 30)

    def test_delete_habit(self):
        """
        Тестирует успешное удаление привычки.

        Проверяется:
            - Ответ API с кодом 204 (No Content).
            - Удаление привычки из базы данных.
        """
        url = reverse("habits:habit-detail", args=[self.habit.id])
        response = self.client.delete(url, format="json")

        # Проверяем, что ответ имеет статус 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что привычка была удалена
        self.assertEqual(Habit.objects.filter(user=self.user).count(), 0)

    def test_create_habit_invalid_data(self):
        """
        Тестирует создание привычки с некорректными данными.

        Проверяется:
            - Ответ API с кодом 400 (Bad Request).
            - Наличие ошибок валидации для полей `periodicity` и `execution_time`.
        """
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Park",
            "time": "09:00",
            "action": "Running",
            "is_pleasant": False,
            "periodicity": 6,  # Ошибка: периодичность меньше 7
            "execution_time": 130,  # Ошибка: время выполнения больше 120 секунд
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")

        # Проверяем, что ответ имеет статус 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем, что ошибки валидации присутствуют
        self.assertIn("periodicity", response.data)
        self.assertIn("execution_time", response.data)

    def test_get_habit_list(self):
        """
        Тестирует получение списка привычек пользователя.

        Проверяется:
            - Ответ API с кодом 200 (OK).
            - Количество возвращенных привычек.
            - Корректность возвращенных данных первой привычки в списке.
        """
        url = reverse("habits:habit-list-create")
        response = self.client.get(url, format="json")

        # Проверяем, что ответ имеет статус 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что список содержит 1 привычку
        self.assertEqual(Habit.objects.filter(user=self.user).count(), 1)

        # Проверяем, что данные в списке совпадают с ожидаемыми
        self.assertEqual(response.json()[0]["place"], "Park")
        self.assertEqual(response.json()[0]["action"], "Running")
