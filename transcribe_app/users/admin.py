from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import CastomToken, User


admin.site.unregister(Group)


@admin.register(CastomToken)
class CastomTokenAdmin(admin.ModelAdmin):
    """Отображение в админ панели токена."""


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'is_active', 'last_login', 'is_staff'
    )
    list_filter = ('is_active', 'is_staff', 'groups')
    search_fields = ('id', 'username', 'email')
    ordering = ('id', 'username', 'last_login')
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Личная информация'), {'fields': ('first_name', 'last_name', 'email')}),  # noqa
        (_('Разрешения'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
