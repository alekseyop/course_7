from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import Users


class UsersTests(APITestCase):
    """
    Набор тестов для проверки функционала API пользователей.

    Этот класс содержит тесты для различных сценариев работы с пользователями:
    регистрация, аутентификация, получение списка пользователей, обновление данных,
    удаление и работа с JWT-токенами.

    Методы:
        - setUp: Устанавливает начальные данные для тестов.
        - test_get_users_list: Тестирует получение списка пользователей (требуется аутентификация).
        - test_register_user: Тестирует регистрацию нового пользователя.
        - test_login_user: Тестирует процесс входа и получение JWT токена.
        - test_token_refresh: Тестирует обновление JWT токена.
        - test_get_user_detail: Тестирует получение деталей конкретного пользователя.
        - test_update_user: Тестирует обновление данных пользователя.
        - test_delete_user: Тестирует удаление пользователя.
    """

    def setUp(self):
        """
        Инициализация тестового пользователя и клиента для выполнения запросов.

        Создает тестового пользователя и аутентифицирует запросы от его имени.
        """
        self.client = APIClient()
        self.user = Users.objects.create(email="testuser@example.com", password="password", telegram_id="123456")
        self.user.set_password("password")  # Убедитесь, что пароль хеширован
        self.user.save()

    def test_get_users_list(self):
        """
        Тестовое получение списка пользователей (требуется аутентификация).

        Отправляется GET-запрос на получение списка пользователей, результат должен быть успешным (200 OK).
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        """
        Тестовая регистрация пользователя.

        Отправляется POST-запрос на регистрацию нового пользователя, результат должен быть успешным (201 Created).
        """
        url = reverse("users:register")
        data = {"email": "newuser@example.com", "password": "newpassword123", "telegram_id": "654321"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Users.objects.filter(email="newuser@example.com").exists())

    def test_login_user(self):
        """
        Тест входа пользователя для получения JWT токена.

        Отправляется POST-запрос с данными для входа, результат должен быть успешным (200 OK),
        с возвратом JWT-токенов (access и refresh).
        """
        url = reverse("users:login")
        data = {
            "email": "testuser@example.com",
            "password": "password",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        """
        Тест обновления JWT токена.

        Отправляется POST-запрос для обновления JWT-токена с использованием refresh-токена.
        Ожидается успешное обновление (200 OK) и получение нового access-токена.
        """
        login_url = reverse("users:login")
        login_data = {"email": "testuser@example.com", "password": "password"}
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", login_response.data)
        refresh_token = login_response.data["refresh"]

        refresh_url = reverse("users:token_refresh")
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(refresh_url, refresh_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_get_user_detail(self):
        """
        Тестирование получения конкретных сведений о пользователе.

        Отправляется GET-запрос на получение данных о пользователе, результат должен быть успешным (200 OK)
        с корректными данными.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_user(self):
        """
        Тестовое обновление данных пользователя.

        Отправляется PATCH-запрос на обновление данных пользователя (например, изменение города),
        результат должен быть успешным (200 OK) с обновленными данными.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users-detail", kwargs={"pk": self.user.id})
        data = {"city": "New City"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "New City")

    def test_delete_user(self):
        """
        Тестовое удаление пользователя.

        Отправляется DELETE-запрос для удаления пользователя, результат должен быть успешным (204 No Content).
        Проверяется, что пользователь действительно удален из базы данных.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users-detail", kwargs={"pk": self.user.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Users.objects.filter(id=self.user.id).exists())
