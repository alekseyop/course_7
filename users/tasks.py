from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import Users


@shared_task
def block_inactive_users():
    """
    Задача для блокировки неактивных пользователей, которые не заходили на сайт больше 30 дней.
    """
    threshold_date = timezone.now() - timedelta(days=30)  # Устанавливаем порог в 30 дней
    inactive_users = Users.objects.filter(last_login__lt=threshold_date, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()

    return f"{len(inactive_users)} пользователей заблокировано."
