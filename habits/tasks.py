import os
import requests
from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from datetime import datetime

TELEGRAM_URL = os.getenv("TELEGRAM_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


@shared_task
def send_telegram_message(habit_id, chat_id):
    """
    Асинхронная задача для отправки сообщения в Telegram.
    """
    habit = Habit.objects.get(id=habit_id)
    message = f"Напоминание: {habit.action} в {habit.time} в {habit.place}."

    url = f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return f"Напоминание отправлено для привычки {habit.action}."
    else:
        return f"Ошибка при отправке напоминания для привычки {habit.action}."


@shared_task
def send_daily_reminders():
    """
    Периодическая задача для отправки ежедневных напоминаний о привычках.
    """
    current_time = timezone.now().time()
    habits = Habit.objects.filter(time__lte=current_time, is_public=True)

    for habit in habits:
        chat_id = habit.user.profile.telegram_chat_id  # Предполагаем, что у пользователя есть профиль с chat_id
        send_telegram_message.delay(habit.id, chat_id)

    return f"Напоминания отправлены для {habits.count()} привычек."
