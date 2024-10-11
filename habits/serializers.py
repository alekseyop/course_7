from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.

    Поля:
        - id (int): Уникальный идентификатор привычки.
        - user (ForeignKey): Пользователь, владелец привычки. Поле только для чтения.
        - place (str): Место выполнения привычки.
        - time (TimeField): Время выполнения привычки.
        - action (str): Действие, описывающее привычку.
        - is_pleasant (bool): Флаг, указывающий, является ли привычка приятной.
        - linked_habit (ForeignKey): Другая привычка, связанная с текущей.
        - periodicity (int): Периодичность выполнения привычки (в днях).
        - reward (str): Вознаграждение за выполнение привычки.
        - execution_time (int): Время выполнения привычки (в секундах).
        - is_public (bool): Флаг, указывающий, публична ли привычка.

    Валидация:
        - validate_execution_time: Проверяет, что время выполнения не превышает 120 секунд.
        - validate_periodicity: Проверяет, что привычка выполняется не реже, чем раз в 7 дней.
        - validate: Общая валидация данных:
            - Нельзя одновременно указать вознаграждение и связанную привычку.
            - Связанная привычка должна быть приятной.
            - Приятная привычка не может иметь вознаграждения или связанную привычку.

    Исключения:
        - serializers.ValidationError: Возникает в случае, если данные не проходят валидацию.
    """

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "linked_habit",
            "periodicity",
            "reward",
            "execution_time",
            "is_public",
        ]
        read_only_fields = ["user"]

    def validate_execution_time(self, value):
        """
        Валидация времени выполнения привычки.

        Args:
            value (int): Время выполнения в секундах.

        Raises:
            serializers.ValidationError: Если время выполнения превышает 120 секунд.

        Returns:
            int: Валидное значение времени выполнения.
        """
        if value > 120:
            raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд.")
        return value

    def validate_periodicity(self, value):
        """
        Валидация периодичности выполнения привычки.

        Args:
            value (int): Периодичность выполнения привычки в днях.

        Raises:
            serializers.ValidationError: Если периодичность выполнения привычки меньше 7 дней.

        Returns:
            int: Валидное значение периодичности.
        """
        if value < 7:
            raise serializers.ValidationError("Привычку нельзя выполнять реже, чем раз в 7 дней.")
        return value

    def validate(self, data):
        """
        Общая валидация данных.

        Args:
            data (dict): Данные, которые необходимо проверить.

        Raises:
            serializers.ValidationError:
                - Если одновременно указаны вознаграждение и связанная привычка.
                - Если связанная привычка не является приятной.
                - Если приятная привычка имеет вознаграждение или связанную привычку.

        Returns:
            dict: Валидные данные.
        """
        if data.get("reward") and data.get("linked_habit"):
            raise serializers.ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")
        if data.get("linked_habit") and not data["linked_habit"].is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")
        if data.get("is_pleasant") and (data.get("reward") or data.get("linked_habit")):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь вознаграждения или связанную привычку."
            )
        return data
