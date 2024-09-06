from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Изменение вкладки user-a в админ панели."""

    role = models.CharField(
        "Роль",
        choices=[
            ("Пользователь", "Пользователь"),
            ("Редактор", "Редактор"),
            ("Администратор", "Администратор"),
        ],
        default="Пользователь",
    )

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
