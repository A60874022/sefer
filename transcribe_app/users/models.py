from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Изменение вкладки user-a в админ панели."""


class CastomToken(Token):
    """Перевод модели Token для админ панели."""

    class Meta(Token.Meta):
        verbose_name = _("Токен")
        verbose_name_plural = _("Токены")
