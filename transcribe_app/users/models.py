from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Изменение вкладки user-a в админ панели."""

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
