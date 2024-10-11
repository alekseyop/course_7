from rest_framework import serializers
from users.models import Users


class UsersSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя (Users).

    Этот сериализатор используется для представления данных пользователей и обработки создания
    или обновления пользователя, с особым вниманием к полю пароля, которое шифруется перед сохранением.

    Поля:
        - id (int): Идентификатор пользователя.
        - username (str): Имя пользователя.
        - first_name (str): Имя.
        - last_name (str): Фамилия.
        - email (str): Электронная почта пользователя.
        - password (str): Пароль пользователя (хранится в зашифрованном виде).
        - telegram_id (str): Идентификатор пользователя в Telegram.
        - city (str): Город проживания пользователя.

    Методы:
        - create: Создает нового пользователя с зашифрованным паролем.
        - update: Обновляет данные существующего пользователя и, если предоставлен новый пароль,
                  шифрует его перед сохранением.
    """

    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "telegram_id",
            "city",
        ]

    def create(self, validated_data):
        """
        Создает нового пользователя с зашифрованным паролем.

        Args:
            validated_data (dict): Проверенные данные пользователя.

        Returns:
            Users: Созданный объект пользователя с зашифрованным паролем.
        """
        password = validated_data.pop("password")
        user = Users(**validated_data)
        user.set_password(password)  # Шифруем пароль перед сохранением
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Обновляет существующего пользователя и шифрует новый пароль, если он был предоставлен.

        Args:
            instance (Users): Объект пользователя, который будет обновлен.
            validated_data (dict): Проверенные данные для обновления.

        Returns:
            Users: Обновленный объект пользователя.
        """
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
