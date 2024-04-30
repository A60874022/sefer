from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CastomToken, User


admin.site.unregister(Group)


@admin.register(CastomToken)
class CastomTokenAdmin(admin.ModelAdmin):
    """Отображение в админ панели токена."""


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение в админ панели пользователя."""
