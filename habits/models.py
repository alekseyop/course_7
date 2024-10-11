"""
Модель Habit представляет привычку пользователя.

Атрибуты:
    user (ForeignKey): Пользователь, которому принадлежит привычка.
    place (CharField): Место, где осуществляется привычка.
    time (TimeField): Время выполнения привычки.
    action (CharField): Действие или цель привычки.
    is_pleasant (BooleanField): Признак того, приятна ли привычка.
    linked_habit (ForeignKey): Связанная привычка (может быть пустой), которая должна быть приятной.
    periodicity (PositiveIntegerField): Периодичность выполнения привычки в днях (по умолчанию 1).
    reward (CharField): Вознаграждение за выполнение привычки (может быть пустым).
    execution_time (PositiveIntegerField): Время выполнения привычки в секундах.
    is_public (BooleanField): Признак того, является ли привычка публичной.

Методы:
    clean(): Проверяет корректность данных перед сохранением модели.
    save(*args, **kwargs): Переопределяет метод сохранения для выполнения валидации.

Meta:
    verbose_name: "Привычка"
    verbose_name_plural: "Привычки"
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.models import Users

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={"is_pleasant": True}
    )
    periodicity = models.PositiveIntegerField(default=1)  # в днях
    reward = models.CharField(max_length=255, **NULLABLE)
    execution_time = models.PositiveIntegerField(help_text="Время в секундах")
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.execution_time > 120:
            raise ValidationError(_("Время выполнения не может превышать 120 секунд."))
        if self.reward and self.linked_habit:
            raise ValidationError(_("Можно установить только одно вознаграждение или связанную привычку."))
        if self.periodicity < 7:
            raise ValidationError(_("Привычку нельзя выполнять реже, чем раз в 7 дней."))
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError(_("Приятная привычка не может иметь награды или связанной привычки."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"Habit: {self.action} at {self.time} in {self.place}"
