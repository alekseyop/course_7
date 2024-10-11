from users.models import Users
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Команда для создания суперпользователя.

    Эта команда создает нового суперпользователя с указанными данными.
    Пользователь создается с адресом электронной почты "admin@example.com", паролем "1q2w3e",
    а также с установленными правами администратора, активного пользователя, и суперпользователя.

    Методы:
        - handle: Основной метод, выполняющий создание суперпользователя.
    """

    def handle(self, *args, **options):
        """
        Создает нового суперпользователя с предопределенными данными.

        Пользователь создается с:
            - email: "admin@example.com"
            - пароль: "1q2w3e"
            - права администратора и суперпользователя.
        """
        user = Users.objects.create(email="admin@example.com")
        user.set_password("1q2w3e")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
