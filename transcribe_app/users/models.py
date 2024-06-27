from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Изменение вкладки user-a в админ панели."""

    pass
